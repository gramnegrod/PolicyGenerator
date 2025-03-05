import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Define the system prompt
SYSTEM_PROMPT = """The Policy & Procedure Generator will allow healthcare professionals to dictate rough concepts for medical office policies and procedures, which
will then be transformed into well-structured, compliant documents following industry standards. YOU WILL RECEIVE RAMBLING INPUT FROM THE USER AND YOU NEED TO ASK QUESTIONS AOBUT WHAT THEY WANT IN THE POLICY AND EVENTUALY AFTER MULTIPLE QUESTION ANSWER ITERATIONS TURN THE CONVOS INTO A GREAT POLICY.

{
  "expert_identity": "You are a healthcare management consultant with extensive experience in developing policies and procedures for medical
offices, particularly in family medicine settings. Your expertise lies in creating structured, concise, and thorough guidelines that ensure
efficient and compliant operations. You have a deep understanding of healthcare laws, regulations, and best-practice guidelines, which allows
you to align policies with industry standards. You are skilled at engaging with stakeholders, including nursing staff and healthcare
professionals, to ensure their input and buy-in. Your approach emphasizes clarity and structure, providing step-by-step instructions that
eliminate ambiguity. You are adept at designing documentation and communication protocols that facilitate effective record-keeping and
reporting. You also focus on accountability, identifying responsible parties and compliance monitoring strategies. Your experience in training
and implementation ensures that staff are well-prepared to adopt new policies. Finally, you incorporate evaluation and continuous improvement
processes to keep policies relevant and effective. Your comprehensive approach ensures that the policies you develop are easy-to-understand,
actionable, practical, and fully compliant with healthcare industry standards.",
  "best_prompt": "\\nYou are tasked with developing a comprehensive set of policies and procedures specifically for nursing staff at a family
medicine office. Your objective is to create structured, concise, and thorough guidelines that enhance operational efficiency, ensure compliance
 with healthcare regulations, and improve patient care. \\n\\nYour response should include the following key elements, clearly organized into
steps:\\n\\n1. **Identification and Definition**  \\n   - Clearly define the policy objectives, scope, and specific issues being addressed,
ensuring relevance to the family medicine office setting.\\n\\n2. **Stakeholder Involvement**  \\n   - Describe how nursing staff and other
relevant healthcare professionals should be involved in the policy development process, ensuring their insights and expertise are
incorporated.\\n\\n3. **Compliance and Alignment**  \\n   - Ensure the policies align with applicable healthcare laws, regulations, and
best-practice guidelines, emphasizing the importance of legal and ethical compliance.\\n\\n4. **Clarity and Structure**  \\n   - Provide clear,
step-by-step instructions that eliminate ambiguity and are easy for staff to follow, ensuring practical usability.\\n\\n5. **Documentation and
Communication**  \\n   - Outline procedures for documentation, record-keeping, reporting, and communication channels, ensuring transparency and
accountability.\\n\\n6. **Accountability and Enforcement**  \\n   - Identify responsible parties and explain strategies for monitoring compliance
and enforcing policies, ensuring accountability.\\n\\n7. **Training and Implementation**  \\n   - Describe how staff training, acknowledgment, and
implementation should occur to ensure effective adoption and understanding.\\n\\n8. **Evaluation and Continuous Improvement**  \\n   - Include
timelines for regular review, evaluation methods, feedback mechanisms, and policy updates to ensure continuous improvement and
relevance.\\n\\nEnsure the policies are practical, actionable, and fully compliant with healthcare industry standards. Use evidence-based
practices and logical reasoning to support your response, and consider the diverse scenarios that may arise in a family medicine office.\\n\\n###
Expert Role: You are an expert Policy and Procedure Specialist for a medical office. You have extensive knowledge of healthcare regulations,
nursing operations, compliance standards, and best practices in medical administration. You excel at drafting clear, precise, and actionable
policy and procedure documents that nursing staff can easily understand and implement effectively. Use deep, detailed reasoning and break the
problem into smaller parts, employing logical stepwise thinking."
}"""

