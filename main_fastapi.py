from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from typing import List
import shutil

from app.llm_client import generate_text
from app.parse_utils import extract_text_from_file
from app.scoring import score_candidate_with_gemini
from app.email_generator import generate_candidate_emails

app = FastAPI(title="Recruitment AI Agent")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Home page: Upload JD & resumes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Form submission route
@app.post("/evaluate", response_class=HTMLResponse)
async def evaluate(
    request: Request,
    jd_file: UploadFile = File(None),
    jd_text: str = Form(""),
    generate_jd: str = Form(None),
    job_title: str = Form(""),
    years_of_experience: str = Form(""),
    must_have_skills: str = Form(""),
    company_name: str = Form(""),
    employment_type: str = Form(""),
    industry: str = Form(""),
    location: str = Form(""),
    resumes: List[UploadFile] = File(None)
):
    # Step 1: Prepare Job Description
    if jd_file:
        jd_text = await extract_text_from_file(jd_file)
    elif generate_jd:
        prompt = f"""
Generate a professional job description with title '{job_title}', 
experience '{years_of_experience}', skills '{must_have_skills}', 
company '{company_name}', employment type '{employment_type}', 
industry '{industry}', location '{location}'.
"""
        jd_text = generate_text(prompt)
    
    # Step 2: Process resumes
    candidates = []
    for resume_file in resumes:
        resume_path = UPLOAD_DIR / resume_file.filename
        with open(resume_path, "wb") as f:
            shutil.copyfileobj(resume_file.file, f)
        resume_text = await extract_text_from_file(resume_file)

        skills_list = [s.strip() for s in must_have_skills.split(",") if s.strip()]

        # Step 3: Score & Missing skills
        score_result = score_candidate_with_gemini(jd_text, resume_text, skills_list)
        score = score_result["score"]
        missing_skills = score_result["missing_skills"]
        remark = score_result["remark"]

        # Step 4: Generate emails
        emails = generate_candidate_emails(jd_text, resume_text, score, missing_skills)

        candidates.append({
            "filename": resume_file.filename,
            "score": score,
            "missing_skills": missing_skills,
            "remark": remark,
            "interview_email": emails["interview_email"],
            "rejection_email": emails["rejection_email"]
        })

    # Step 5: Highlight top candidate
    top_score = max([c["score"] for c in candidates], default=0)
    for c in candidates:
        c["is_top"] = c["score"] == top_score

    return templates.TemplateResponse("results.html", {
        "request": request,
        "candidates": candidates,
        "jd_text": jd_text
    })
