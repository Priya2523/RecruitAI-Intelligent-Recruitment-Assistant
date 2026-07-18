"""
RecruitAI - Intelligent Recruitment Assistant
Cleaned deployment version (Render / Hugging Face Spaces compatible).
"""

import os
import re
import json

import fitz  # PyMuPDF
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # headless backend, required on servers with no display
import matplotlib.pyplot as plt
import gradio as gr
from groq import Groq

# --------------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------------

os.makedirs("charts", exist_ok=True)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

MODEL_NAME = "llama-3.3-70b-versatile"

# --------------------------------------------------------------------------
# PDF / text extraction
# --------------------------------------------------------------------------

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    document = fitz.open(pdf_path)
    text = ""
    for page in document:
        text += page.get_text()
    document.close()
    return text


def _clean_json_response(raw_text):
    """Strip markdown code fences Groq sometimes wraps JSON in."""
    result = raw_text.strip()
    result = re.sub(r"^```json", "", result)
    result = re.sub(r"^```", "", result)
    result = re.sub(r"```$", "", result)
    return result.strip()


# --------------------------------------------------------------------------
# Groq-powered parsing / evaluation
# --------------------------------------------------------------------------

def parse_jd_with_groq(jd_text):
    prompt = f"""
You are an expert recruitment assistant.

Extract the following information from this Job Description.

Return ONLY valid JSON.

Format:

{{
    "job_title":"",
    "skills":[],
    "experience":"",
    "education":"",
    "location":""
}}

Job Description:

{jd_text}
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    result = _clean_json_response(response.choices[0].message.content)
    return json.loads(result)


def parse_resume_with_groq(resume_text):
    prompt = f"""
You are an expert recruitment assistant.

Extract information from this resume.

Return ONLY valid JSON.

Format:

{{
    "candidate_name":"",
    "skills":[],
    "experience":"",
    "education":"",
    "location":"",
    "certifications":[],
    "projects":[]
}}

Resume:

{resume_text}
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    result = _clean_json_response(response.choices[0].message.content)
    return json.loads(result)