# Define the welcome message
WELCOME_MESSAGE = "Welcome to the Healthcare Policy & Procedure Generator! I can help you create professional healthcare policies for your medical office. What type of policy or procedure would you like to develop today?"

# Load environment variables (for local development)
load_dotenv(override=True)

# For debugging, print the current environment variables path
env_path = os.path.join(os.getcwd(), '.env')
print(f"Looking for .env file at: {env_path}")
print(f"Does .env file exist? {os.path.exists(env_path)}")

# Set page configuration
st.set_page_config(
    page_title="OpenAI Chat",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Get OpenAI API key - read directly from the .env file as a fallback
try:
    # Try to get from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # If not found, try to read directly from the .env file
    if not openai_api_key:
        with open('.env', 'r') as f:
            env_content = f.read()
            for line in env_content.split('\n'):
                if line.startswith('OPENAI_API_KEY='):
                    openai_api_key = line.split('=', 1)[1].strip()
                    print(f"Loaded API key directly from .env file")
    
    # Debug information
    st.sidebar.info(f"Current working directory: {os.getcwd()}")
    if openai_api_key:
        st.sidebar.success("✅ API Key loaded successfully")
        st.sidebar.info(f"Key preview: {openai_api_key[:5]}...{openai_api_key[-5:]}")
    else:
        st.sidebar.error("❌ Failed to load API key from environment or .env file")
    
    if not openai_api_key:
        st.error("OpenAI API key is missing. Please add it in the environment variables (.env file).")
        st.stop()
        
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=openai_api_key)
    
except Exception as e:
    st.error(f"Error loading API key: {str(e)}")
    st.stop()

# Default model
DEFAULT_MODEL = os.getenv("MODEL", "gpt-4o")

# Custom CSS for a more modern look
st.markdown("""
<style>
    /* Main container styling */
    .main {
        max-width: 1000px;
        margin: 0 auto;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6;
        color: #2c3e50;
        padding: 10px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        padding: 15px 20px;
        font-size: 16px;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: #6c5ce7;
        box-shadow: 0 1px 5px rgba(108,92,231,0.2);
    }
    
    /* Message styling */
    .user-message {
        background-color: #e6f7ff;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #1890ff;
        font-size: 16px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .assistant-message {
        background-color: #f8f9fa;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #6c5ce7;
        font-size: 16px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #6c5ce7;
        color: white;
        border-radius: 8px;
        padding: 10px 15px;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #5b4cc7;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Token usage info */
    .usage-info {
        text-align: center;
        font-size: 14px;
        color: #6c757d;
        margin-top: 30px;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
        border-right: 1px solid #e1e4e8;
    }
</style>
""", unsafe_allow_html=True)

# App title with a nicer layout
st.title("💬 Healthcare Policy & Procedure Generator")
st.markdown("Create professional healthcare policies with AI assistance")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Model",
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4"],
        index=0  # Default to gpt-4o
    )
    max_tokens = st.slider("Max Tokens", 100, 2000, 1000)
    
    # API key input (optional as we can use secrets)
    custom_api_key = st.text_input("OpenAI API Key (optional)", type="password")
    if custom_api_key:
        client = OpenAI(api_key=custom_api_key)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        div_class = "assistant-message" if message["role"] == "assistant" else "user-message"
        st.markdown(f'<div class="{div_class}">{message["content"]}</div>', unsafe_allow_html=True)

# Initialize token usage counter
if "token_usage" not in st.session_state:
    st.session_state.token_usage = {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}

# Define a callback function to handle form submission
def handle_input():
    if st.session_state.user_input.strip():
        user_message = st.session_state.user_input
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Create a placeholder for the assistant's response with a spinner
        with st.spinner("Thinking..."):
            try:
                # Call OpenAI API using the modern client syntax
                response = client.chat.completions.create(
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
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        # Clear the input box (this happens before the widget is rendered again)
        st.session_state.user_input = ""

# User input with callback
st.text_input("Your message:", key="user_input", placeholder="Type your message here...", on_change=handle_input)

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
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]
    st.session_state.token_usage = {"total_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0}
    st.rerun()
