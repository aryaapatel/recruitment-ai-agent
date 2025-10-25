# app/email_generator.py
from app.llm_client import generate_text
import json, re

def generate_candidate_emails(jd_text: str, resume_text: str, score: float, missing_skills: list[str]):
    prompt = f"""
You are an HR assistant generating candidate emails. 

Job Description:
{jd_text}

Candidate Resume:
{resume_text}

Matching Score: {score}
Missing Skills: {', '.join(missing_skills)}

Tasks:
1. If score >= 70, generate a personalized interview call email.
2. If score < 70, generate a rejection email.
3. Provide a short remark summarizing candidate fit.

Respond ONLY in JSON format like:
{{"interview_email": "", "rejection_email": ""}}
"""
    response = generate_text(prompt)
    # try:
    #     result = json.loads(response)
    #     return {
    #         "interview_email": result.get("interview_email", ""),
    #         "rejection_email": result.get("rejection_email", "")
    #     }
    # except Exception:
    #     # fallback if Gemini returned non-JSON
    #     return {"interview_email": "", "rejection_email": response}
    try:
        # Use regex to find the JSON block, even if it's wrapped in other text
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            json_str = match.group(0)
            result = json.loads(json_str)
            return {
                "interview_email": result.get("interview_email", ""),
                "rejection_email": result.get("rejection_email", "")
            }
        else:
            # If no JSON is found, put the raw response in one of the email fields for debugging
            return {"interview_email": "", "rejection_email": f"Failed to parse JSON from AI: {response}"}

    except json.JSONDecodeError:
         # Fallback if the extracted string is still not valid JSON
        return {"interview_email": "", "rejection_email": f"Invalid JSON received from AI: {response}"}