import os
import streamlit as st
import re
import faiss
from langchain.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from chat_with_pdf.utils import *
from langchain_groq import ChatGroq
api_key1=st.secrets["GROQ_API_KEY"]
embeddings=download_embeddings()
def patched_client_init(self, *args, proxies=None, **kwargs):
    """
    Patched __init__ method for langchain_groq.Client to accept the proxies argument.
    """
    # Call the original __init__ method without the proxies argument
    super(ChatGroq, self).__init__(*args, **kwargs)

ChatGroq.__init__ = patched_client_init
llm=ChatGroq(groq_api_key=api_key1,model_name="llama3-8b-8192",temperature=0.6)
st.title("Upload PDFs and Chat with Their Content")
uploaded_files = st.file_uploader("Choose a PDF file", type="pdf", accept_multiple_files=True)
## Process uploaded  PDF's
#if st.button('Submit'):
if uploaded_files:
    documents=[]
    for uploaded_file in uploaded_files:
        temppdf=f"./temp.pdf"
        with open(temppdf,"wb") as file:
            file.write(uploaded_file.getvalue())
            file_name=uploaded_file.name

        loader=PyPDFLoader(temppdf)
        docs=loader.load()
        documents.extend(docs)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    splits = text_splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    # Initialize session state variables
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["Greetings! Please feel free to ask any questions related to the uploaded document."]
    if 'requests' not in st.session_state:
        st.session_state['requests'] = []
    
    # Initialize conversation memory
    if 'buffer_memory' not in st.session_state:
        st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)
    # Define prompt templates
    system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer as a friendly helpdesk agent and use the provided context to build the answer and If the answer is not contained within the text, say 'I'm not sure about that, but I'm here to help with anything else you need!'. Do not say 'According to the provided context' or anything similar. Just give the answer naturally.""")                                                                        
    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
    # Create conversation chain
    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

    # Container for chat history
    response_container = st.container()
    # Container for text box
    text_container = st.container()
    with text_container:
        user_query =st.chat_input("Enter your query")

        if user_query:
            with st.spinner("typing..."):
               conversation_string = get_conversation_string()
               refined_query = query_refiner(conversation_string, user_query)
               refined_query = re.sub(r'(?i)refined query', '', refined_query)
               refined_query = re.sub(r'(?i)relevant', '', refined_query)
               refined_query = re.sub(r'(?i)irrelevant', '', refined_query)
               refined_query = re.sub(r'(?i)Refined question:', '', refined_query)
               #refined_query=refined_query+" "+user_query   
               #st.write(refined_query)
               #st.write(conversation_string)
               context = retriever.get_relevant_documents(refined_query,k=5)
               response = conversation.predict(input=f"Context:\n{context}\n\nQuery:\n{user_query}")



        
            # Append the new query and response to the session state  
            st.session_state.requests.append(user_query)
            st.session_state.responses.append(response)
    st.markdown(
      """
      <style>
      [data-testid="stChatMessageContent"] p{
          font-size: 1rem;
      }
      </style>
      """, unsafe_allow_html=True
     )


     # Display chat history
    with response_container:
      if st.session_state['responses']:
          for i in range(len(st.session_state['responses'])):
              with st.chat_message('Momos',avatar='icon.png'):
                  st.write(st.session_state['responses'][i])
              if i < len(st.session_state['requests']):
                  message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')