import os
import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader
import bs4
from dotenv import load_dotenv

load_dotenv()

## Streamlit APP
st.set_page_config(page_title="LangChain: Summarize Text From Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From Website or YouTube")
st.subheader('Summarize URL')

generic_url = st.text_input("Enter the URL (Website or YouTube)", label_visibility="collapsed")

# Groq Model Using API
llm = ChatGroq(model="Gemma-7b-It", groq_api_key=os.getenv("GROQ_API_KEY"))

prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarize the Content"):
    # Validate all the inputs
    if not validators.url(generic_url):
        st.error("Please enter a valid URL. Supported sources include website URLs and YouTube video URLs.")
    else:
        try:
            # Ensure the URL has a scheme (http:// or https://)
            if not generic_url.startswith(('http://', 'https://')):
                generic_url = 'https://' + generic_url

            with st.spinner("Processing..."):
                # Load content from the URL
                loader = WebBaseLoader(web_paths=(generic_url),
                     bs_kwargs=dict(parse_only=bs4.SoupStrainer(
                         class_=("post-title", "post-content", "post-header")
                     ))
                )
                docs = loader.load()

                if not docs:
                    st.warning("No readable content was found on the page.")
                else:
                    # Chain for summarization
                    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                    output_summary = chain.run(docs)
                    st.success(output_summary)

        except Exception as e:
            st.error("An error occurred while processing the request. Please try again later.")
            # Log the detailed error if needed for debugging
            st.error(f"Details: {e}")
