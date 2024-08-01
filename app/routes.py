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

#添加获取用户和用户活动的API端点
@bp.route('/admin/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/admin/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'status': 'error', 'message': 'User not found'})

@bp.route('/admin/user/<int:user_id>/activities', methods=['GET'])
def get_user_activities(user_id):
    activities = UserActivity.query.filter_by(user_id=user_id).all()
    return jsonify([activity.to_dict() for activity in activities])


#检查关键词
def check_keyword(content):
    # Implement keyword check logic
    question = Question.query.filter_by(content=content).first()
    if question:
        answer = Answer.query.filter_by(question_id=question.id).first()
        if answer:
            return answer.content
    return "I don't understand"
