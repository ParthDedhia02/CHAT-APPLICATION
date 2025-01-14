from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Validate API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key not found. Please configure the `.env` file.")
    st.stop()

# Configure GenAI
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-exp")
chat = model.start_chat(history=[])

# Function to get Gemini response for text
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error fetching response: {e}")
        return []

# Streamlit app initialization
st.set_page_config(
    page_title="AI CHATBOT 🤖",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"ABOUT": "Hi, this is Parth!"}
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        font-size: 60px; 
        color: #FFEB00; 
        text-align: center; 
        font-family: "Arial", sans-serif;
    }
    .response-box {
        padding: 20px; 
        background-color: #C4D9FF; 
        border-radius: 10px; 
        margin-top: 10px;
        font-size: 30px; 
        color: black;
    }
    textarea {
        font-size: 1.5rem !important;
        height: 100px !important;
        width: 100% !important;
    }
    input {
        font-size: 1.75rem !important;
    }
    .stButton button.submit-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton button.submit-button:hover {
        background-color: #45a049;
    }
    .stButton button.clear-history-button {
        background-color: #FF4500;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .stButton button.clear-history-button:hover {
        background-color: #FF6347;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>AI CHATBOT 🤖</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("wb.png", use_container_width=True)
st.sidebar.title("Welcome to the AI Chatbot 🦾")
st.sidebar.markdown("""
    <div style="font-size: 20px; font-family: 'Arial', sans-serif;">
        Ask me anything! I'm here to help 🤖💡
    </div>
""", unsafe_allow_html=True)

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Navbar with Chat History toggle button
nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    toggle_history = st.button("Chat History", key="toggle_history")

# User input and button
if not toggle_history:
    with st.container():
        st.markdown("<h1>💬 Ask Your Question:</h1>", unsafe_allow_html=True)
        input = st.text_area(
            "Type your question here",
            "",
            max_chars=250,
            key="user_input",
            placeholder="e.g. What is the meaning of life? 🤔"
        )
        submit = st.button("Submit", key="submit_button")

        if submit:
            if input.strip():
                # Get AI response
                response = get_gemini_response(input)
                full_response = "".join([chunk.text for chunk in response])

                st.session_state["chat_history"].append(("You", input))
                st.session_state["chat_history"].append(("Bot", full_response))

                # Display chatbot conversation
                st.markdown("### 🤖 Bot's Response:")
                st.markdown(f"<div class='response-box'>{full_response}</div>", unsafe_allow_html=True)
            else:
                st.warning("Please enter a valid question. 🧐")

# Display Chat History if toggled
if toggle_history:
    st.markdown("### 🗨️ Conversation History:")
    if len(st.session_state["chat_history"]) > 0:
        for idx, (speaker, message) in enumerate(st.session_state["chat_history"]):
            if speaker == "You":
                st.markdown(f"**{speaker}**: {message}")
            else:
                st.markdown(f"**{speaker}**: <div class='response-box'>{message}</div>", unsafe_allow_html=True)
    else:
        st.info("Chat history is empty. Start a conversation!")

    # Clear Chat History button
    if st.button("Clear Chat History", key="clear_history", help="Click to clear chat history."):
        st.session_state["chat_history"] = []
