import streamlit as st
import requests

# The URL where your FastAPI server is listening
API_URL = "http://127.0.0.1:8000"

# 1. Setup the webpage look (Wide mode gives us room for a sidebar)
st.set_page_config(page_title="VIK Assistant", layout="wide")

# 2. Custom CSS to hide Streamlit's default junk and center the chat
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* Center the chat and limit its width for better readability */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 850px; 
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Clean, minimalist text)
with st.sidebar:
    st.title("VIK Assistant")
    st.caption("Your smart university AI.")
    st.divider()
    
    # A prominent "New Chat" button
    if st.button("New Chat / Clear Memory", use_container_width=True, type="primary"):
        try:
            requests.post(f"{API_URL}/clear")
            st.session_state.messages = []
            st.rerun() # Instantly refreshes the screen to wipe the chat
        except:
            st.error("Could not reach backend to clear memory.")
    
    st.divider()
    st.markdown("### Suggested Questions:")
    st.markdown("- *Who teaches Data-Driven Systems?*")
    st.markdown("- *When is the Spring holiday?*")
    st.markdown("- *How many ECTS credits is the Marketing course?*")

# 4. Initialize the UI's internal memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Welcome Screen (Elegant and clean)
if len(st.session_state.messages) == 0:
    st.header("How can I help you with your studies today?")
    st.caption("I have read the 2025/2026 Academic Calendar, VIK Courses, and GTK Courses.")

# 6. Redraw all previous chat bubbles using default minimalist icons
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. The actual chat input box at the bottom
if prompt := st.chat_input("Message VIK Assistant..."):
    
    # Show user message instantly
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show a "Thinking..." spinner while we wait for the backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{API_URL}/chat", json={"prompt": prompt})
                if response.status_code == 200:
                    bot_answer = response.json()["answer"]
                else:
                    bot_answer = f"System Error: Backend returned {response.status_code}"
            except requests.exceptions.ConnectionError:
                bot_answer = "Error: Could not connect to the backend! Is your FastAPI server running?"
        
        # Display the final answer
        message_placeholder.markdown(bot_answer)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_answer})
