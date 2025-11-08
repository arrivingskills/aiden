from flask import Flask, render_template, request, jsonify
import os
import aiden.former.ai_demo

print("Setting up ChromaDB...")
collection = aiden.former.ai_demo.setup_chromadb()

aiden.former.ai_demo.load_chroma_data(collection)
print("\nEnsure Ollama is running locally with at least one model downloaded.")
print(
    "You can start Ollama and download the llama2 model with: 'ollama run llama2'\n"
)

app = Flask(
    __name__, template_folder="/Users/andy/ws/lessons/christine/templates"
)

if not os.path.exists("/Users/andy/ws/lessons/christine/templates"):
    os.makedirs("/Users/andy/ws/lessons/christine/templates")

if not os.path.exists("static"):
    os.makedirs("static")


with open("/Users/andy/ws/lessons/christine/templates/index.html", "r") as f:
    html_content = f.read()

responses = {}

default_responses = [
    "I'm not sure I understand. Could you rephrase that?",
    "Interesting. Tell me more about that.",
    "I'm still learning. Could you try asking something else?",
    "I don't have an answer for that yet.",
    "Let's talk about something else. What's on your mind?",
]


def get_response(user_input):
    user_input = user_input.lower()
    response = aiden.former.ai_demo.submit_ai_query(user_input, collection)
    return response


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    bot_response = get_response(user_message)
    return jsonify({"response": bot_response.replace("\\n", "<br>")})


if __name__ == "__main__":
    print("Chatbot is starting up...")
    print("Make sure you have Flask installed. If not, run: pip install flask")
    print("To interact with the chatbot, open your web browser and go to:")
    print("http://127.0.0.1:5000/")
    app.run(debug=True)
