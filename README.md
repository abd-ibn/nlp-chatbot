# FSTT Assistant ChatBOT

## Overview

This is an assistant chatbot application built for the FSTT (Faculté des Sciences et Techniques de Tanger). It uses language models and Pinecone vector database to provide responses to user queries related to courses, trainings, modules, departments, clubs, and more.

## How to Run

1. First, navigate to the `app` folder in your terminal or command prompt.

2. Activate the virtual environment by running the following command:

   ```
   & "env/Scripts/Activate.ps1"
   ```

3. Install the required dependencies from the `requirements.txt` file using pip:

   ```
   pip install -r requirements.txt
   ```

4. Set up the API keys in the code:
   
   - You'll need a Pinecone API key for the vector database.
   - You'll need a Hugging Face API token for the language model (LLM) used in the application.

5. For the Pinecone vector database:
   
   - Run the notebook `3-embedding.ipynb` to store the necessary data for this project into your Pinecone index.

6. Finally, to run the application, execute the following command:

   ```
   streamlit run app.py
   ```

This will start the Streamlit server and open the application in your default web browser. You can then interact with the chatbot by asking questions related to the FSTT.

<br/><br/><br/>


### Project
   - Supervised by : Mr. Lotfi EL AACHAK
   - Realized by : Abdelali IBN TABET , Soueilem Mohamed Abd Nasir 
