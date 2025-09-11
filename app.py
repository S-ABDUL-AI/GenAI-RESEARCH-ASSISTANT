import streamlit as st
import tempfile
from model import ResearchAssistant, SimpleResearchAssistant

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="📘 GenAI Research Assistant", layout="wide")

# -------------------------------
# CUSTOM STYLES
# -------------------------------
st.markdown(
    """
    <style>
    body { background-color: #ffffff; color: black; }
    .demo-banner {
        background-color: #fef9c3;
        color: #92400e;
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
    .badge-blue { background-color: #2563eb; }   /* gpt-4o-mini */
    .badge-green { background-color: #16a34a; }  /* gpt-3.5-turbo */
    .badge-yellow { background-color: #ca8a04; } /* demo */
    .badge-red { background-color: #dc2626; }    /* error */
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# SESSION STATE
# -------------------------------
if "assistant" not in st.session_state:
    st.session_state.assistant = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# DEMO SAMPLE CONTENT
# -------------------------------
sample_pdf_text = """
Artificial Intelligence (AI) is transforming industries across the globe.
From healthcare to finance, AI systems are being used to automate tasks,
enhance decision-making, and generate new insights. However, concerns
around ethics, bias, and transparency remain critical as AI adoption grows.
"""

sample_url_text = """
OpenAI is a leading AI research organization focused on creating safe and useful artificial intelligence.
Its flagship model, GPT, is widely used for text generation, coding assistance, and research applications.
"""

# -------------------------------
# TITLE
# -------------------------------
st.title("📘 GenAI Research Assistant")
st.markdown("Upload a PDF or paste a URL, then chat with it! 🚀")

# -------------------------------
# TAB SETUP
# -------------------------------
tabs = st.tabs(["🟡 Demo Mode", "🟢 GPT-3.5-Turbo", "🔵 GPT-4o-Mini"])

# =========================================================
# DEMO MODE TAB
# =========================================================
with tabs[0]:
    st.markdown('<div class="demo-banner">🚀 Running in Demo Mode — No API Key Required</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload a PDF (Demo)", type=["pdf"], key="demo_pdf")
    url_input = st.text_input("Enter a website URL (Demo)", key="demo_url")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📘 Try Sample PDF (Demo)"):
            st.session_state.assistant = SimpleResearchAssistant("demo")
            st.session_state.assistant.load_text(sample_pdf_text)
            st.success("✅ Sample PDF loaded!")
    with col2:
        if st.button("🌐 Try Sample Website (Demo)"):
            st.session_state.assistant = SimpleResearchAssistant("demo")
            st.session_state.assistant.load_text(sample_url_text)
            st.success("✅ Sample website loaded!")

    if st.session_state.assistant and isinstance(st.session_state.assistant, SimpleResearchAssistant):
        if st.button("📄 Summarize (Demo)"):
            summary = st.session_state.assistant.summarize()
            st.subheader("📄 Summary")
            st.markdown('<span class="badge badge-yellow">🤖 Demo</span>', unsafe_allow_html=True)
            st.write(summary)

            st.subheader("👀 Document Preview")
            preview_text = st.session_state.assistant.text[:1000]
            st.text_area("Preview", preview_text, height=300)

        st.subheader("💬 Chat with your document (Demo)")
        if st.button("🗑️ Clear Chat History", key="clear_demo"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")

        user_query = st.chat_input("Ask me anything (Demo)...", key="demo_chat")
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)

            answer = st.session_state.assistant.ask(user_query, st.session_state.chat_history)

            with st.chat_message("assistant"):
                st.markdown('<span class="badge badge-yellow">🤖 Demo</span>', unsafe_allow_html=True)
                st.markdown(answer)

            st.session_state.chat_history.append((user_query, answer))

# =========================================================
# GPT-3.5 TAB
# =========================================================
with tabs[1]:
    api_key_35 = st.text_input("🔑 Enter your OpenAI API Key (GPT-3.5)", type="password", key="api_35")

    uploaded_file = st.file_uploader("Upload a PDF (GPT-3.5)", type=["pdf"], key="gpt35_pdf")
    url_input = st.text_input("Enter a website URL (GPT-3.5)", key="gpt35_url")

    if uploaded_file or url_input:
        if api_key_35:
            st.session_state.assistant = ResearchAssistant(api_key_35, model="gpt-3.5-turbo")
            if uploaded_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                st.session_state.assistant.load_pdf(tmp_path)
                st.success("✅ PDF loaded successfully!")
            elif url_input:
                st.session_state.assistant.load_url(url_input)
                st.success("✅ Website loaded successfully!")
        else:
            st.error("❌ Please enter your OpenAI API key for GPT-3.5.")

    if st.session_state.assistant and isinstance(st.session_state.assistant, ResearchAssistant):
        if st.button("📄 Summarize (GPT-3.5)"):
            summary, model = st.session_state.assistant.summarize()
            st.subheader("📄 Summary")
            st.markdown('<span class="badge badge-green">🤖 GPT-3.5</span>', unsafe_allow_html=True)
            st.write(summary)

        st.subheader("💬 Chat with your document (GPT-3.5)")
        if st.button("🗑️ Clear Chat History", key="clear_35"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")

        user_query = st.chat_input("Ask me anything (GPT-3.5)...", key="gpt35_chat")
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)

            answer, model = st.session_state.assistant.ask(user_query, st.session_state.chat_history)

            with st.chat_message("assistant"):
                st.markdown('<span class="badge badge-green">🤖 GPT-3.5</span>', unsafe_allow_html=True)
                st.markdown(answer)

            st.session_state.chat_history.append((user_query, answer))

# =========================================================
# GPT-4o-MINI TAB
# =========================================================
with tabs[2]:
    api_key_4o = st.text_input("🔑 Enter your OpenAI API Key (GPT-4o-Mini)", type="password", key="api_4o")

    uploaded_file = st.file_uploader("Upload a PDF (GPT-4o-Mini)", type=["pdf"], key="gpt4o_pdf")
    url_input = st.text_input("Enter a website URL (GPT-4o-Mini)", key="gpt4o_url")

    if uploaded_file or url_input:
        if api_key_4o:
            st.session_state.assistant = ResearchAssistant(api_key_4o, model="gpt-4o-mini")
            if uploaded_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                st.session_state.assistant.load_pdf(tmp_path)
                st.success("✅ PDF loaded successfully!")
            elif url_input:
                st.session_state.assistant.load_url(url_input)
                st.success("✅ Website loaded successfully!")
        else:
            st.error("❌ Please enter your OpenAI API key for GPT-4o-Mini.")

    if st.session_state.assistant and isinstance(st.session_state.assistant, ResearchAssistant):
        if st.button("📄 Summarize (GPT-4o-Mini)"):
            summary, model = st.session_state.assistant.summarize()
            st.subheader("📄 Summary")
            st.markdown('<span class="badge badge-blue">🤖 GPT-4o-Mini</span>', unsafe_allow_html=True)
            st.write(summary)

        st.subheader("💬 Chat with your document (GPT-4o-Mini)")
        if st.button("🗑️ Clear Chat History", key="clear_4o"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")

        user_query = st.chat_input("Ask me anything (GPT-4o-Mini)...", key="gpt4o_chat")
        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)

            answer, model = st.session_state.assistant.ask(user_query, st.session_state.chat_history)

            with st.chat_message("assistant"):
                st.markdown('<span class="badge badge-blue">🤖 GPT-4o-Mini</span>', unsafe_allow_html=True)
                st.markdown(answer)

            st.session_state.chat_history.append((user_query, answer))

# -------------------------------
# SIDEBAR FOOTER (Developer Info)
# -------------------------------
st.sidebar.markdown("---", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div style="color: black; font-size: 14px;">
        <h3>👨‍💻 About the Developer</h3>
        <p><b>Sherriff Abdul-Hamid</b><br>
        AI Engineer | Data Scientist | Economist</p>
        <p><b>Contact:</b><br>
        📧 <a href="mailto:Sherriffhamid001@gmail.com" style="color: black;">Sherriffhamid001@gmail.com</a><br>
        🌐 <a href="https://github.com/S-ABDUL-AI" target="_blank" style="color: black;">GitHub</a><br>
        🔗 <a href="https://www.linkedin.com/in/abdul-hamid-sherriff-08583354/" target="_blank" style="color: black;">LinkedIn</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
