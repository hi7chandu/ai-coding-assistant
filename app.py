import streamlit as st
from agent import coding_agent
from utils import run_code
from PIL import Image
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Coding Assistant Pro",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
}

h1, h2, h3 {
    color: white;
}

.chat-box {
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

.user-msg {
    background-color: #2563eb;
    color: white;
}

.bot-msg {
    background-color: #1e293b;
    color: white;
    border: 1px solid #334155;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background: linear-gradient(to right, #3b82f6, #8b5cf6);
    color: white;
    font-weight: bold;
    border: none;
}

.stTextInput>div>div>input {
    background-color: #1e293b;
    color: white;
}

.css-1d391kg {
    background-color: #111827;
}

[data-testid="stSidebar"] {
    background: #111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center; font-size:50px;'>
🤖 AI Coding Assistant Pro
</h1>
<p style='text-align:center; color:lightgray;'>
Smart Coding • File Upload • Image AI • Code Runner
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([2.5, 1])

# ==================================================
# LEFT SIDE
# ==================================================
with col1:

    st.subheader("💬 AI Chat")

    # CHAT HISTORY
    for msg in st.session_state.messages:

        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-box user-msg">
                👤 {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"""
                <div class="chat-box bot-msg">
                🤖 {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    # CHAT INPUT
    user_input = st.chat_input("Ask coding questions...")

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.spinner("🤖 Thinking..."):
            response = coding_agent(user_input)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()

# ==================================================
# RIGHT SIDE
# ==================================================
with col2:

    st.subheader("🛠 AI Tools")

    # ---------------- FILE UPLOAD ----------------
    uploaded_file = st.file_uploader(
        "📂 Upload Python File",
        type=["py"]
    )

    file_content = ""

    if uploaded_file:

        file_content = uploaded_file.read().decode("utf-8")

        st.success("✅ File uploaded!")

        st.code(file_content, language="python")

        if st.button("🤖 Explain Code"):

            with st.spinner("Analyzing code..."):

                result = coding_agent(
                    "Explain this code",
                    file_content
                )

            st.success(result)

        if st.button("▶ Run Code"):

            result = run_code(file_content)

            st.success(result)

    st.markdown("---")

    # ---------------- IMAGE UPLOAD ----------------
    st.subheader("🖼 Image AI")

    image_file = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"]
    )

    if image_file:

        image = Image.open(image_file)

        st.image(image, use_container_width=True)

        if st.button("🔍 Analyze Image"):

            with st.spinner("Analyzing image..."):

                result = coding_agent(
                    "Describe this image"
                )

            st.info(result)

    st.markdown("---")

    # ---------------- QUICK ACTIONS ----------------
    st.subheader("⚡ Quick Actions")

    if st.button("Generate Python Project"):
        st.info("Feature coming soon!")

    if st.button("Debug My Code"):
        st.info("Feature coming soon!")

    if st.button("Convert Code"):
        st.info("Feature coming soon!")

# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown("""
<div style='text-align:center; color:gray;'>

Made with ❤️ using Streamlit + OpenRouter

</div>
""", unsafe_allow_html=True)
