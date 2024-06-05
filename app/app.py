import os
import streamlit as st
from langchain_community.llms import HuggingFaceEndpoint
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message
from utils import *

# Load custom CSS
with open('styles.css') as f:
    st.markdown(f'<style>{(f.read())}<style>', unsafe_allow_html=True)

# Set Hugging Face API token
os.environ['HUGGINGFACEHUB_API_TOKEN'] = 'your huggingface key'

# Streamlit UI
st.header("Assistant ChatBOT de la FSTT")
st.subheader(" ")

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Bonjour ! Je suis l'assistant ChatBot de la FSTT. Comment puis-je vous aider aujourd'hui ?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# Adjust model parameters explicitly
model_kwargs = {
    "temperature": 0.3,
    #"max_length": 512,
    #"max_new_tokens": 512,
}

# Create the HuggingFaceEndpoint with adjusted parameters
llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", **model_kwargs)

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

# Define message prompt templates
system_msg_template = SystemMessagePromptTemplate.from_template(template="""Vous êtes un assistant de la FSTT (Faculté des Sciences et Techniques de Tanger). Répondez en français à la question en utilisant uniquement le contexte fourni ci-dessous. Fournissez uniquement les informations nécessaires, aussi brièvement que possible. Ne complétez pas ou ne générez pas de nouvelles questions. Si la réponse ne se trouve pas dans le texte ci-dessous, indiquez que vous ne savez pas et que vous ne pouvez pas répondre à cette question.""")

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

# Create conversation chain
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# Containers for chat history and input box
response_container = st.container()
textcontainer = st.container()

# from transformers import pipeline

# messages = [
#     {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
#     {"role": "user", "content": "Who are you?"},
# ]
# chatbot = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.3")
# chatbot(messages)

with textcontainer:
    query = st.text_input("Posez une question ", key="input")
    if query:
        with st.spinner("En train de générer la réponse..."):
            # Clear conversation memory for each new question
            st.session_state.buffer_memory.clear()
            processed_query = process_text(query)
            context = find_match(processed_query)
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}?\n\n-end of prompt-")

        st.session_state.requests.append(query)
        st.session_state.responses.append(response)

with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i], key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
