import os
import streamlit as st
import PyPDF2 as pdf
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage
api_key=st.secrets["GROQ_API_KEY"]



llm=ChatGroq(groq_api_key=api_key,model="llama-3.3-70b-versatile",temperature=0.5)

def get_response(input):
    messages=[{"role": "user", "content": input}]
    response=llm.invoke(messages)
    return response.content
def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template
input_prompt_template = """
You are an expert in resume analysis and Applicant Tracking Systems (ATS). Your task is to analyze a given resume and a job description, calculate the ATS score, and predict the likelihood of the resume being shortlisted for the job. Your analysis should include:

A breakdown of the ATS score, highlighting how well the resume aligns with the job description.
Identification of any loopholes or gaps in the resume, including missing skills, keywords, or experience that may decrease the chances of shortlisting.
Detailed suggestions for improving the resume to increase the chances of shortlisting, ensuring it aligns better with the job description.
A prediction of the percentage chances of getting shortlisted based on the resume's alignment with the job description.
Here is the resume: {text}
Here is the job description: {jd}
"""


## streamlit app
st.title("ATS-Powered Resume Analyzer")
jd = st.text_area("Paste the Job Description")  
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd.strip():
        resume_text = input_pdf_text(uploaded_file)
        #st.write(resume_text)
        #st.write(jd)
        input_prompt = input_prompt_template.format(text=resume_text, jd=jd)
        response = get_response(input_prompt)
        st.write(response)
