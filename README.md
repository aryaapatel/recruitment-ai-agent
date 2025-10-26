# Recruitment AI Agent 🤖

This project is a powerful, AI-driven tool designed to streamline the initial stages of the recruitment process. It leverages the Google Gemini API to automatically parse, score, and evaluate candidate resumes against a given job description.

The application features two distinct interfaces:
1.  An interactive web application built with **Streamlit** for easy, visual use.
2.  A robust REST API built with **FastAPI** for programmatic integration.

![Screenshot of the Recruitment AI Agent Streamlit UI]
!https://www.canva.com/design/DAG2zmlG0Eo/7jGqpYqE5Qfxl05RjCqtWA/view?utm_content=DAG2zmlG0Eo&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h4f74195fea

> https://www.veed.io/view/bee1d1aa-4d0e-4820-87da-d62c22a3fc91?panel=share


## ✨ Features

-   **Dual Job Description Input**: Upload an existing Job Description (PDF, DOCX, TXT) or generate a new one on-the-fly by providing key details.
-   **Bulk Resume Processing**: Upload multiple candidate resumes at once for evaluation.
-   **AI-Powered Scoring**: Each resume is scored out of 100 based on its relevance to the job description, using the Gemini API.
-   **Skills Gap Analysis**: The AI identifies which "must-have" skills are missing from each candidate's resume.
-   **Automated Email Generation**: For each candidate, the application generates personalized interview invitation and rejection emails based on their score.
-   **Top Candidate Highlighting**: The candidate with the highest score is visually highlighted in the results table.
-   **Flexible Deployment**: Run as an easy-to-use Streamlit web app or as a scalable FastAPI backend.

## 🛠️ Tech Stack

-   **Backend & Logic**: Python
-   **AI Model**: Google Gemini Pro
-   **Web App Interface**: Streamlit
-   **API Interface**: FastAPI, Uvicorn
-   **Data Handling**: Pandas
-   **File Parsing**: PyPDF2, python-docx

## 📁 Project Structure
recruitment-agent/
├── app/
│ ├── init.py
│ ├── email_generator.py # Logic for generating emails
│ ├── llm_client.py # Handles communication with Gemini API
│ ├── parse_utils.py # Extracts text from PDF, DOCX, TXT files
│ └── scoring.py # Logic for scoring candidates
├── main_fastapi.py # Entry point for the FastAPI application
├── main_streamlit.py # Entry point for the Streamlit application
├── requirements.txt # List of Python dependencies
├── .env # File for storing secret API keys
└── README.md # This file
code
Code
## ⚙️ Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/recruitment-agent.git
cd recruitment-agent

2. Create a Virtual Environment

# For Linux/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Install all the necessary Python libraries from the requirements.txt file.

pip install -r requirements.txt

4. Set Up Environment Variables

The application requires a Google Gemini API key to function.
1. Create a file named .env in the root of the project directory.
2. Add your API key to this file as follows:

LLM_API_KEY="YOUR_GOOGLE_GEMINI_API_KEY"

You can get your API key from the Google AI Studio.

🚀 How to Run
You can run this project in two different modes. Make sure you are in the project's root directory (recruitment-agent/) before running the commands.

1. Running with Streamlit (Interactive Web App)
This is the recommended way for direct use.

streamlit run main_streamlit.py

Your web browser should automatically open with the application running at http://localhost:8501.

2. Running with FastAPI (API Server)
This is ideal for backend or programmatic use.

uvicorn main_fastapi:app --reload

The API will be running at http://127.0.0.1:8000. You can access the interactive API documentation (powered by Swagger UI) at http://127.0.0.1:8000/docs.


