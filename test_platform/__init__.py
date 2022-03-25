from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs import env_map



db = SQLAlchemy()


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(env_map[env])

    db.init_app(app)

    # 注册蓝图
    from test_platform.apis import  api
    app.register_blueprint(api, url_prefix = '/loginInfo')

    return app