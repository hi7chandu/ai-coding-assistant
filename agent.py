import requests
import streamlit as st

SYSTEM_PROMPT = """
You are an elite AI coding assistant.

Responsibilities:
- Explain Python code clearly
- Fix bugs step-by-step
- Optimize code
- Review uploaded files
- Suggest best practices
- Teach beginners simply
"""

chat_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def coding_agent(user_input, file_content=""):

    auth_token = st.secrets.get("auth_token")

    if not auth_token:
        return (
            "❌ Missing Streamlit secret.\n\n"
            "Add this in Streamlit Cloud Secrets:\n"
            'auth_token = "Bearer sk-or-v1-your_api_key"'
        )

    full_prompt = f"""
User Question:
{user_input}

Uploaded Code:
{file_content}
"""

    chat_history.append({
        "role": "user",
        "content": full_prompt
    })

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": auth_token,
            "Content-Type": "application/json"
        },
        json={
            "model": "baidu/cobuddy:free",
            "messages": chat_history
        }
    )

    result = response.json()

    if "choices" in result:
        reply = result["choices"][0]["message"]["content"]
    else:
        reply = f"❌ API Error: {result}"

    chat_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply

