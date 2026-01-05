import streamlit as st
import requests
import time

# ================= CONFIG =================
API_URL = "http://127.0.0.1:8000/run"

st.set_page_config(
    page_title="Agent Chat",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= CUSTOM CSS =================
st.markdown(
    """
    <style>
    /* -------- GENERAL -------- */
    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .subtitle {
        font-size: 15px;
        color: #9aa4b2;
        margin-bottom: 24px;
    }

    /* -------- REMOVE AVATARS -------- */
    .stChatMessage [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* -------- CHAT ALIGNMENT -------- */
    
    /* User → RIGHT SIDE */
    .stChatMessage[data-testid="chat-message-user"] {
        flex-direction: row-reverse;
        text-align: right;
        justify-content: flex-end;
    }

    .stChatMessage[data-testid="chat-message-user"] .stMarkdown {
        background-color: rgba(31, 111, 235, 0.15);
        padding: 12px 16px;
        border-radius: 16px;
        max-width: 75%;
        margin-left: auto;
        margin-right: 0;
    }

    /* Add user label on right side */
    .stChatMessage[data-testid="chat-message-user"]::before {
        content: "User";
        font-size: 12px;
        color: #6b7280;
        margin-right: 8px;
        align-self: flex-end;
        margin-bottom: 4px;
    }

    /* Assistant → LEFT SIDE */
    .stChatMessage[data-testid="chat-message-assistant"] {
        flex-direction: row;
        text-align: left;
        justify-content: flex-start;
    }

    .stChatMessage[data-testid="chat-message-assistant"] .stMarkdown {
        background-color: rgba(128, 128, 128, 0.15);
        padding: 12px 16px;
        border-radius: 16px;
        max-width: 75%;
        margin-right: auto;
        margin-left: 0;
    }

    /* Add agent label on left side */
    .stChatMessage[data-testid="chat-message-assistant"]::before {
        content: "Agent";
        font-size: 12px;
        color: #6b7280;
        margin-left: 8px;
        align-self: flex-end;
        margin-bottom: 4px;
    }

    /* -------- THEME AWARE INPUT -------- */
    html[data-theme="dark"] textarea {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }

    html[data-theme="light"] textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    .stChatInput textarea {
        border-radius: 999px;
        padding: 12px 16px;
    }

    /* -------- RESPONSIVE ADJUSTMENTS -------- */
    @media (max-width: 768px) {
        .stChatMessage[data-testid="chat-message-user"] .stMarkdown,
        .stChatMessage[data-testid="chat-message-assistant"] .stMarkdown {
            max-width: 85%;
        }
        
        .stChatMessage[data-testid="chat-message-user"]::before,
        .stChatMessage[data-testid="chat-message-assistant"]::before {
            font-size: 11px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= HEADER =================
st.markdown('<div class="main-title">🤖 Agent Chat</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Multi-agent orchestration with Planner, Researcher & Summarizer</div>',
    unsafe_allow_html=True
)

# ================= SESSION STATE =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= CHAT HISTORY =================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= CHAT INPUT =================
prompt = st.chat_input("Message Agent Orchestration System...")

# ================= MESSAGE HANDLING =================
if prompt:
    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant message
    with st.chat_message("assistant"):
        with st.spinner("🤝 Agents are collaborating..."):
            try:
                start_time = time.time()

                response = requests.post(
                    API_URL,
                    json={"query": prompt},
                    timeout=300
                )

                data = response.json()
                output = data.get("output", "No response received.")
                elapsed = time.time() - start_time

                st.markdown(output)
                st.caption(f"⏱️ {elapsed:.2f} seconds")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": output
                })

            except Exception as e:
                error_msg = f"❌ Backend error: {e}"
                st.error(error_msg)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })