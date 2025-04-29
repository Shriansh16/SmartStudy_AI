from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage,SystemMessage
from langchain.schema import Document  
import os
api_key=st.secrets["GROQ_API_KEY"]

llm=ChatGroq(groq_api_key=api_key,model="llama-3.3-70b-versatile",temperature=0.5)


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
        #st.write(transcript)

        return transcript

    except Exception as e:
        print("Can't do for this video, please try for another video")
def generate_response(transcript_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    
    # Wrap transcript in a Document object
    document = Document(page_content=transcript_text)
    
    # Split the document
    splits = text_splitter.split_documents([document])
    
    # Debugging: Uncomment to see splits
    # st.write(splits)

    chunks_prompt = """
    Please summarize the below text:
    Text: "{text}"
    Summary:
    """

    map_prompt_template = PromptTemplate(input_variables=['text'], template=chunks_prompt)

    final_prompt = '''
    Provide comprehensive and detailed notes based on the given documents, focusing on key concepts, explanations, and examples. The notes should help college students not only understand the topics thoroughly but also prepare effectively for their exams. Ensure the content is organized, with clear headings, subheadings, bullet points, and concise explanations where necessary.
    Documents: {text}
    '''

    final_prompt_template = PromptTemplate(input_variables=['text'], template=final_prompt)

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        map_prompt=map_prompt_template,
        combine_prompt=final_prompt_template,
        verbose=True
    )

    output = summary_chain.run(splits)
    return output

st.title("YouTube Study Notes Generator")
st.subheader("Effortlessly Generate Comprehensive Summarized Notes from YouTube Videos. Paste the Video Link Below to Get Started")
youtube_link=st.text_input("Paste the Youtube Video url")
submit = st.button("Submit")
if submit:
  with st.spinner("Processing..."):
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