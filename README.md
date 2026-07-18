# 🤖 RecruitAI – Intelligent Recruitment Assistant

**Live Demo:** https://recruitai-intelligent-recruitment.onrender.com/

## 📌 Project Overview

RecruitAI is an AI-powered recruitment assistant that automates the initial candidate screening process by comparing resumes against a job description using Large Language Models (LLMs).

The application analyzes candidate resumes, extracts relevant skills and experience, compares them with the job requirements, calculates a matching score, ranks candidates, and provides AI-generated hiring recommendations.

This project reduces manual screening effort and helps recruiters identify the most suitable candidates faster.

---

# 🚩 Problem Statement

Recruiters receive hundreds of resumes for every job opening.

Traditional resume screening involves:

- Reading each resume manually
- Comparing candidate skills with the Job Description
- Identifying missing skills
- Ranking candidates
- Deciding whom to shortlist

This process is:

- Time-consuming
- Repetitive
- Prone to human bias
- Difficult when handling large volumes of applications

Organizations require an intelligent system that can automatically evaluate resumes and provide consistent candidate rankings.

---

# 💡 Solution

RecruitAI automates resume screening using AI.

The application:

- Accepts a Job Description
- Accepts multiple candidate resumes
- Extracts structured information using Groq LLM
- Compares candidate skills with required skills
- Calculates a match score
- Identifies matched and missing skills
- Ranks candidates
- Generates AI-based hiring recommendations

This enables recruiters to make faster and more informed hiring decisions.

---

# 🎯 Objectives

- Reduce manual resume screening time
- Improve recruitment efficiency
- Rank candidates objectively
- Identify skill gaps automatically
- Assist recruiters with AI-powered recommendations

---

# ⚙️ Features

✅ Upload Job Description

✅ Upload Multiple Resumes

✅ AI Resume Parsing

✅ AI Job Description Analysis

✅ Skill Matching

✅ Match Percentage Calculation

✅ Missing Skills Detection

✅ Candidate Ranking

✅ Hiring Recommendation

✅ Interactive Gradio Web Interface

---

# 🏗️ System Workflow

```
Job Description
        │
        ▼
Extract Required Skills
        │
        ▼
Upload Candidate Resumes
        │
        ▼
Resume Parsing using Groq LLM
        │
        ▼
Skill Comparison
        │
        ▼
Score Calculation
        │
        ▼
Candidate Ranking
        │
        ▼
AI Recommendation
```

---

# 🧠 Tech Stack

## Programming Language

- Python

## AI Model

- Groq LLM (llama-3.3-70b-versatile)

## Framework

- Gradio

## Libraries

- Pandas
- PyMuPDF (fitz) — PDF text extraction
- Matplotlib — score and status charts

---

# 📂 Project Structure

```
RecruitAI-Intelligent-Recruitment-Assistant/

│
├── app.py
├── requirements.txt
├── Agentic_Recruitment_Assistant.ipynb
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Priya2523/RecruitAI-Intelligent-Recruitment-Assistant.git
```

Go to the project folder

```bash
cd RecruitAI-Intelligent-Recruitment-Assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create an environment variable

```
GROQ_API_KEY=your_api_key
```

Run the application

```bash
python app.py
```

---

# 🌐 Live Demo

https://recruitai-intelligent-recruitment.onrender.com/

---

# 📊 Output

The application generates:

- Candidate Match Score
- Skill Match Analysis
- Missing Skills
- Candidate Ranking
- AI Recommendation
- Overall Hiring Decision

---

# 💼 Business Impact

RecruitAI helps organizations:

- Reduce resume screening time significantly
- Improve recruiter productivity
- Standardize candidate evaluation
- Reduce manual effort
- Improve hiring quality through AI-assisted recommendations

---

# 🔮 Future Enhancements

- ATS Integration
- LinkedIn Profile Analysis
- Interview Question Generation
- Candidate Email Automation
- Recruiter Dashboard
- Resume Database Search
- Multi-language Resume Support
- Advanced Analytics Dashboard

---

# 👩‍💻 Developer

**Priya A**

PGDM (AI & Data Science)

GitHub:
https://github.com/Priya2523

---
