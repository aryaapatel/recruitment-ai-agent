# import streamlit as st
# import pandas as pd
# import io

# # Import the same core logic functions
# from app.llm_client import generate_text
# from app.parse_utils import extract_text_from_file
# from app.scoring import score_candidate_with_gemini
# from app.email_generator import generate_candidate_emails

# st.set_page_config(layout="wide")
# st.title("🤖 Recruitment AI Agent")

# # --- 1. JOB DESCRIPTION INPUT ---
# st.header("1. Provide the Job Description")
# jd_option = st.radio("Choose JD Source:", ("Upload File", "Generate New JD"), horizontal=True)

# jd_text = ""
# must_have_skills = ""

# if jd_option == "Upload File":
#     jd_file = st.file_uploader("Upload Job Description (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
#     if jd_file:
#         jd_text = extract_text_from_file(jd_file, jd_file.name)
#     # A field to manually input skills is still useful when using an uploaded JD
#     must_have_skills = st.text_input("Enter Must-Have Skills (comma-separated)", placeholder="e.g., Python, FastAPI, Streamlit")

# else: # Generate New JD
#     st.subheader("Generate a New Job Description")
#     col1, col2 = st.columns(2)
#     with col1:
#         job_title = st.text_input("Job Title")
#         company_name = st.text_input("Company Name")
#         location = st.text_input("Location")
#     with col2:
#         employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract"])
#         years_of_experience = st.text_input("Years of Experience")
#         industry = st.text_input("Industry")
    
#     must_have_skills = st.text_input("Must-Have Skills (comma-separated)", placeholder="e.g., Python, FastAPI, Streamlit")
    
#     if st.button("✨ Generate JD"):
#         if all([job_title, years_of_experience, must_have_skills]):
#             with st.spinner("Generating Job Description..."):
#                 prompt = f"""
# Generate a professional job description with title '{job_title}', 
# experience '{years_of_experience}', skills '{must_have_skills}', 
# company '{company_name}', employment type '{employment_type}', 
# industry '{industry}', location '{location}'.
# """
#                 jd_text = generate_text(prompt)
#         else:
#             st.warning("Please fill in at least Job Title, Experience, and Skills.")

# if jd_text:
#     with st.expander("View Job Description", expanded=True):
#         st.text_area(label="", value=jd_text, height=200)

# # --- 2. RESUME UPLOAD ---
# st.header("2. Upload Candidate Resumes")
# resume_files = st.file_uploader(
#     "Upload one or more resumes (PDF, DOCX, TXT)", 
#     type=["pdf", "docx", "txt"], 
#     accept_multiple_files=True
# )

# # --- 3. EVALUATION ---
# if st.button("🚀 Evaluate Candidates", type="primary", use_container_width=True, disabled=(not jd_text or not resume_files)):
#     with st.spinner("AI is evaluating candidates... This may take a moment."):
#         candidates = []
#         for resume_file in resume_files:
#             # Streamlit's UploadedFile is already a file-like object
#             resume_text = extract_text_from_file(resume_file, resume_file.name)
            
#             skills_list = [s.strip() for s in must_have_skills.split(",") if s.strip()]

#             # Call core logic for scoring
#             score_result = score_candidate_with_gemini(jd_text, resume_text, skills_list)
#             print(score_result,"######################")
#             score = score_result.get("score", 0)
            
#             # Call core logic for email generation
#             emails = generate_candidate_emails(jd_text, resume_text, score, score_result.get("missing_skills", []))
#             print(emails,"***********************************")

#             candidates.append({
#                 "Filename": resume_file.name,
#                 "Score": score,
#                 "Remark": score_result.get("remark", "N/A"),
#                 "Missing Skills": ", ".join(score_result.get("missing_skills", [])),
#                 "Interview Email": emails.get("interview_email", ""),
#                 "Rejection Email": emails.get("rejection_email", "")
#             })

#         if candidates:
#             st.header("🏆 Evaluation Results")
            
#             # Find top candidate
#             top_score = max(c["Score"] for c in candidates if c["Score"] is not None)
            
#             df = pd.DataFrame(candidates)
            
#             def highlight_top(row):
#                 return ['background-color: #d4edda' if row.Score == top_score else '' for _ in row]

#             st.dataframe(df.style.apply(highlight_top, axis=1), use_container_width=True)
            
#             # Display emails in expanders
#             st.header("✉️ Generated Emails")
#             for _, row in df.iterrows():
#                 with st.expander(f"Emails for {row['Filename']} (Score: {row['Score']})"):
#                     if row['Score'] >= 70 and row['Interview Email']:
#                         st.subheader("Interview Invitation")
#                         st.code(row['Interview Email'])
#                     elif row['Rejection Email']:
#                         st.subheader("Rejection Email")
#                         st.code(row['Rejection Email'])

#         else:
#             st.error("Could not process any candidates.")
import streamlit as st
import pandas as pd
import io

# Import the same core logic functions
from app.llm_client import generate_text
from app.parse_utils import extract_text_from_file
from app.scoring import score_candidate_with_gemini
from app.email_generator import generate_candidate_emails

