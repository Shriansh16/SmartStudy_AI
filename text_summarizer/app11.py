import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
#from fpdf import FPDF
import io

#api_key=st.secrets["GROQ_API_KEY"]
api_key=st.secrets["GROQ_API_KEY"]
original_init = ChatGroq.__init__

def patched_client_init(self, *args, **kwargs):
    # Remove the proxies argument
    kwargs.pop('proxies', None)
    
    # Call the original __init__ method
    original_init(self, *args, **kwargs)

ChatGroq.__init__ = patched_client_init
llm=ChatGroq(groq_api_key=api_key,model="llama-3.1-70b-versatile",temperature=0.5)


st.title("PDF SmartNotes")
st.subheader("Upload your PDFs and get summarized, exam-ready notes instantly")
uploaded_files = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)

# Process uploaded PDFs
if st.button('Submit'):
 if uploaded_files:
    documents = []
    for uploaded_file in uploaded_files:
        temppdf = f"./temp_{uploaded_file.name}"  # Create a unique file for each upload
        with open(temppdf, "wb") as file:
            file.write(uploaded_file.getvalue())

        loader = PyPDFLoader(temppdf)
        docs = loader.load()
        documents.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    splits = text_splitter.split_documents(documents)
    #st.write(splits)

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
    st.write(output)