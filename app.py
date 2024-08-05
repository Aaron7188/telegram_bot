import os

import requests as requests
import telegram
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from telegram import ChatPermissions
from telegram.ext import Updater, Filters

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#自动回复
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = relationship("Question", back_populates="answers")
    answer = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), nullable=False)

Question.answers = relationship("Answer", order_by=Answer.id, back_populates="question")

@app.route('/add_question', methods=['POST'])
def add_question():
    data = request.json
    question = Question(question=data['question'], language=data['language'])
    db.session.add(question)
    db.session.commit()
    return jsonify({'message': 'Question added successfully'})

@app.route('/add_answer', methods=['POST'])
def add_answer():
    data = request.json
    answer = Answer(question_id=data['question_id'], answer=data['answer'], language=data['language'])
    db.session.add(answer)
    db.session.commit()
    return jsonify({'message': 'Answer added successfully'})

@app.route('/get_answer', methods=['GET'])
def get_answer():
    question_text = request.args.get('question')
    language = request.args.get('language')
    question = Question.query.filter_by(question=question_text, language=language).first()
    if question:
        answer = Answer.query.filter_by(question_id=question.id, language=language).first()
        if answer:
            return jsonify({'answer': answer.answer})
    return jsonify({'answer': 'No answer found'})

def start(update, context):
    update.message.reply_text('Hi! I am your bot. How can I help you today?')

def handle_message(update, context):
    user_message = update.message.text
    response = requests.get('http://localhost:5000/get_answer', params={'question': user_message, 'language': 'en'})
    answer = response.json().get('answer', 'No answer found')
    update.message.reply_text(answer)


#群管理功能
def welcome(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome!")

def kick_user(update, context):
    if len(context.args) == 1:
        user_id = int(context.args[0])
        context.bot.kick_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Kicked user {user_id}")

def ban_user(update, context):
    if len(context.args) == 1:
        user_id = int(context.args[0])
        context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Banned user {user_id}")

def mute_user(update, context):
    if len(context.args) == 1:
        user_id = int(context.args[0])
        permissions = ChatPermissions(can_send_messages=False)
        context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user_id, permissions=permissions)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Muted user {user_id}")


def main():
    updater = telegram.ext.Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(telegram.ext.CommandHandler("start", start))
    dp.add_handler(telegram.ext.MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(telegram.ext.CommandHandler("welcome", welcome))
    dp.add_handler(telegram.ext.CommandHandler("kick", kick_user))
    dp.add_handler(telegram.ext.CommandHandler("ban", ban_user))
    dp.add_handler(telegram.ext.CommandHandler("mute", mute_user))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    db.create_all()
    main()