st.set_page_config(layout="wide")
st.title("🤖 Recruitment AI Agent")

# --- Initialize session_state ---
# This is the key! It ensures our variables persist across reruns.
if 'jd_text' not in st.session_state:
    st.session_state.jd_text = ""
if 'must_have_skills' not in st.session_state:
    st.session_state.must_have_skills = ""


# --- 1. JOB DESCRIPTION INPUT ---
st.header("1. Provide the Job Description")
jd_option = st.radio("Choose JD Source:", ("Upload File", "Generate New JD"), horizontal=True)

if jd_option == "Upload File":
    jd_file = st.file_uploader("Upload Job Description (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    if jd_file:
        # Store the extracted text in session_state
        st.session_state.jd_text = extract_text_from_file(jd_file, jd_file.name)
    
    # Use a different key for the text_input to avoid conflicts
    st.session_state.must_have_skills = st.text_input(
        "Enter Must-Have Skills (comma-separated)", 
        value=st.session_state.must_have_skills, # Read its previous value
        placeholder="e.g., Python, FastAPI, Streamlit"
    )

else: # Generate New JD
    st.subheader("Generate a New Job Description")
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("Job Title")
        company_name = st.text_input("Company Name")
        location = st.text_input("Location")
    with col2:
        employment_type = st.selectbox("Employment Type", ["Full-time", "Part-time", "Contract"])
        years_of_experience = st.text_input("Years of Experience")
        industry = st.text_input("Industry")
    
    st.session_state.must_have_skills = st.text_input(
        "Must-Have Skills (comma-separated)", 
        value=st.session_state.must_have_skills, # Read its previous value
        placeholder="e.g., Python, FastAPI, Streamlit"
    )
    
    if st.button("✨ Generate JD"):
        if all([job_title, years_of_experience, st.session_state.must_have_skills]):
            with st.spinner("Generating Job Description..."):
                prompt = f"""
Generate a professional job description with title '{job_title}', 
experience '{years_of_experience}', skills '{st.session_state.must_have_skills}', 
company '{company_name}', employment type '{employment_type}', 
industry '{industry}', location '{location}'.
"""
                # Store the generated text in session_state
                st.session_state.jd_text = generate_text(prompt)
        else:
            st.warning("Please fill in at least Job Title, Experience, and Skills.")

# ALWAYS read from session_state to display the JD
if st.session_state.jd_text:
    with st.expander("View Job Description", expanded=True):
        st.text_area(
            label="Job Description Preview", 
            value=st.session_state.jd_text, 
            height=200, 
            label_visibility="collapsed"
        )

# --- 2. RESUME UPLOAD ---
st.header("2. Upload Candidate Resumes")
resume_files = st.file_uploader(
    "Upload one or more resumes (PDF, DOCX, TXT)", 
    type=["pdf", "docx", "txt"], 
    accept_multiple_files=True
)

# --- 3. EVALUATION ---
# ALWAYS read from session_state for the disabled check
if st.button("🚀 Evaluate Candidates", type="primary", use_container_width=True, disabled=(not st.session_state.jd_text or not resume_files)):
    with st.spinner("AI is evaluating candidates... This may take a moment."):
        candidates = []
        # Use the skills from session_state
        skills_list = [s.strip() for s in st.session_state.must_have_skills.split(",") if s.strip()]
        
        for resume_file in resume_files:
            resume_text = extract_text_from_file(resume_file, resume_file.name)
            
            # Use the JD from session_state for the backend calls
            jd = st.session_state.jd_text
            score_result = score_candidate_with_gemini(jd, resume_text, skills_list)
            score = score_result.get("score", 0)
            emails = generate_candidate_emails(jd, resume_text, score, score_result.get("missing_skills", []))

            candidates.append({
                "Filename": resume_file.name,
                "Score": score,
                "Remark": score_result.get("remark", "N/A"),
                "Missing Skills": ", ".join(score_result.get("missing_skills", [])),
                "Interview Email": emails.get("interview_email", ""),
                "Rejection Email": emails.get("rejection_email", "")
            })

        if candidates:
            st.header("🏆 Evaluation Results")
            if not pd.DataFrame(candidates)["Score"].empty and pd.DataFrame(candidates)["Score"].notna().any():
                top_score = pd.DataFrame(candidates)["Score"].max()
                def highlight_top(row):
                    return ['background-color: #d4edda' if row.Score == top_score else '' for _ in row]
                st.dataframe(pd.DataFrame(candidates).style.apply(highlight_top, axis=1), use_container_width=True)
            else:
                 st.dataframe(pd.DataFrame(candidates), use_container_width=True)
            
            st.header("✉️ Generated Emails")
            for _, row in pd.DataFrame(candidates).iterrows():
                with st.expander(f"Emails for {row['Filename']} (Score: {row['Score']})"):
                    if row['Score'] is not None and row['Score'] >= 70 and row['Interview Email']:
                        st.subheader("Interview Invitation")
                        st.code(row['Interview Email'])
                    elif row['Rejection Email']:
                        st.subheader("Rejection Email")
                        st.code(row['Rejection Email'])
        else:
            st.error("Could not process any candidates.")