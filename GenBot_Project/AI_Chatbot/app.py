from flask import Flask, render_template, request, jsonify, session
from chatbot import get_response
import datetime
import os

app = Flask(__name__)
app.secret_key = 'genbot-secret-key-2024'


@app.route('/')
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    bot_response = get_response(user_message)
    timestamp = datetime.datetime.now().strftime('%H:%M')

    # Store in session history
    if 'chat_history' not in session:
        session['chat_history'] = []
    session['chat_history'].append({
        'user': user_message,
        'bot': bot_response,
        'time': timestamp
    })
    session.modified = True

    return jsonify({
        'response': bot_response,
        'timestamp': timestamp
    })


@app.route('/history')
def history():
    return jsonify(session.get('chat_history', []))


@app.route('/clear')
def clear_history():
    session['chat_history'] = []
    return jsonify({'status': 'cleared'})


if __name__ == '__main__':
    app.run(debug=True)
