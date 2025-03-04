import streamlit as st
import openai
from dotenv import load_dotenv
import os
import time

# Load environment variables (for local development)
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="OpenAI Chat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Get OpenAI API key
if os.getenv("OPENAI_API_KEY"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    # For Streamlit Sharing, use secrets
    openai.api_key = st.secrets.get("OPENAI_API_KEY", "")

# Default model
DEFAULT_MODEL = os.getenv("MODEL", "gpt-4-turbo")

# Custom CSS
st.markdown("""
<style>
    .main {
        max-width: 800px;
        margin: 0 auto;
    }
    .stTextInput > div > div > input {
        padding: 12px 15px;
        font-size: 16px;
    }
    .user-message {
        background-color: #e6f7ff;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #1890ff;
    }
    .assistant-message {
        background-color: #f2f2f2;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #6c757d;
    }
    .usage-info {
        text-align: center;
        font-size: 12px;
        color: #6c757d;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title("💬 AI Chat Assistant")
st.markdown("Interact with OpenAI's language models")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Model",
        ["gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o", "gpt-4"]
    )
    max_tokens = st.slider("Max Tokens", 100, 2000, 1000)
    
    # API key input (optional as we can use secrets)
    custom_api_key = st.text_input("OpenAI API Key (optional)", type="password")
    if custom_api_key:
        openai.api_key = custom_api_key
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

# Check for API key
if not openai.api_key:
    st.error("OpenAI API key is missing. Please add it in the sidebar or through environment variables.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant who provides accurate, concise, and useful information to users."},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        div_class = "assistant-message" if message["role"] == "assistant" else "user-message"
        st.markdown(f'<div class="{div_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Initialize token usage counter
if "token_usage" not in st.session_state:
    st.session_state.token_usage = {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}

# User input
user_input = st.text_input("Your message:", key="user_input", placeholder="Type your message here...")

# When user submits input
if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message immediately
    st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)
    
    # Create a placeholder for the assistant's response with a spinner
    with st.spinner("Thinking..."):
        try:
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                max_tokens=max_tokens
            )
            
            # Get the response
            assistant_response = response.choices[0].message.content
            
            # Update token usage
            st.session_state.token_usage = {
                "total_tokens": st.session_state.token_usage["total_tokens"] + response.usage.total_tokens,
                "prompt_tokens": st.session_state.token_usage["prompt_tokens"] + response.usage.prompt_tokens,
                "completion_tokens": st.session_state.token_usage["completion_tokens"] + response.usage.completion_tokens
            }
            
            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Display assistant's response
            st.markdown(f'<div class="assistant-message">{assistant_response}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Force a rerun to update the UI
    st.rerun()

# Display token usage
st.markdown(
    f'<div class="usage-info">Total Tokens Used: {st.session_state.token_usage["total_tokens"]} '
    f'(Prompt: {st.session_state.token_usage["prompt_tokens"]}, '
    f'Completion: {st.session_state.token_usage["completion_tokens"]})</div>',
    unsafe_allow_html=True
)

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant who provides accurate, concise, and useful information to users."},
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]
    st.session_state.token_usage = {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}
    st.rerun()
