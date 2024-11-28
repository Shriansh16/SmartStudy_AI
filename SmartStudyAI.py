import streamlit as st
import runpy

def main():
    # Set the title and sidebar layout
    st.set_page_config(page_title="SmartStudyAI", layout="wide")
    st.title("Welcome to SmartStudyAI: Your AI-Powered Study Assistant")
    st.sidebar.title("Navigation")

    # Add attractive options to the sidebar with icons
    page = st.sidebar.radio("Choose an option:", 
                            ["📝 Documents Summarizer", 
                             "📚 Chat with Your PDFs", 
                             "🔍 Resume Checker", 
                             "🌐 Website Content Summarizer", 
                             "🎥 YouTube Video Summarizer"])

    # Navigate to the selected page
    if page == "📝 Documents Summarizer":
        document_summarizer()
    elif page == "📚 Chat with Your PDFs":
        chat_with_pdf()
    elif page == "🔍 Resume Checker":
        resume_checker()
    elif page == "🌐 Website Content Summarizer":
        website_summarizer()
    elif page == "🎥 YouTube Video Summarizer":
        youtube_summarizer()

def document_summarizer():
    """Runs the document summarizer app"""
    st.subheader("Document Summarizer: Prepare Notes")
    runpy.run_path('text_summarizer/app11.py')

def chat_with_pdf():
    """Runs the PDF chat app"""
    st.subheader("Chat with Your PDFs")
    runpy.run_path('chat_with_pdf/chat_with_pdf.py')

def youtube_summarizer():
    """Runs the YouTube video summarizer app"""
    st.subheader("YouTube Video Summarizer: Prepare Notes")
    runpy.run_path('youtube_video_summarizer/app.py')

def resume_checker():
    """Runs the resume checker app"""
    st.subheader("Resume ATS Matcher")
    runpy.run_path('Resume_ATS_tracker/resume_analyser.py')

def website_summarizer():
    """Runs the website content summarizer app"""
    st.subheader("Website Content Summarizer: Prepare Notes")
    runpy.run_path('website_text_summarizer/app.py')

if __name__ == "__main__":
    main()
