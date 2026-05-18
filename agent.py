
import requests
import streamlit as st

API_KEY = st.secrets["OPENROUTER_API_KEY"]

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
    {"role": "system", "content": SYSTEM_PROMPT}
]

def coding_agent(user_input, file_content=""):

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
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "baidu/cobuddy:free",
            "messages": chat_history
        }
    )

    result = response.json()

    # --- THE FIX STARTS HERE ---
    # We check if the API actually sent a valid response back
    if "choices" in result:
        reply = result["choices"][0]["message"]["content"]
    else:
        # If something went wrong (like a bad API key), it catches the error safely
        print("API Error Response:", result) 
        reply = f"API Error: The AI model did not return a standard response. Details: {result}"
    # --- THE FIX ENDS HERE ---

    chat_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply

