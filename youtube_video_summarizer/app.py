from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage
load_dotenv()   
import os
api_key=os.getenv("GROQ_API_KEY")
llm=ChatGroq(groq_api_key=api_key,model="llama-3.1-70b-versatile",temperature=0.5)


def extract_transcript_details(youtube_video_url):
    try:
        # Extract the video ID properly, handling different URL formats
        parsed_url = urlparse(youtube_video_url)
        video_id = parse_qs(parsed_url.query).get("v", [None])[0]
        
        if not video_id:
              
            video_id = parsed_url.path.split('/')[-1]

        # Get the transcript
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        print("Can't do for this video, please try for another video")
def generate_response(transcript_text):
    messages=[
    SystemMessage(content="Provide comprehensive and detailed notes based on the given document, focusing on key concepts, explanations, and examples. The notes should help college students not only understand the topics thoroughly but also prepare effectively for their exams. Ensure the content is organized, with clear headings, subheadings, bullet points, and concise explanations where necessary."),
    HumanMessage(content=f"document: {transcript_text}")
     ]
    response=llm.invoke(messages)
    return response.content

st.title("YouTube Study Notes Generator")
st.subheader("Effortlessly Generate Comprehensive Summarized Notes from YouTube Videos. Paste the Video Link Below to Get Started")
youtube_link=st.text_input("Paste the Youtube Video url")
submit = st.button("Submit")
if submit:
    if youtube_link:
        # Proceed only if the YouTube link is provided
        try:
            text = extract_transcript_details(youtube_link)
            summary = generate_response(text)
            st.markdown("## Detailed Notes:")
            st.write(summary)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        # Show an error message if no link is provided
        st.error("Please paste a valid YouTube video URL to generate notes.")
    
