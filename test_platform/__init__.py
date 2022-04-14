#encoding=utf8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs import env_map
import redis



db = SQLAlchemy()
redis_store = None

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(env_map[env])

    db.init_app(app)

    global redis_store
    redis_store = redis.StrictRedis(host = env_map[env].REDIS_HOST, port = env_map[env].REDIS_PORT)

    # 注册蓝图
    from test_platform.apis import  api, api_case, api_login
    app.register_blueprint(api, url_prefix = '/loginInfo')
    app.register_blueprint(api_case, url_prefix = '/case')
    app.register_blueprint(api_login)

    return app