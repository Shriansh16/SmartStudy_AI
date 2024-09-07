import os
import streamlit as st
import PyPDF2 as pdf
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": input}] ,
    n=1
    )
    
    return response.choices[0].message.content
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
input_prompt_template = """
You are an expert in resume optimization for Applicant Tracking Systems (ATS). Given the following inputs:

Resume: {text}
Job Description: {jd}
Your tasks are as follows:

Calculate the ATS score by analyzing how well the resume matches the job description based on relevant keywords, skills, and experience.

Suggest specific improvements to enhance the ATS score, including:

Keywords to add or modify
Skills to highlight
Adjustments to work experience and formatting
Return the ATS score along with clear and actionable suggestions that will help tailor the resume to better align with the job description.
"""

input_prompt_template1 = """
Hey, act as a highly advanced ATS (Applicant Tracking System) with expert knowledge across all IT domains, including but not limited to software engineering, data science, data analysis, big data engineering, cybersecurity, cloud computing, DevOps, AI/ML, and more. Your task is to evaluate the provided resume based on the given job description. The job market is highly competitive, so provide the best possible assistance to improve the resume. Assess the percentage match based on the job description, identify any missing skills, and provide a summary of the resume profile. Also, offer recommendations for improving the resume, including skill enhancements, experience relevance, and keyword optimization. Ensure high accuracy in the analysis.

Resume: {text}
Job Description: {jd}

Respond with the evaluation in bullet points as follows:
- **Job Description Match:** %
- **Missing Skills:** [list of missing skills]
- **Profile Summary:** [summary of the resume profile]
- **Recommended Improvements:** [specific suggestions for enhancing the resume]
- **Skill Proficiency Assessment:** [evaluation of listed skills]
- **Experience Relevance:** [feedback on relevance of listed experience]
- **Achievements and Metrics:** [suggestions for including achievements or metrics]
- **Keywords Optimization:** [list of recommended keywords or phrases]
- **Resume Formatting Suggestions:** [advice on formatting improvements]

"""

## streamlit app
st.title("ATS-Powered Resume Analyzer")
jd = st.text_area("Paste the Job Description")  
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd.strip():
        resume_text = input_pdf_text(uploaded_file)
        st.write(resume_text)
        input_prompt = input_prompt_template.format(text=resume_text, jd=jd)
        response = get_response(input_prompt)
        st.write(response)