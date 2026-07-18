

import os
import fitz  # PyMuPDF
import pandas as pd

from google.colab import files
uploaded = files.upload()

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text

sample_resume = os.path.join(
    "/content/MANSI GURAV Resumepdf.pdf"
)

resume_text = extract_text_from_pdf(sample_resume)

print(resume_text[:2000])

resume_files = [f for f in os.listdir() if f.endswith(".pdf")]

resume_data = []

for file in resume_files:

    pdf_path = file

    text = extract_text_from_pdf(pdf_path)

    resume_data.append({
        "Candidate": file,
        "Resume_Text": text
    })

print("Total resumes processed:", len(resume_data))

resume_df = pd.DataFrame(resume_data)

resume_df.head()

def read_job_description(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return text

jd_files = [f for f in os.listdir() if f.endswith(".txt")]

print("Total Job Descriptions:", len(jd_files))
print()

for jd in jd_files:
    print(jd)

for jd in jd_files:
    print("=" * 50)
    print("Job:", jd)
    print("=" * 50)

    with open(jd, "r", encoding="utf-8") as f:
        text = f.read()

    print(text[:500])   # Print first 500 characters
    print()

jd_data = {}

for jd in jd_files:
    with open(jd, "r", encoding="utf-8") as f:
        jd_data[jd] = f.read()

print("Loaded", len(jd_data), "Job Descriptions")

for name, content in jd_data.items():
    print("=" * 70)
    print("Job Title:", name)
    print("=" * 70)
    print(content[:500])      # First 500 characters
    print("\n")



import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

resume_files = [f for f in os.listdir() if f.endswith(".pdf")]

import fitz
import os

resume_files = [f for f in os.listdir() if f.endswith(".pdf")]

print(resume_files)

resume_file = resume_files[0]   # Opens the first PDF

doc = fitz.open(resume_file)

resume_text = ""

for page in doc:
    resume_text += page.get_text()

doc.close()

print(resume_text[:1000])

import fitz
import os

resume_files = [f for f in os.listdir() if f.endswith(".pdf")]

for resume_file in resume_files:
    print("=" * 50)
    print("Processing:", resume_file)

    doc = fitz.open(resume_file)

    text = ""
    for page in doc:
        text += page.get_text()

    doc.close()

    print(text[:500])

model = SentenceTransformer("all-MiniLM-L6-v2")

results = []

resume_embedding = model.encode(resume_text)

for jd_name, jd_text in jd_data.items():

    jd_embedding = model.encode(jd_text)

    score = cosine_similarity(
        [resume_embedding],
        [jd_embedding]
    )[0][0]

    results.append((jd_name, score))

results = sorted(results, key=lambda x: x[1], reverse=True)

for jd, score in results:
    print(f"{jd} --> {score*100:.2f}%")

jd_skills = {
    "BIM_MEP_Modeller.txt": [
        "Revit MEP",
        "AutoCAD",
        "Navisworks",
        "HVAC",
        "Plumbing",
        "Fire Fighting",
        "Clash Detection"
    ],

    "Transport_Executive.txt": [
        "Transportation Management",
        "Logistics",
        "Import Export",
        "SAP",
        "Fleet Management",
        "Dispatch",
        "Vendor Management"
    ],

    "cyber_security_Intern.txt": [
        "Python",
        "Networking",
        "Cyber Security",
        "IDS",
        "Machine Learning"
    ],

    "SEO_Executive.txt": [
        "SEO",
        "Google Analytics",
        "Keyword Research",
        "Technical SEO"
    ],

    "Full_Stack_Developer_Intern.txt": [
        "Python",
        "React",
        "HTML",
        "CSS",
        "JavaScript",
        "MySQL",
        "ASP.NET"
    ]
}

resume_lower = resume_text.lower()

for jd, skills in jd_skills.items():

    matched = []

    for skill in skills:
        if skill.lower() in resume_lower:
            matched.append(skill)

    print("\n", jd)
    print("Matched Skills:", matched)

best_jd, best_score = results[0]

print("Best Job Recommendation")
print("-----------------------")
print("Role :", best_jd)
print("Match :", round(best_score*100,2), "%")

for jd, skills in jd_skills.items():

    matched = []
    missing = []

    for skill in skills:
        if skill.lower() in resume_text.lower():
            matched.append(skill)
        else:
            missing.append(skill)

    print("="*60)
    print("Job:", jd)
    print("Matched Skills :", matched)
    print("Missing Skills :", missing)

best_jd, best_score = results[0]

matched = []
missing = []

for skill in jd_skills[best_jd]:
    if skill.lower() in resume_text.lower():
        matched.append(skill)
    else:
        missing.append(skill)

print("========== RecruitAI Recommendation ==========\n")

print("Recommended Role :", best_jd)
print("Match Score      :", round(best_score*100,2), "%")

print("\nMatched Skills")
for s in matched:
    print("✔", s)

print("\nMissing Skills")
for s in missing:
    print("✘", s)

import os

resume_folder = "Resume"

resume_files = [f for f in os.listdir() if f.endswith(".pdf")]
print(resume_files)

import os

resume_files = [f for f in os.listdir() if f.lower().endswith(".pdf")]
print(resume_files)

all_resumes = {}

for file in resume_files:

    doc = fitz.open(file)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    all_resumes[file] = text
print("Loaded",len(all_resumes),"resumes")

selected_jd = "Transport_Executive.txt"

jd_text = jd_data[selected_jd]
jd_embedding = model.encode(jd_text)

results = []

for resume_name, resume_text in all_resumes.items():

    resume_embedding = model.encode(resume_text)

    score = cosine_similarity(
        [jd_embedding],
        [resume_embedding]
    )[0][0]

    results.append((resume_name, score))

results = sorted(results, key=lambda x: x[1], reverse=True)

print("===== Candidate Ranking =====\n")

for i, (resume, score) in enumerate(results, start=1):
    print(f"{i}. {resume} --> {score*100:.2f}%")

jd_skills = {
    "Transport_Executive.txt": [
        "Transportation Management",
        "Logistics",
        "Import",
        "Export",
        "Fleet Management",
        "SAP",
        "Dispatch",
        "Vendor Management"
    ]
}

selected_skills = jd_skills[selected_jd]

for resume_name, resume_text in all_resumes.items():

    matched = []

    for skill in selected_skills:
        if skill.lower() in resume_text.lower():
            matched.append(skill)

    print("="*60)
    print("Candidate :", resume_name)
    print("Matched Skills :", matched)

for resume_name, score in results:

    if score >= 0.75:
        decision = "✅ Strongly Recommended"

    elif score >= 0.60:
        decision = "🟡 Recommended"

    elif score >= 0.40:
        decision = "🟠 Consider"

    else:
        decision = "❌ Not Suitable"

    print(f"{resume_name:35} {score*100:.2f}%   {decision}")

import re

def extract_skills(text, skill_list):
    text = text.lower()

    matched = []

    for skill in skill_list:
        if skill.lower() in text:
            matched.append(skill)

    return matched

MASTER_SKILLS = [

    "Python",
    "SQL",
    "Power BI",
    "Excel",
    "Tableau",

    "AWS",
    "Azure",
    "Docker",
    "Kubernetes",

    "Java",
    "C++",
    "React",
    "Node.js",

    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",

    "Pandas",
    "NumPy",

    "SAP",
    "Logistics",
    "Fleet Management",
    "Import Export",

    "AutoCAD",
    "Revit MEP",
    "HVAC",
    "Fire Fighting"
]

candidate_profiles = []

for name, text in all_resumes.items():

    profile = {

        "Candidate": name,

        "Skills": extract_skills(text, MASTER_SKILLS),

        "Text": text

    }

    candidate_profiles.append(profile)

for candidate in candidate_profiles:

    print(candidate["Candidate"])

    print(candidate["Skills"])

    print("="*60)

jd_profile = {}

jd_profile["Skills"] = extract_skills(jd_text, MASTER_SKILLS)

print(jd_profile)



from groq import Groq
from google.colab import userdata

api_key = userdata.get("recruit_api")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Reply with only one word: Connected"
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)

