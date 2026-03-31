import httpx
import streamlit as st


# -------------------------------
# Get API Key from Streamlit Secrets
# -------------------------------
def get_openrouter_api_key():
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        return None


def validate_api_key():
    """Verify that the key exists and that OpenRouter accepts it."""
    api_key = get_openrouter_api_key()
    if not api_key:
        return False, "OPENROUTER_API_KEY not set in Streamlit secrets."

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        response = httpx.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10,
        )
        if response.status_code == 401:
            return False, (
                "Authentication failed (401). Your OpenRouter API key may be "
                "invalid, inactive, or not enabled for chat models. "
                "Please verify your key at https://openrouter.ai/keys"
            )
        return True, None
    except Exception as e:
        return False, f"Error validating API key: {str(e)}"


# -------------------------------
# Chat Function
# -------------------------------
def chat_with_openrouter(prompt, history=None):
    api_key = get_openrouter_api_key()

    if not api_key:
        return "Error: OPENROUTER_API_KEY not set in Streamlit secrets."

    try:
        messages = history[:] if history else []
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.7,
        }

        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )

        if response.status_code == 401:
            return (
                "Authentication failed (401). "
                "Your OpenRouter API key may be invalid or inactive. "
                "Please verify at https://openrouter.ai/keys"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        return f"Error: {str(e)}"
