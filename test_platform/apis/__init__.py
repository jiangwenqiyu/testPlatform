from flask import Blueprint

api = Blueprint('api', __name__)

from test_platform.apis import loginInfo