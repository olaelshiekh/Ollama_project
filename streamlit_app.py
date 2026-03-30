import streamlit as st
import ollama

MODEL_NAME = "llama3.2:latest"

st.set_page_config(
    page_title="Ola Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Llama3.2 Chatbot")

# Sidebar with info
with st.sidebar:
    st.subheader("ℹ️ About")
    st.write(f"**Model:** {MODEL_NAME}")
    st.write("A simple chatbot powered by Ollama")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Chat history cleared!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Hello, how can I assist you today?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from Ollama
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = ollama.chat(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                stream=True
            )
            
            for chunk in response:
                full_response += chunk['message']['content']
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Make sure Ollama is running and the model is installed.")