import json
import re

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
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    # Remove markdown code blocks if present
    result = re.sub(r"^```json", "", result)
    result = re.sub(r"^```", "", result)
    result = re.sub(r"```$", "", result)
    result = result.strip()

    return json.loads(result)

jd_profile = parse_jd_with_groq(jd_text)

print(jd_profile)

import json
import re

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
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    result = re.sub(r"^```json", "", result)
    result = re.sub(r"^```", "", result)
    result = re.sub(r"```$", "", result)

    result = result.strip()

    return json.loads(result)

resume_profile = parse_resume_with_groq(
    all_resumes["A_Priya.pdf"]
)

print(json.dumps(resume_profile, indent=4))

import json
import re

def evaluate_candidate(jd_profile, resume_profile):

    prompt = f"""
You are an experienced technical recruiter.

Evaluate the candidate against the Job Description.

Job Description:

{json.dumps(jd_profile, indent=2)}

Candidate:

{json.dumps(resume_profile, indent=2)}

Return ONLY valid JSON.

Format:

{{
  "overall_score": 0,
  "matched_skills": [],
  "missing_skills": [],
  "strengths": [],
  "concerns": [],
  "recommendation": ""
}}

Scoring should be fair and based on:
- Skills
- Experience
- Education
- Location
- Certifications
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    result = re.sub(r"^```json", "", result)
    result = re.sub(r"^```", "", result)
    result = re.sub(r"```$", "", result)
    result = result.strip()

    return json.loads(result)

evaluation = evaluate_candidate(jd_profile, resume_profile)

print(json.dumps(evaluation, indent=4))

import json
import re

def evaluate_candidate(jd_profile, resume_profile):

    prompt = f"""
