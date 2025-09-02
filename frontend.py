# Step1: Setup Streamlit
import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Step2: User is able to ask question
# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    try:
        # Make API request
        response = requests.post(BACKEND_URL, json={"message": user_input})
        
        # Check status code first
        if response.status_code == 200:
            try:
                # Parse JSON once
                data = response.json()
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": f'{data["response"]} WITH TOOL: [{data["tool_called"]}]'
                })
            except ValueError:
                st.error(f"Invalid JSON response: {response.text}")
        else:
            st.error(f"Request failed with status {response.status_code}: {response.text}")
            
    except requests.RequestException as e:
        st.error(f"Failed to connect to backend: {str(e)}")

# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])