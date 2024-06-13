#AI Answer 
from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
import fitz  # PyMuPDF

genai.configure(api_key=os.getenv("AIzaSyBOr6MnVBoU-RVkuzskwUVbsf1RuVTEjmI"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Initialize our Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
submit = st.button("Ask the question")

if pdf_file:
    pdf_text = read_pdf(pdf_file)
    #st.session_state['chat_history'].append(("PDF", pdf_text))
    #st.subheader("Extracted PDF Text")
    #st.write(pdf_text)

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("Question", input))
    st.subheader("The Response is")
    answer = ""
    for chunk in response:
        st.write(chunk.text)
        answer += chunk.text
    st.session_state['chat_history'].append(("Answer", answer))

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