You are an experienced recruiter.

Compare the Job Description with the Candidate profile.

Scoring Rules:

Skills = 40 points
Experience = 20 points
Education = 10 points
Location = 10 points
Certifications = 10 points
Communication & Overall Profile = 10 points

The total overall_score MUST be between 0 and 100.

Job Description:

{json.dumps(jd_profile, indent=2)}

Candidate:

{json.dumps(resume_profile, indent=2)}

Return ONLY valid JSON.

{{
    "overall_score": 0,
    "skill_score": 0,
    "experience_score": 0,
    "education_score": 0,
    "location_score": 0,
    "certification_score": 0,
    "communication_score": 0,
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "concerns": [],
    "recommendation": ""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    result = re.sub(r"^```json", "", result)
    result = re.sub(r"^```", "", result)
    result = re.sub(r"```$", "", result)
    result = result.strip()

    return json.loads(result)

evaluation = evaluate_candidate(jd_profile, resume_profile)

print(json.dumps(evaluation, indent=4))

all_candidate_profiles = []

for filename, resume_text in all_resumes.items():

    print(f"Parsing {filename}...")

    profile = parse_resume_with_groq(resume_text)

    profile["file_name"] = filename

    all_candidate_profiles.append(profile)

print("Done!")

for profile in all_candidate_profiles:

    print("="*60)

    print(profile["candidate_name"])

    print(profile["skills"])

    print(profile["experience"])

all_evaluations = []

for candidate in all_candidate_profiles:

    print(f"Evaluating {candidate['candidate_name']}...")

    evaluation = evaluate_candidate(jd_profile, candidate)

    evaluation["candidate_name"] = candidate["candidate_name"]
    evaluation["file_name"] = candidate["file_name"]

    all_evaluations.append(evaluation)

print("Evaluation completed!")

for result in all_evaluations:

    print("="*80)
    print("Candidate :", result["candidate_name"])
    print("Score :", result["overall_score"])
    print("Recommendation :", result["recommendation"])

import pandas as pd

summary = []

for result in all_evaluations:

    summary.append({
        "Candidate": result["candidate_name"],
        "Score": result["overall_score"],
        "Recommendation": result["recommendation"]
    })

df = pd.DataFrame(summary)

df = df.sort_values(by="Score", ascending=False)

df

import pandas as pd

summary = []

for result in all_evaluations:

    summary = []

for result in all_evaluations:

    summary.append({
        "Candidate": result["candidate_name"],
        "Score": result["overall_score"],
        "Recommendation": result["recommendation"],
        "Strengths": ", ".join(result["strengths"]),
        "Concerns": ", ".join(result["concerns"]),
        "Matched Skills": ", ".join(result["matched_skills"]),
        "Missing Skills": ", ".join(result["missing_skills"])
    })

df = pd.DataFrame(summary)

df = df.sort_values(by="Score", ascending=False)

df

import json
import re

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
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    result = re.sub(r"^```json", "", result)
    result = re.sub(r"^```", "", result)
    result = re.sub(r"```$", "", result)
    result = result.strip()

    return json.loads(result)

all_evaluations = []

for candidate in all_candidate_profiles:

    print(f"Evaluating {candidate['candidate_name']}...")

    evaluation = evaluate_candidate(jd_profile, candidate)

    evaluation["candidate_name"] = candidate["candidate_name"]
    evaluation["file_name"] = candidate["file_name"]

    all_evaluations.append(evaluation)

print("Evaluation completed!")

import pandas as pd

summary = []

for result in all_evaluations:

    summary.append({

        "Candidate": result["candidate_name"],

        "Score": result["overall_score"],

        "Fit Level": result["fit_level"],

        "Interview": result["interview_decision"],

        "Better Roles": ", ".join(result["better_suited_roles"]),

        "Recommendation": result["recommendation"]

    })

df = pd.DataFrame(summary)

df = df.sort_values(by="Score", ascending=False)

df

for result in all_evaluations:

    print("=" * 100)

    print("Candidate:", result["candidate_name"])

    print("Score:", result["overall_score"])

    print("Fit Level:", result["fit_level"])

    print("Interview Decision:", result["interview_decision"])

    print("\nBetter Roles:")
    for role in result["better_suited_roles"]:
        print("-", role)

    print("\nReasoning:")
    for reason in result["reasoning"]:
        print("-", reason)

    print("\nStrengths:")
    for strength in result["strengths"]:
        print("-", strength)

    print("\nConcerns:")
    for concern in result["concerns"]:
        print("-", concern)

    print("\nRecommendation:")
    print(result["recommendation"])

    print("\n")

print(json.dumps(all_candidate_profiles[0], indent=4))

print(json.dumps(jd_profile, indent=4))

import re

def extract_years(exp_text):
    """
    Extract numeric years from strings like:
    '3 years'
    '13 Years'
    '2-5 Years'
    """
    numbers = re.findall(r"\d+", str(exp_text))

    if not numbers:
        return 0

    return int(numbers[0])


def calculate_score(jd_profile, resume_profile):

    score = 0

    breakdown = {}

    #########################################
    # Skills (40 Marks)
    #########################################

    jd_skills = set(skill.lower() for skill in jd_profile["skills"])
    resume_skills = set(skill.lower() for skill in resume_profile["skills"])

    matched = jd_skills.intersection(resume_skills)

    if len(jd_skills) > 0:
        skill_score = round((len(matched) / len(jd_skills)) * 40)
    else:
        skill_score = 0

    score += skill_score
    breakdown["Skill Score"] = skill_score

    #########################################
    # Experience (20 Marks)
    #########################################

    candidate_years = extract_years(resume_profile["experience"])

    jd_min = extract_years(jd_profile["experience"])

    if candidate_years >= jd_min:
        experience_score = 20
    else:
        experience_score = round((candidate_years / jd_min) * 20)

    score += experience_score
    breakdown["Experience Score"] = experience_score

    #########################################
    # Education (10 Marks)
    #########################################

    education = resume_profile["education"].lower()

    if "bachelor" in education or "b.tech" in education:
        education_score = 10
    elif "diploma" in education:
        education_score = 5
    else:
        education_score = 0

    score += education_score
    breakdown["Education Score"] = education_score

    #########################################
    # Location (10 Marks)
    #########################################

    if jd_profile["location"].lower() in resume_profile["location"].lower():
        location_score = 10
    else:
        location_score = 5

    score += location_score
    breakdown["Location Score"] = location_score

    #########################################
    # Certifications (10 Marks)
    #########################################

    if len(resume_profile["certifications"]) >= 3:
        cert_score = 10
    elif len(resume_profile["certifications"]) >= 1:
        cert_score = 5
    else:
        cert_score = 0

    score += cert_score
    breakdown["Certification Score"] = cert_score

    #########################################
    # Projects / Profile (10 Marks)
    #########################################

    if len(resume_profile["projects"]) >= 3:
        profile_score = 10
    elif len(resume_profile["projects"]) >= 1:
        profile_score = 5
    else:
        profile_score = 0

    score += profile_score
    breakdown["Profile Score"] = profile_score

    return score, breakdown

all_evaluations = []

for candidate in all_candidate_profiles:

    evaluation = evaluate_candidate(jd_profile, candidate)

    python_score, score_breakdown = calculate_score(
        jd_profile,
        candidate
    )

    evaluation["overall_score"] = python_score
    evaluation["score_breakdown"] = score_breakdown
    evaluation["candidate_name"] = candidate["candidate_name"]
    evaluation["file_name"] = candidate["file_name"]

    all_evaluations.append(evaluation)

print("Evaluation completed!")

print(all_evaluations[0])

import re

def extract_years(exp_text):
    numbers = re.findall(r"\d+", str(exp_text))
    if not numbers:
        return 0

    # Handle "2-5 Years" by taking the first number for minimum
    return int(numbers[0])


def calculate_score(jd_profile, resume_profile):

    score = 0
    breakdown = {}

    ####################################################
    # Skill Score (40)
    ####################################################

    skill_alias = {
        "microsoft excel": ["excel", "ms excel", "microsoft excel", "excell", "ms office"],
        "erp systems (sap / oracle)": ["sap", "oracle"],
        "communication skills": ["communication", "communication skills"],
        "documentation management": ["documentation"]
    }

    resume_skills = [s.lower() for s in resume_profile["skills"]]
    jd_skills = [s.lower() for s in jd_profile["skills"]]

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

    skill_score = round((matched / len(jd_skills)) * 40)

    score += skill_score

    breakdown["Skill Score"] = skill_score

    ####################################################
    # Experience (20)
    ####################################################

    candidate_years = extract_years(resume_profile["experience"])

    exp = jd_profile["experience"]

    nums = re.findall(r"\d+", exp)

    jd_min = int(nums[0])
    jd_max = int(nums[1])

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

    ####################################################
    # Education (10)
    ####################################################

    education = resume_profile["education"].lower()

    if any(x in education for x in ["logistics","supply chain","commerce","business administration"]):
        education_score = 10

    elif "bachelor" in education or "b.tech" in education:
        education_score = 7

    elif "diploma" in education:
        education_score = 5

    else:
        education_score = 2

    score += education_score

    breakdown["Education Score"] = education_score

    ####################################################
    # Location (10)
    ####################################################

    if jd_profile["location"].lower() in resume_profile["location"].lower():

        location_score = 10

    else:

        location_score = 5

    score += location_score

    breakdown["Location Score"] = location_score

    ####################################################
    # Certifications (10)
    ####################################################

    certs = len(resume_profile["certifications"])

    if certs >= 3:
        cert_score = 10

    elif certs >= 1:
        cert_score = 6

    else:
        cert_score = 2

    score += cert_score

    breakdown["Certification Score"] = cert_score

    ####################################################
    # Projects (10)
    ####################################################

    projects = len(resume_profile["projects"])

    if projects >= 3:
        project_score = 10

    elif projects >= 1:
        project_score = 7

    else:
        project_score = 2

    score += project_score

    breakdown["Project Score"] = project_score

    return score, breakdown

for r in all_evaluations:
    print(r["candidate_name"])
    print(r["overall_score"])
    print(r["score_breakdown"])
    print("-"*60)

import gradio as gr
print(gr.__version__)

import pandas as pd

def evaluate_pipeline(jd_file, resume_files):

    print(type(resume_files))
    print(resume_files)

    if resume_files:
        print("Number of resumes:", len(resume_files))
        for r in resume_files:
            print(r.name)

def evaluate_pipeline(jd_file, resume_files):

    # ---------- Read JD ----------
    with open(jd_file.name, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_profile = parse_jd_with_groq(jd_text)

    results = []

    # ---------- Read each resume ----------
    for resume in resume_files:

        text = extract_text_from_pdf(resume.name)

        profile = parse_resume_with_groq(text)

        python_score, breakdown = calculate_score(
            jd_profile,
            profile
        )

        ai_result = evaluate_candidate(
            jd_profile,
            profile
        )

        ai_result["overall_score"] = python_score

        results.append([
            profile["candidate_name"],
            python_score,
            ai_result["fit_level"],
            ai_result["interview_decision"]
        ])

    df = pd.DataFrame(
        results,
        columns=[
            "Candidate",
            "Score",
            "Fit Level",
            "Interview Decision"
        ]
    )

    df = df.sort_values(
        "Score",
        ascending=False
    )

    return df

import gradio as gr

with gr.Blocks(title="RecruitAI") as demo:

    gr.Markdown("# 🤖 RecruitAI - Intelligent Recruitment Assistant")
    gr.Markdown("Upload a Job Description and Resume Folder to evaluate candidates.")

    with gr.Row():
        jd_file = gr.File(label="📄 Upload Job Description")

        resume_files = gr.File(
            label="📁 Upload Resume Folder",
            file_count="multiple"
        )

    evaluate_btn = gr.Button("🚀 Evaluate Candidates")

    gr.Markdown("## 📊 Candidate Ranking")

    results_table = gr.Dataframe(
        headers=[
            "Candidate",
            "Score",
            "Fit Level",
            "Interview Decision"
        ],
        interactive=False
    )

    evaluate_btn.click(
        fn=evaluate_pipeline,
        inputs=[jd_file, resume_files],
        outputs=results_table
    )

if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0', server_port=7860)

import pandas as pd

def evaluate_pipeline(jd_file, resume_files):

    # Read JD
    with open(jd_file.name, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_profile = parse_jd_with_groq(jd_text)

    required_skills = jd_profile.get("skills", [])

    results = []

    for resume in resume_files:

        try:

            resume_text = extract_text_from_pdf(resume.name)

            profile = parse_resume_with_groq(resume_text)

            python_score, breakdown = calculate_score(
                jd_profile,
                profile
            )

            ai_result = evaluate_candidate(
                jd_profile,
                profile
            )

            candidate_skills = profile.get("skills", [])

            matched_skills = [
                skill
                for skill in candidate_skills
                if skill.lower() in [s.lower() for s in required_skills]
            ]

            missing_skills = [
                skill
                for skill in required_skills
                if skill.lower() not in [s.lower() for s in candidate_skills]
            ]

            recommendation = (
                f"Matched {len(matched_skills)} of "
                f"{len(required_skills)} required skills."
            )

            results.append([
                profile.get("candidate_name",""),
                python_score,
                ", ".join(required_skills),
                ", ".join(candidate_skills),
                ", ".join(matched_skills),
                ", ".join(missing_skills),
                profile.get("experience",""),
                profile.get("education",""),
                recommendation,
                ai_result["fit_level"],
                ai_result["interview_decision"]
            ])

        except Exception as e:

            print(f"Error processing {resume.name}: {e}")

    df = pd.DataFrame(

        results,

        columns=[

            "Candidate",

            "Score",

            "Required Skills",

            "Candidate Skills",

            "Matched Skills",

            "Missing Skills",

            "Experience",

            "Education",

            "AI Recommendation",

            "Fit Level",

            "Interview Decision"

        ]

    )

    df = df.sort_values(

        by="Score",

        ascending=False

    )

    return df

import gradio as gr

with gr.Blocks(
    title="RecruitAI",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown("# 🤖 RecruitAI - Intelligent Recruitment Assistant")
    gr.Markdown(
        "Upload a Job Description and multiple resumes to evaluate, rank and shortlist candidates."
    )

    with gr.Row():

        jd_file = gr.File(
            label="📄 Upload Job Description"
        )

        resume_files = gr.File(
            label="📁 Upload Multiple Resumes",
            file_count="multiple"
        )

    evaluate_btn = gr.Button(
        "🚀 Evaluate Candidates",
        variant="primary"
    )

    gr.Markdown("## 📊 Candidate Ranking")

    results_table = gr.Dataframe(
        headers=[
            "Candidate",
            "Score",
            "Required Skills",
            "Candidate Skills",
            "Matched Skills",
            "Missing Skills",
            "Experience",
            "Education",
            "Current CTC",
            "Expected CTC",
            "Notice Period",
            "AI Recommendation",
            "Fit Level",
            "Interview Decision"
        ],
        interactive=False,
        wrap=True
    )

    evaluate_btn.click(
        fn=evaluate_pipeline,
        inputs=[
            jd_file,
            resume_files
        ],
        outputs=results_table
    )

if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0', server_port=7860)

import matplotlib.pyplot as plt
import os

os.makedirs("charts", exist_ok=True)

import matplotlib.pyplot as plt
import os

os.makedirs("charts", exist_ok=True)

import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("charts", exist_ok=True)

def evaluate_pipeline(jd_file, resume_files):

    # --------------------------
    # Read JD
    # --------------------------
    with open(jd_file.name, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_profile = parse_jd_with_groq(jd_text)
    required_skills = jd_profile.get("skills", [])

    candidates = []

    # --------------------------
    # Process Resumes
    # --------------------------
    for resume in resume_files:

        try:

            resume_text = extract_text_from_pdf(resume.name)

            profile = parse_resume_with_groq(resume_text)

            python_score, breakdown = calculate_score(
                jd_profile,
                profile
            )

            ai = evaluate_candidate(
                jd_profile,
                profile
            )

            candidate_skills = profile.get("skills", [])

            matched = [
                s for s in candidate_skills
                if s.lower() in [x.lower() for x in required_skills]
            ]

            missing = [
                s for s in required_skills
                if s.lower() not in [x.lower() for x in candidate_skills]
            ]

            candidates.append({

                "Candidate": profile.get("candidate_name", ""),
                "Score": python_score,
                "Matched Skills": matched,
                "Missing Skills": missing,
                "Education": profile.get("education", ""),
                "Experience": profile.get("experience", ""),
                "Decision": ai["interview_decision"],
                "Fit": ai["fit_level"]

            })

        except Exception as e:
            print("Resume Error:", e)

    # --------------------------
    # Sort Candidates
    # --------------------------
    candidates = sorted(
        candidates,
        key=lambda x: x["Score"],
        reverse=True
    )

    # --------------------------
    # Ranking Table
    # --------------------------
    ranking = []

    medals = ["🥇", "🥈", "🥉"]

    for i, c in enumerate(candidates):

        rank = medals[i] if i < 3 else str(i + 1)

        ranking.append([
            rank,
            c["Candidate"],
            c["Score"],
            c["Decision"]
        ])

    ranking_df = pd.DataFrame(
        ranking,
        columns=[
            "Rank",
            "Candidate",
            "Score",
            "Decision"
        ]
    )

    # --------------------------
    # Dashboard
    # --------------------------
    total = len(candidates)

    shortlisted = sum(
        x["Decision"].lower() == "shortlist"
        for x in candidates
    )

    hold = sum(
        x["Decision"].lower() == "hold"
        for x in candidates
    )

    rejected = total - shortlisted - hold

    highest = candidates[0]["Score"] if total else 0

    # --------------------------
    # Charts
    # --------------------------
    chart_path = None
    pie_chart_path = None

    if total > 0:

        # Bar Chart
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

        # Pie Chart
        pie_chart_path = "charts/candidate_status.png"

        plt.figure(figsize=(5, 5))

        plt.pie(
            [shortlisted, hold, rejected],
            labels=["Shortlisted", "Hold", "Rejected"],
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("    Candidate Status Distribution")

        plt.savefig(
            pie_chart_path,
            bbox_inches="tight"
        )

        plt.close()
            # --------------------------
    # Candidate Card
    # --------------------------
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

    # --------------------------
    # Return Outputs
    # --------------------------
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
        pie_chart_path
    )

import gradio as gr

with gr.Blocks(
    title="RecruitAI - Intelligent Recruitment Assistant"
) as demo:

    # ==========================
    # Header
    # ==========================

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

    # ==========================
    # Upload Section
    # ==========================

    gr.Markdown("## 📂 Upload Documents")

    with gr.Row():

        jd_file = gr.File(
            label="📄 Job Description (.txt)",
            file_types=[".txt"]
        )

        resume_files = gr.File(
            label="📑 Candidate Resumes (.pdf)",
            file_types=[".pdf"],
            file_count="multiple"
        )

    evaluate_btn = gr.Button(
        "🚀 Evaluate Candidates",
        variant="primary",
        size="lg"
    )

    gr.Markdown("---")

    # ==========================
    # Dashboard
    # ==========================

    gr.Markdown("""
# 📊 Recruitment Dashboard

### AI Powered Hiring Analytics
""")

    with gr.Row():

        total_candidates = gr.Number(
            label="👥 Total Candidates",
            interactive=False
        )

        shortlisted = gr.Number(
            label="🟢 Shortlisted",
            interactive=False
        )

        hold = gr.Number(
            label="🟡 Hold",
            interactive=False
        )

        rejected = gr.Number(
            label="🔴 Rejected",
            interactive=False
        )

        highest_score = gr.Number(
            label="🏆 Highest Score",
            interactive=False
        )

    gr.Markdown("---")

    # ==========================
    # Ranking Table
    # ==========================

    gr.Markdown("## 🏅 Candidate Ranking")

    results_table = gr.Dataframe(
        headers=[
            "Rank",
            "Candidate",
            "Score",
            "Decision"
        ],
        interactive=False,
        wrap=True
    )

    gr.Markdown("---")

    # ==========================
    # Candidate Details
    # ==========================

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

    # ==========================
    # Analytics
    # ==========================

    gr.Markdown("# 📈 Candidate Analytics")

    with gr.Row():

        score_chart = gr.Image(
            label="📊 Candidate Score Comparison",
            type="filepath",
            interactive=False
        )

        pie_chart = gr.Image(
            label="🥧    Candidate Status Distribution",
            type="filepath",
            interactive=False
        )

    # ==========================
    # Button Action
    # ==========================

    evaluate_btn.click(
        fn=evaluate_pipeline,
        inputs=[
            jd_file,
            resume_files
        ],
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
            pie_chart
        ]
    )

if __name__ == '__main__':
    demo.launch(server_name='0.0.0.0', server_port=7860)

