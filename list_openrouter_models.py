import openai
import streamlit as st


def get_openrouter_api_key():
    return st.secrets["OPENROUTER_API_KEY"]


def list_openrouter_models():
    api_key = get_openrouter_api_key()
    client = openai.OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    try:
        models = client.models.list()
        return [m.id for m in models.data]
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    st.write("Available OpenRouter models:")
    st.write(list_openrouter_models())
