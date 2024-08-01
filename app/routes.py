from flask import Blueprint, request, jsonify
from app import db, redis
from app.models import Question, Answer, Message

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return "Hello, World!"

@bp.route('/webhook', methods=['POST'])
def webhook():
    # Handle incoming webhook from Telegram
    data = request.get_json()
    message = data.get('message')
    if message:
        user_id = message['from']['id']
        content = message['text']
        # Save message to database
        new_message = Message(user_id=user_id, content=content)
        db.session.add(new_message)
        db.session.commit()
        # Check for keyword and reply
        response = check_keyword(content)
        return jsonify({'text': response})
    return jsonify({'status': 'ok'})

def check_keyword(content):
    # Implement keyword check logic
    question = Question.query.filter_by(content=content).first()
    if question:
        answer = Answer.query.filter_by(question_id=question.id).first()
        if answer:
            return answer.content
    return "I don't understand"
