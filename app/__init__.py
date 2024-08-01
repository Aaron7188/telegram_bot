from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import os

# 加载 .env 文件
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
redis = FlaskRedis()

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    redis.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)

    # 初始化定时任务
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=send_scheduled_message, trigger="interval", seconds=60)
    scheduler.start()


    return app


def send_scheduled_message():
    # 在这里定义定时发送消息的逻辑
    print("Sending scheduled message")