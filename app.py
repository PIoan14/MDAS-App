import streamlit as st
import random
import time
from datetime import datetime

def response_generator():
    response = random.choice(
        [
            "Hello there! 👋 How can I assist you today?",
            "Hi, human! 🤖 Anything I can help you with?",
            "Do you need help? 🧐",
            "Sure! Let me think about that for a moment... 💭",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.set_page_config(page_title="Simple Chat", page_icon="💬", layout="wide")
st.title("💬 Simple Chat")

st.markdown(
    """
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
        border-right: 1px solid #444;
    }
    .conversation-button {
        background-color: #292929;
        color: white !important;
        border: none;
        width: 100%;
        text-align: left;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        font-size: 14px;
        transition: all 0.2s ease;
    }
    .conversation-button:hover {
        background-color: #ff4b4b;
    }
    .conversation-selected {
        background-color: #ff4b4b;
        color: white !important;
    }
    .faq-button {
        background-color: #ff4b4b;
        color: white !important;
        border: none;
        width: 100%;
        padding: 10px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    .faq-button:hover {
        background-color: #ff6666;
        transform: scale(1.03);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ===== Inițializare stare =====
if "conversations" not in st.session_state:
    st.session_state.conversations = {}  # dict cu {nume_conv: list[mesaje]}
if "current_conv" not in st.session_state:
    st.session_state.current_conv = None


# ===== SIDEBAR =====
st.sidebar.header("📁 Conversations")

# Afișează conversațiile existente
if st.session_state.conversations:
    for conv_name, conv_messages in st.session_state.conversations.items():
        preview = (
            conv_messages[0]["content"][:40] + "..."
            if conv_messages
            else "(Empty conversation)"
        )
        label = f"💬 {preview}"
        selected = conv_name == st.session_state.current_conv
        button_class = (
            "conversation-button conversation-selected"
            if selected
            else "conversation-button"
        )

        if st.sidebar.button(label, key=conv_name):
            st.session_state.current_conv = conv_name
            st.rerun()
        else:
            st.sidebar.markdown(
                f"<div class='{button_class}'>{label}</div>", unsafe_allow_html=True
            )
else:
    st.sidebar.write("No conversations yet. ✨")

st.sidebar.markdown("---")
if st.sidebar.button("➕ New Conversation"):
    new_name = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    st.session_state.conversations[new_name] = []
    st.session_state.current_conv = new_name
    st.rerun()


# ===== ZONA PRINCIPALĂ DE CHAT =====
if st.session_state.current_conv:
    messages = st.session_state.conversations[st.session_state.current_conv]
else:
    st.warning("💡 Create or select a conversation from the sidebar to begin.")
    st.stop()


# ===== FAQ la început (doar conversație nouă) =====
if len(messages) == 0:
    st.markdown("### 💡 Frequently Asked Questions")
    cols = st.columns(2)
    faq_buttons = [
        "🔑 Reset password",
        "🕒 Opening hours",
        "📤 Give me some code in JAVA",
        "📱 Mobile app",
    ]
    for i, q in enumerate(faq_buttons):
        with cols[i % 2]:
            if st.button(q, key=f"faq_{i}", use_container_width=True):
                messages.append({"role": "user", "content": q})
                with st.chat_message("user"):
                    st.markdown(q)
                with st.chat_message("assistant"):
                    response = st.write_stream(response_generator())
                messages.append({"role": "assistant", "content": response})
                st.session_state.conversations[
                    st.session_state.current_conv
                ] = messages
                st.rerun()

    # Aplică stilul personalizat pentru butoanele FAQ
    st.markdown(
        """
        <script>
        var buttons = window.parent.document.querySelectorAll('button[kind="secondary"]');
        buttons.forEach(b => {
            b.classList.add('faq-button');
        });
        </script>
        """,
        unsafe_allow_html=True,
    )


# ===== Afișare mesaje existente =====
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ===== Introducere mesaj nou =====
if prompt := st.chat_input("💬 Say something..."):
    messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"🙂 {prompt}")

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    messages.append({"role": "assistant", "content": response})
    st.session_state.conversations[st.session_state.current_conv] = messages