def evaluate_candidate(jd_profile, resume_profile):
    prompt = f"""
You are an experienced Senior HR Recruitment Manager.

Your task is to compare a Job Description with a Candidate Profile.

Think like a recruiter.

Do NOT simply compare keywords.

Analyze:

1. Technical Skills
2. Domain Experience
3. Education
4. Certifications
5. Location
6. Overall suitability

If the candidate is NOT suitable,
suggest 3 better job roles based on the candidate profile.

Finally decide ONE of these:

- Strong Fit
- Good Fit
- Partial Fit
- Not Fit

Interview Decision must be ONLY one:

- Shortlist
- Hold
- Reject

Job Description

{json.dumps(jd_profile, indent=2)}

Candidate Profile

{json.dumps(resume_profile, indent=2)}

Return ONLY valid JSON.

{{
    "overall_score": 0,
    "fit_level": "",
    "reasoning": [],
    "better_suited_roles": [],
    "interview_decision": "",
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "concerns": [],
    "recommendation": ""
}}
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    result = _clean_json_response(response.choices[0].message.content)
    return json.loads(result)


# --------------------------------------------------------------------------
# Python-side scoring (no LLM)
# --------------------------------------------------------------------------

def extract_years(exp_text):
    """Pull the first integer out of strings like '3 years', '2-5 Years'."""
    numbers = re.findall(r"\d+", str(exp_text))
    if not numbers:
        return 0
    return int(numbers[0])


def calculate_score(jd_profile, resume_profile):
    score = 0
    breakdown = {}

    # ---- Skills (40) ----
    skill_alias = {
        "microsoft excel": ["excel", "ms excel", "microsoft excel", "excell", "ms office"],
        "erp systems (sap / oracle)": ["sap", "oracle"],
        "communication skills": ["communication", "communication skills"],
        "documentation management": ["documentation"],
    }

    resume_skills = [s.lower() for s in resume_profile.get("skills", [])]
    jd_skills = [s.lower() for s in jd_profile.get("skills", [])]

    matched = 0
    for jd_skill in jd_skills:
        found = False
        if jd_skill in skill_alias:
            for alias in skill_alias[jd_skill]:
                if any(alias in rs for rs in resume_skills):
                    found = True
                    break
        else:
            if any(jd_skill in rs for rs in resume_skills):
                found = True
        if found:
            matched += 1

    skill_score = round((matched / len(jd_skills)) * 40) if jd_skills else 0
    score += skill_score
    breakdown["Skill Score"] = skill_score

    # ---- Experience (20) ----
    candidate_years = extract_years(resume_profile.get("experience", ""))
    exp = jd_profile.get("experience", "")
    nums = re.findall(r"\d+", str(exp))

    # Original code assumed a "min-max" range and crashed on a single number
    # (e.g. "5 years"). Made robust to 0, 1, or 2 numbers.
    if len(nums) >= 2:
        jd_min, jd_max = int(nums[0]), int(nums[1])
    elif len(nums) == 1:
        jd_min = jd_max = int(nums[0])
    else:
        jd_min = jd_max = 0

    if jd_min <= candidate_years <= jd_max:
        experience_score = 20
    elif candidate_years > jd_max:
        experience_score = 15
    elif candidate_years >= (jd_min - 1):
        experience_score = 10
    else:
        experience_score = 5

    score += experience_score
    breakdown["Experience Score"] = experience_score

    # ---- Education (10) ----
    education = resume_profile.get("education", "").lower()
    if any(x in education for x in ["logistics", "supply chain", "commerce", "business administration"]):
        education_score = 10
    elif "bachelor" in education or "b.tech" in education:
        education_score = 7
    elif "diploma" in education:
        education_score = 5
    else:
        education_score = 2
    score += education_score
    breakdown["Education Score"] = education_score

    # ---- Location (10) ----
    jd_location = jd_profile.get("location", "").lower()
    resume_location = resume_profile.get("location", "").lower()
    location_score = 10 if jd_location and jd_location in resume_location else 5
    score += location_score
    breakdown["Location Score"] = location_score

    # ---- Certifications (10) ----
    certs = len(resume_profile.get("certifications", []))
    if certs >= 3:
        cert_score = 10
    elif certs >= 1:
        cert_score = 6
    else:
        cert_score = 2
    score += cert_score
    breakdown["Certification Score"] = cert_score

    # ---- Projects (10) ----
    projects = len(resume_profile.get("projects", []))
    if projects >= 3:
        project_score = 10
    elif projects >= 1:
        project_score = 7
    else:
        project_score = 2
    score += project_score
    breakdown["Project Score"] = project_score

    return score, breakdown


# --------------------------------------------------------------------------
# Main pipeline called by the Gradio UI
# --------------------------------------------------------------------------

def evaluate_pipeline(jd_file, resume_files):

    empty_df = pd.DataFrame(columns=["Rank", "Candidate", "Score", "Decision"])

    if client is None:
        return (
            empty_df, 0, 0, 0, 0, 0,
            "No candidates found.",
            "⚠️ GROQ_API_KEY is not set on the server. Add it in your hosting "
            "platform's environment variables and redeploy.",
            None, None,
        )

    if not jd_file or not resume_files:
        return (
            empty_df, 0, 0, 0, 0, 0,
            "No candidates found.",
            "Please upload a Job Description and at least one resume.",
            None, None,
        )

    with open(jd_file.name, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_profile = parse_jd_with_groq(jd_text)
    required_skills = jd_profile.get("skills", [])

    candidates = []

    for resume in resume_files:
        try:
            resume_text = extract_text_from_pdf(resume.name)
            profile = parse_resume_with_groq(resume_text)

            python_score, breakdown = calculate_score(jd_profile, profile)
            ai = evaluate_candidate(jd_profile, profile)

            candidate_skills = profile.get("skills", [])
            matched = [s for s in candidate_skills if s.lower() in [x.lower() for x in required_skills]]
            missing = [s for s in required_skills if s.lower() not in [x.lower() for x in candidate_skills]]

            candidates.append({
                "Candidate": profile.get("candidate_name", ""),
                "Score": python_score,
                "Matched Skills": matched,
                "Missing Skills": missing,
                "Education": profile.get("education", ""),
                "Experience": profile.get("experience", ""),
                "Decision": ai.get("interview_decision", "Hold"),
                "Fit": ai.get("fit_level", "Unknown"),
            })

        except Exception as e:
            print(f"Resume Error ({getattr(resume, 'name', 'unknown')}): {e}")

    candidates = sorted(candidates, key=lambda x: x["Score"], reverse=True)

    ranking = []
    medals = ["🥇", "🥈", "🥉"]
    for i, c in enumerate(candidates):
        rank = medals[i] if i < 3 else str(i + 1)
        ranking.append([rank, c["Candidate"], c["Score"], c["Decision"]])

    ranking_df = pd.DataFrame(ranking, columns=["Rank", "Candidate", "Score", "Decision"])

    total = len(candidates)
    shortlisted = sum(x["Decision"].lower() == "shortlist" for x in candidates)
    hold = sum(x["Decision"].lower() == "hold" for x in candidates)
    rejected = total - shortlisted - hold
    highest = candidates[0]["Score"] if total else 0

    chart_path = None
    pie_chart_path = None

    if total > 0:
        names = [c["Candidate"] for c in candidates]
        scores = [c["Score"] for c in candidates]

        plt.figure(figsize=(8, 4))
        plt.bar(names, scores)
        plt.title("Candidate Score Comparison")
        plt.xlabel("Candidates")
        plt.ylabel("Score")
        plt.xticks(rotation=30)
        plt.tight_layout()
        chart_path = "charts/score_chart.png"
        plt.savefig(chart_path)
        plt.close()

        pie_chart_path = "charts/candidate_status.png"
        plt.figure(figsize=(5, 5))
        plt.pie(
            [shortlisted, hold, rejected],
            labels=["Shortlisted", "Hold", "Rejected"],
            autopct="%1.1f%%",
            startangle=90,
        )
        plt.title("    Candidate Status Distribution")
        plt.savefig(pie_chart_path, bbox_inches="tight")
        plt.close()

    if total:
        top = candidates[0]
        candidate_card = f"""
# 👤 {top['Candidate']}

### ⭐ Score : **{top['Score']}**

### 🎓 Education

{top['Education']}

### 💼 Experience

{top['Experience']}

### 🟢 Matched Skills

{'<br>'.join('✅ ' + x for x in top['Matched Skills'])}

### 🔴 Missing Skills

{'<br>'.join('❌ ' + x for x in top['Missing Skills'])}
"""

        recommendation = f"""
## 🤖 AI Recommendation

**Fit Level:** {top['Fit']}

**Interview Decision:** {top['Decision']}

Matched **{len(top['Matched Skills'])}** required skills.

Missing **{len(top['Missing Skills'])}** required skills.

Proceed according to recruiter policy.
"""
    else:
        candidate_card = "No candidates found."
        recommendation = "No recommendation available."

    return (
        ranking_df,
        total,
        shortlisted,
        hold,
        rejected,
        highest,
        candidate_card,
        recommendation,
        chart_path,
        pie_chart_path,
    )


# --------------------------------------------------------------------------
# Gradio UI
# --------------------------------------------------------------------------

with gr.Blocks(title="RecruitAI - Intelligent Recruitment Assistant") as demo:

    gr.Markdown("""
<div style='text-align:center;
padding:25px;
border-radius:20px;
background:linear-gradient(90deg,#4F46E5,#7C3AED);
color:white;
box-shadow:0px 4px 15px rgba(0,0,0,0.2);'>

<h1>🤖 RecruitAI</h1>

<h3>Intelligent Recruitment Assistant</h3>

<p>
Upload one Job Description and multiple resumes to automatically rank
candidates using AI + Python Scoring.
</p>

</div>
""")

    gr.Markdown("## 📂 Upload Documents")

    with gr.Row():
        jd_file = gr.File(label="📄 Job Description (.txt)", file_types=[".txt"])
        resume_files = gr.File(
            label="📑 Candidate Resumes (.pdf)",
            file_types=[".pdf"],
            file_count="multiple",
        )

    evaluate_btn = gr.Button("🚀 Evaluate Candidates", variant="primary", size="lg")

    gr.Markdown("---")

    gr.Markdown("""
# 📊 Recruitment Dashboard

### AI Powered Hiring Analytics
""")

    with gr.Row():
        total_candidates = gr.Number(label="👥 Total Candidates", interactive=False)
        shortlisted = gr.Number(label="🟢 Shortlisted", interactive=False)
        hold = gr.Number(label="🟡 Hold", interactive=False)
        rejected = gr.Number(label="🔴 Rejected", interactive=False)
        highest_score = gr.Number(label="🏆 Highest Score", interactive=False)

    gr.Markdown("---")

    gr.Markdown("## 🏅 Candidate Ranking")

    results_table = gr.Dataframe(
        headers=["Rank", "Candidate", "Score", "Decision"],
        interactive=False,
        wrap=True,
    )

    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
# 👤 Candidate Profile

AI Generated Candidate Summary
""")
            candidate_card = gr.Markdown()

        with gr.Column(scale=1):
            gr.Markdown("""
# 🤖 AI Recommendation

Python Scoring + LLM Recommendation
""")
            recommendation_box = gr.Markdown()

    gr.Markdown("---")

    gr.Markdown("# 📈 Candidate Analytics")

    with gr.Row():
        score_chart = gr.Image(label="📊 Candidate Score Comparison", type="filepath", interactive=False)
        pie_chart = gr.Image(label="🥧    Candidate Status Distribution", type="filepath", interactive=False)

    evaluate_btn.click(
        fn=evaluate_pipeline,
        inputs=[jd_file, resume_files],
        outputs=[
            results_table,
            total_candidates,
            shortlisted,
            hold,
            rejected,
            highest_score,
            candidate_card,
            recommendation_box,
            score_chart,
            pie_chart,
        ],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
