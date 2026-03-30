import ollama
from datetime import datetime

MODEL_NAME = "llama3.2:latest"

def create_chatbot():
    """Create and run a simple chatbot."""
    conversation_history = []
    
    print("=" * 60)
    print("🤖 Llama3.2 Chatbot")
    print("=" * 60)
    print(f"Model: {MODEL_NAME}")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to reset conversation history")
    print("=" * 60)
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit']:
                print("\nGoodbye! 👋")
                break
            
            if user_input.lower() == 'clear':
                conversation_history = []
                print("Conversation history cleared.\n")
                continue
            
            # Add user message to history
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Get response from Ollama
            print("\nBot: ", end="", flush=True)
            
            response = ollama.chat(
                model=MODEL_NAME,
                messages=conversation_history,
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                text = chunk['message']['content']
                print(text, end="", flush=True)
                full_response += text
            
            print("\n")
            
            # Add bot response to history
            conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Make sure Ollama is running and the model is installed.\n")

if __name__ == "__main__":
    create_chatbot()