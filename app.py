import json
from langchain_community.llms import Ollama
import streamlit as st

# Initialize the Ollama client with LLaMa 3.1 model
llm = Ollama(model="llama3.1", base_url="http://localhost:11434", verbose=True)

def sendPrompt(history):
    global llm
    # Join the conversation history into a single string
    conversation = "\n".join([f"{message['role']}: {message['content']}" for message in history])
    response = llm.invoke(conversation)
    return response

def save_conversation(file_path):
    # Save conversation history to a JSON file
    with open(file_path, "w") as file:
        json.dump(st.session_state.messages, file, indent=4)

def load_conversation(file_path):
    # Load conversation history from a JSON file
    try:
        with open(file_path, "r") as file:
            st.session_state.messages = json.load(file)
    except FileNotFoundError:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question!"}
        ]

st.title("Chat with Ollama")

# Load conversation history at the start
load_conversation("conversation_history.json")

# Handle user input and update conversation
if prompt := st.chat_input("Your question"):
    # Add user's prompt to the conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response from the model using the entire conversation history
    response = sendPrompt(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Save updated conversation history
    save_conversation("conversation_history.json")

# Display the conversation history
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])
