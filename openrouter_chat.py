import streamlit as st
import openai
import os


# Load OpenRouter API key from Streamlit secrets
def get_openrouter_api_key():
    return st.secrets["OPENROUTER_API_KEY"]


def chat_with_openrouter(prompt, history=None):
    api_key = get_openrouter_api_key()
    client = openai.OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    messages = []
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=messages,
            max_tokens=256,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
