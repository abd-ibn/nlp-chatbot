from sentence_transformers import SentenceTransformer
import pinecone
from pinecone import Pinecone
import openai
import os
import streamlit as st

# Set up OpenAI API key
openai.api_key = ""

# Set up Pinecone API key
api_key = os.getenv("PINECONE_API_KEY") or "your pinecone key"
pc = Pinecone(api_key=api_key)
index_name = 'chatbot'
index = pc.Index(index_name)

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to find matches in Pinecone index
def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(vector=input_em, top_k=3, include_metadata=True)
    matches = result['matches']
    context = " ".join([match['metadata']['text'] for match in matches])
    return context

# Function to get conversation string
def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses']) - 1):
        conversation_string += "Human: " + st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: " + st.session_state['responses'][i + 1] + "\n"
    return conversation_string

import nltk
from nltk.corpus import stopwords
import re

# Download the French stop words list if not already downloaded
# nltk.download('stopwords')

# Function to process text
def process_text(query):
    # Define the French stop words
    stop_words = set(stopwords.words('french'))
    
    # Split the query into words
    words = query.split()
    
    # Remove stop words
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    # Join the words back into a string
    filtered_query = ' '.join(filtered_words)
    
    # Replace "fst" or "fstt" with "faculte" (case-insensitive)
    filtered_query = re.sub(r'\bfst{1,2}\b', 'faculte', filtered_query, flags=re.IGNORECASE)
    
    # Check if "mst" or "master" is in the original query (case-insensitive)
    if re.search(r'\bmst\b', query, flags=re.IGNORECASE) or re.search(r'\bmaster\b', query, flags=re.IGNORECASE):
        # Append "mst" and "master" to the filtered query
        filtered_query += " mst master"
    
    # Check if "licence" or "lst" is in the original query (case-insensitive)
    if re.search(r'\blicence\b', query, flags=re.IGNORECASE) or re.search(r'\blst\b', query, flags=re.IGNORECASE):
        # Append "licence" and "lst" to the filtered query
        filtered_query += " lst licence"
    
    return filtered_query
