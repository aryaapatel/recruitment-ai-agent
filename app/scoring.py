# app/scoring.py
from app.llm_client import generate_text
import json, re

def score_candidate_with_gemini(jd_text: str, resume_text: str, must_have_skills: list[str]):
    prompt = f"""
You are an HR assistant evaluating a candidate for a job. 

Job Description:
{jd_text}

Candidate Resume:
{resume_text}

Must-have Skills: {', '.join(must_have_skills)}

Tasks:
1. Give a score out of 100 indicating the candidate's suitability.
2. List any missing must-have skills.
3. Provide a brief remark explaining the score.

Respond ONLY in JSON format like:
{{"score": 0, "missing_skills": [], "remark": ""}}
"""
    # response = generate_text(prompt)
    # try:
    #     result = json.loads(response)
    #     return {
    #         "score": result.get("score"),
    #         "missing_skills": result.get("missing_skills", []),
    #         "remark": result.get("remark", "")
    #     }
    # except Exception:
    #     # fallback if Gemini returned non-JSON
    #     return {"score": None, "missing_skills": [], "remark": response}
    response = generate_text(prompt)
    try:
        # Clean the response string before parsing
        cleaned_response = re.sub(r'^```json\s*|\s*```$', '', response, flags=re.MULTILINE).strip()
        result = json.loads(cleaned_response)
        return {
            "score": result.get("score"),
            "missing_skills": result.get("missing_skills", []),
            "remark": result.get("remark", "")
        }
    except (json.JSONDecodeError, AttributeError):
        # fallback if Gemini returned non-JSON or cleaning failed
        return {"score": None, "missing_skills": [], "remark": response}