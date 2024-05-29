import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from groq import Groq

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq client
client = Groq(api_key=api_key)

def get_ai_response(user_message, historical_data):
    messages = [
        {"role": "user", "content": user_message},
        {"role": "user", "content": f"Here is the stock data:\n\n{historical_data}"}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Streamlit web application
st.title("AI stock analysis")
st.subheader("With the help of AI analyse data like a pro.")

# Upload CSV file
uploaded_file = st.file_uploader("Upload Historical Stock Data (CSV)", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data")
    st.write(df)

    # Convert DataFrame to string for AI processing
    data_str = df.to_string(index=False)

    # User input text box
    user_input = st.text_input("Ask the AI about the data: ")

    if st.button("Ask AI"):
        with st.spinner("AI is thinking..."):
            ai_response = get_ai_response(user_input, data_str)
            st.text_area("AI: ", ai_response, height=600)