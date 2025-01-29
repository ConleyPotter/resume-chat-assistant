from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

from flask import Flask, jsonify, request
from flask_cors import CORS

# Load environment variables from .env file
import os
from dotenv import load_dotenv

load_dotenv()  

# Get the Pinecone API key from the environment
api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set")

# Create a Pinecone client
pc = Pinecone(api_key=api_key)

# Create an Assistant instance
assistant = pc.assistant.Assistant(assistant_name="example-assistant")

# Send a message to the assistant (example, you can uncomment to test)
# msg = Message(content="Where did the applicant go to college?")
# resp = assistant.chat(messages=[msg])

# print(resp["message"]["content"])

# Define the main function, which provides a way to pass a message to the assistant
def main(user_message_content: str):
    msg = Message(content=user_message_content)
    ai_response = assistant.chat(messages=[msg])
    return ai_response

# Create a Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Allow only requests from localhost:3000 to /api/*

# Define a route for the chat API
@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = main(user_message)  # Call your main function
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)