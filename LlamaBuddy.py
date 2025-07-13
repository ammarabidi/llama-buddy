import streamlit as st
import requests
import time
from datetime import datetime

# Configuration
API_KEY = st.secrets["API_KEY"] #api key
MODEL = "meta-llama/llama-3-70b-instruct"  # Model name
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
REQUEST_INTERVAL = 10  # Seconds between requests

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

def get_llama_response(prompt, task_type="chat"):
    # Rate limiting
    elapsed = time.time() - st.session_state.last_request_time
    if elapsed < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed)
    
    # Task-specific prompts
    task_prompts = {
        "code": f"Return only executable code with no explanations or comments. Code for: {prompt}",
        "translate": f"Translate this to English: {prompt}",
        "explain": f"Explain this in simple terms: {prompt}"
    }
    final_prompt = task_prompts.get(task_type, prompt)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://llama-assistant.streamlit.app",  # Update with URL
        "X-Title": "Llama 3 Assistant"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": final_prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(
            BASE_URL,
            headers=headers,
            json=payload,
            timeout=45  # Increased timeout
        )
        
        # Debugging output
        st.sidebar.code(f"Status: {response.status_code}\nResponse: {response.text[:200]}...")
        
        response.raise_for_status()
        st.session_state.last_request_time = time.time()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e.response.text}")
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
    return None

# Streamlit UI
st.set_page_config(page_title="AI Assistant", page_icon="🧠")
st.title("Ammar Codes🧠")
st.caption(f"Powered by {MODEL} via OpenRouter")

# Task selection
task_type = st.sidebar.radio(
    "Task Type",
    ["chat", "code", "translate", "explain"],
    horizontal=True,
    index=0
)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and task_type == "code":
            st.code(message["content"], language="python")
        else:
            st.write(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = get_llama_response(prompt, task_type)
        
        if response:
            if task_type == "code":
                st.code(response, language="python")
            else:
                st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.warning("Failed to get response. Please check your API key and try again.")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info(
    f"### Usage Info\n"
    f"🔹 **Model**: {MODEL}\n"
    f"⏱️ **Rate Limit**: 1 request every {REQUEST_INTERVAL}s\n"
    f"📝 **Last Request**: {datetime.fromtimestamp(st.session_state.last_request_time).strftime('%H:%M:%S') if st.session_state.last_request_time > 0 else 'None yet'}\n\n"
    f"💡 **Tips**:\n"
    f"- For code, specify language in your prompt\n"
    f"- Keep prompts clear and concise\n"
    f"- Free tier has limited requests/hour"
)

# Debug info
if st.sidebar.checkbox("Show debug info"):
    st.sidebar.json({
        "session_state": dict(st.session_state),
        "last_request": st.session_state.get("last_request_time", 0)
    })