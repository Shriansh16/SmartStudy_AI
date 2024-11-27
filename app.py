import streamlit as st
import runpy

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Page 1", "Page 2", "Page 3"])

    if page == "Documents Summarizer (prepare notes)":
        document_summarizer()
    elif page == "Chat with your PDFs":
        chat_with_pdf()
    elif page == "Match your Resume with job description":
        resume_checker()
    elif page == "Website Content Summarizer (prepare notes)":
        website_summarizer()
    elif page == "Youtube video summarizer (Prepare notes)":
        youtube_summarizer()

def document_summarizer():
    runpy.run_path('text_summarizer/app11.py')

def chat_with_pdf():
    runpy.run_path('chat_with_pdf/chat_with_pdf.py')

def youtube_summarizer():
    runpy.run_path('youtube_video_summarizer/app.py')

def resume_checker():
    runpy.run_path('Resume_ATS_tracker/resume_analyser.py')

def website_summarizer():
    runpy.run_path('website_text_summarizer/app.py')


if __name__ == "__main__":
    main()