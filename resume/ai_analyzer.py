from groq import Groq
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 🔥 STEP 1: AI decides if input is job-related
def is_job_related(text):
    prompt = f"""
You are an intelligent classifier.

Your task is to decide whether the input is related to a JOB, CAREER, or ROLE.

ACCEPT (return YES):
- Job titles (Backend Developer, Data Scientist, GRC Analyst)
- Career domains (Cybersecurity, Data Science)
- Short valid job roles

REJECT (return NO):
- Random words (asdfghjkl)
- Common words (bus, smart, hello, talk)
- Meaningless text

Be slightly flexible — short job titles are VALID.

Return ONLY:
YES or NO

Input:
{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        answer = response.choices[0].message.content.strip().upper()
        return answer == "YES"

    except Exception as e:
        print("❌ Validation Error:", e)
        return False


# 🔥 STEP 2: Generate job description from job role
def generate_job_description(job_title):
    prompt = f"""
Generate a professional job description for the role: {job_title}.

Include:
- Required skills
- Responsibilities
- Tools/technologies

Return only plain text.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


# 🔥 STEP 3: MAIN FUNCTION
def analyze_resume_with_ai(text, job_desc=""):

    # ✅ Step 1: Validate input using AI
    if not is_job_related(job_desc):
        return """{
            "ats_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Please enter a valid job role or career-related input"]
        }"""

    # ✅ Step 2: If short → treat as job title
    if len(job_desc.strip()) < 30:
        job_desc = generate_job_description(job_desc)

    # 🔥 Step 3: ATS Analysis
    prompt = f"""
You are a STRICT ATS (Applicant Tracking System).

RULES:
- Return ONLY valid JSON (no explanation)
- If resume is irrelevant → give LOW score (<40)
- Do NOT guess skills
- Only use skills explicitly present in resume
- Only match skills present in BOTH resume and job description

INPUT:

Job Description:
{job_desc}

Resume:
{text}

OUTPUT (STRICT JSON ONLY):

{{
  "ats_score": number,
  "matched_skills": [],
  "missing_skills": [],
  "suggestions": []
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ GROQ ERROR:", str(e))

        return """{
            "ats_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["AI service error"]
        }"""