import streamlit as st
from agent import coding_agent
from utils import run_code
import streamlit as st

st.write("Secrets loaded:", "auth_token" in st.secrets)

if "auth_token" in st.secrets:
    st.write("Preview:", st.secrets["auth_token"][:20])

st.set_page_config(
    page_title="AI Coding Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------- HEADER ----------
st.markdown(
    "<h1 style='text-align:center;'>🤖 AI Coding Assistant Pro</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------- LEFT + RIGHT LAYOUT ----------
col1, col2 = st.columns([2, 1])

# ---------- LEFT SIDE (CHAT) ----------
with col1:

    st.subheader("💬 Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask anything about code...")

    if user_input:

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = coding_agent(user_input)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

        st.rerun()

# ---------- RIGHT SIDE (TOOLS) ----------
with col2:

    st.subheader("🛠 Tools")

    uploaded_file = st.file_uploader(
        "Upload Python file",
        type=["py"]
    )

    file_content = ""

    if uploaded_file:

        file_content = uploaded_file.read().decode("utf-8")

        st.success("✅ File loaded!")

        st.code(file_content, language="python")

        if st.button("🤖 Explain Code"):

            result = coding_agent(
                "Explain this code",
                file_content
            )

            st.info(result)

        if st.button("▶ Run Code"):
            result = run_code(file_content)
            st.success(result)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit + OpenRouter")
