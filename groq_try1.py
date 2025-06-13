import streamlit as st
import pandas as pd
import requests

GROQ_API_KEY = "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"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

@st.cache_data
def load_data():
    return pd.read_csv(r"master_filled.csv")

df = load_data()
st.title("CSV-Powered Crop Q&A Chatbot (Groq-Powered)")

if st.checkbox("Show Data"):
    st.dataframe(df)
    
question = st.text_input("Ask a question about the crops:")


def relevant_rows(df, question):
    crops = df['crop'].unique()
    hits = [c for c in crops if c.lower() in question.lower()]
    if hits:
        return df[df['crop'].isin(hits)].head(50)  # grab up to 50 matching rows
    else:
        return df.sample(50)

# Make Groq API call
def query_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# Generate prompt and get response
subset = relevant_rows(df, question)
prompt = f"""
You are a helpful assistant. Below is a table of crop data:

{subset.to_csv(index=False)}

Answer the following question based on the table only:
{question}
"""

answer = query_groq(prompt)
st.markdown("Answer: " + answer)