import os
import uuid
from flask import Flask, jsonify, render_template, request, session
from database import init_db, save_message, get_history, clear_history, get_college_info
from chatbot import CollegeChatbot

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-this-secret")
init_db()
chatbot = CollegeChatbot()

SUGGESTED_QUESTIONS = [
    "What courses are available?",
    "What is the admission process?",
    "What scholarships are available?",
    "Is hostel accommodation available?",
    "What is the college fee structure?",
    "How can I contact the college?"
]

@app.before_request
def ensure_session():
    if "chat_session_id" not in session:
        session["chat_session_id"] = str(uuid.uuid4())

@app.get("/")
def index():
    info = get_college_info()
    return render_template(
        "index.html",
        college_name=info.get("name", "College Enquiry Chatbot"),
        suggested_questions=SUGGESTED_QUESTIONS
    )

@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Please enter a message."}), 400
    if len(message) > 1000:
        return jsonify({"error": "Please keep your question under 1000 characters."}), 400

    session_id = session["chat_session_id"]
    save_message(session_id, "user", message)
    result = chatbot.get_response(message)
    save_message(session_id, "bot", result["answer"])
    return jsonify({
        "answer": result["answer"],
        "matched": result["matched"],
        "score": result["score"]
    })

@app.get("/api/history")
def history():
    return jsonify({"messages": get_history(session["chat_session_id"])})

@app.post("/api/clear")
def clear():
    clear_history(session["chat_session_id"])
    return jsonify({"success": True, "message": "Chat history cleared."})

@app.get("/api/college")
def college():
    return jsonify(get_college_info())

@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "The requested resource was not found."}), 404

@app.errorhandler(500)
def server_error(_error):
    return jsonify({"error": "Something went wrong on the server. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
