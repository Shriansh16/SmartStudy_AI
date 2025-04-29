import os
import streamlit as st
from openai import OpenAI
from langchain.document_loaders import PyPDFLoader
from groq import Groq


def query_refiner(conversation, query):
  #  if not conversation or not query:
   #     return query
    api_key1 = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key1)
    response = client.chat.completions.create(
    model="gemma2-9b-it",
     messages=[{"role": "system", "content": "If the user's query is unrelated to the conversation context, return it as is. Otherwise, refine the query in under 20 words."},
              {"role": "user", "content": f"Given the conversation log:\n{conversation}\n\nand the query:\n{query}\n\nDetermine if the query is relevant. If yes, refine it; if not, return it as is. Provide only the refined question, without any additional text."}
    ],
    temperature=0.5,
    max_tokens=40,
    top_p=1,
    stream=False,
    stop=None,
     )
    return response.choices[0].message.content
def get_conversation_string():
    conversation_string = ""
    start_index = max(len(st.session_state['responses']) - 2, 0)
    for i in range(start_index, len(st.session_state['responses']) - 1):        
        conversation_string += "Human: " + st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: " + st.session_state['responses'][i+1] + "\n"
    return conversation_string

