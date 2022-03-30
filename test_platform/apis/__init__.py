#encoding=utf8

from flask import Blueprint

api = Blueprint('loginInfo', __name__)
api_case = Blueprint('case', __name__)

from test_platform.apis import loginInfo
from test_platform.apis import testcases