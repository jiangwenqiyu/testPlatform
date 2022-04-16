#encoding=utf8

from flask import Blueprint
from flask_restful import Api

api = Blueprint('loginInfo', __name__)
api_case = Blueprint('case', __name__)
api_login = Blueprint('login', __name__)
api_stress = Blueprint('stress', __name__)
api_login_restful = Api(api_login)

from test_platform.apis import loginInfo
from test_platform.apis import testcases
from test_platform.apis import stressTest