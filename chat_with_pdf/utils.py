from dotenv import load_dotenv
import os
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from openai import OpenAI
from langchain.document_loaders import PyPDFLoader
load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")


def query_refiner(conversation, query):
  client = OpenAI(api_key=KEY)  
  chat_service = client.chat  
  response = chat_service.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "If the user's query is unrelated to the conversation context, return it as is. Otherwise, refine the query in under 20 words."},
          {"role": "user", "content": f"Given the conversation log:\n{conversation}\n\nand the query:\n{query}\n\nDetermine if the query is relevant. If yes, refine it; if not, return it as is. Provide only the refined question, without any additional text."}
      ],
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
  )
  return response.choices[0].message.content
def get_conversation_string():
    conversation_string = ""
    start_index = max(len(st.session_state['responses']) - 2, 0)
    for i in range(start_index, len(st.session_state['responses']) - 1):        
        conversation_string += "Human: " + st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: " + st.session_state['responses'][i+1] + "\n"
    return conversation_string

