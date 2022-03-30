#encoding=utf8

from test_platform import db
import datetime

class BaseModel:
    createTime = db.Column(db.DateTime, default=datetime.datetime.now)
    updateTime = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    id = db.Column(db.Integer, primary_key=True)


class Module(BaseModel, db.Model):
    __tablename__ = 'main_module'


    name = db.Column(db.String(20))


class OpeSystems(BaseModel, db.Model):
    __tablename__ = 'ope_systems'
    name = db.Column(db.String(20))
    module_id = db.Column(db.Integer, db.ForeignKey('main_module.id'))


class FuncModule(BaseModel, db.Model):
    __tablename__ = 'func_module'
    name = db.Column(db.String(20))
    system_id = db.Column(db.Integer, db.ForeignKey('ope_systems.id'))


class EnvConfig(BaseModel, db.Model):
    __tablename__ = 'env_config'
    name = db.Column(db.String(20), nullable=False)
    host = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String(20))
    comment = db.Column(db.String(20))


class TestCase(BaseModel, db.Model):
    __tablename__ = 'test_case'
    name = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(150), nullable=False)
    header = db.Column(db.JSON, nullable=False)
    param = db.Column(db.JSON)
    data = db.Column(db.JSON, nullable=False)
    dataType = db.Column(db.String(10), nullable=False, comment='入参类型  data json ')
    reqType = db.Column(db.String(10), nullable=False, comment='请求类型  get post ')
    exp_result = db.Column(db.JSON, nullable=False, comment='预期结果  {"jmespath表达式: 值"}')
    need_save = db.Column(db.JSON, nullable=False, comment='本次执行后需要保存的值  ["jmespath表达式"]  保存在redis中{用例id_表达式:值}')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    caseOrder = db.Column(db.Integer, nullable=False, comment='用例执行顺序')
    func_module_id = db.Column(db.Integer, db.ForeignKey("func_module.id"), comment='三级模块的id')
    status = db.Column(db.Integer, comment='当前用例状态 0 就绪  1 进行中  2  成功  3  失败')
    res = db.Column(db.JSON)



class ExeCaseRecord(BaseModel, db.Model):
    __tablename__ = 'exe_case_record'
    caseId = db.Column(db.Integer, db.ForeignKey('test_case.id'))
    consume = db.Column(db.String(10), nullable=False)
    data = db.Column(db.JSON, nullable=False)
    res = db.Column(db.JSON, nullable=False)
    success = db.Column(db.Integer, nullable=False, comment='用例执行是否成功 1 成功  2 失败')
    env_name = db.Column(db.String(10), nullable=False)


class User(BaseModel, db.Model):
    __tablename__ = 'user'
    account = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.String(20), nullable=False)


class Role(BaseModel, db.Model):
    __tablename__ = 'role'
    name = db.Column(db.String(20), nullable=False)