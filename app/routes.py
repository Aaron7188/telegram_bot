from flask import Blueprint, request, jsonify
from app import db, redis
from app.models import Question, Answer, Message, User, UserActivity

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

    # 处理新成员加入
    new_chat_member = data.get('new_chat_member')
    if new_chat_member:
        return jsonify({'text': 'Welcome to the group!'})

    return jsonify({'status': 'ok'})

#签到功能
@bp.route('/checkin', methods=['POST'])
def checkin():
    data = request.get_json()
    user_id = data.get('user_id')
    user = User.query.get(user_id)

    if user:
        user.points += 10
        activity = UserActivity(user_id=user.id, activity_type='checkin')
        db.session.add(activity)
        db.session.commit()
        return jsonify({'status': 'success', 'points': user.points})
    return jsonify({'status': 'error', 'message': 'User not found'})


#检查关键词
def check_keyword(content):
    # Implement keyword check logic
    question = Question.query.filter_by(content=content).first()
    if question:
        answer = Answer.query.filter_by(question_id=question.id).first()
        if answer:
            return answer.content
    return "I don't understand"
