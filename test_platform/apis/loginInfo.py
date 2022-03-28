#encoding=utf8

from test_platform.apis import api
from flask import request, jsonify, current_app
from test_platform.models import Module, OpeSystems, FuncModule
from test_platform import db

# 获取一级模块
@api.route('/getfirstlist', methods = ['POST'])
def getFirst():
    """
    获取主页面一级模块
    :return: 一级模块id、名称
    """
    ret = dict()
    content = list()

    modules = Module.query.all()
    for module in modules:
        m_id = module.id
        m_name = module.name
        temp = dict()
        temp['first_id'] = m_id
        temp['first_name'] = m_name
        content.append(temp)
    ret['status'] = '0'
    ret['data'] = content
    ret['msg'] = ''

    return jsonify(ret)


# 根据一级模块id，获取二级模块
@api.route('/getsecondlist', methods = ['POST'])
def getSecond():
    '''
    接收参数: firstId  一级分类id
    :return: 二级模块名称、id
    '''

    req_data = request.get_json()
    firstId = req_data.get('firstId')
    if firstId is None:
        return jsonify(status='1', msg='请检查参数')

    sys = OpeSystems.query.filter_by(module_id=firstId).all()
    data = []
    for i in sys:
        temp = dict()
        temp['second_id'] = i.id
        temp['second_name'] = i.name
        data.append(temp)

    return jsonify(status='0', msg='', data = data)


# 根据二级模块id，获取三级模块
@api.route('/getthirdlist', methods = ['POST'])
def getThird():
    '''
    接收参数: secondId  二级分类id
    :return: 三级模块名称、id
    '''

    req_data = request.get_json()
    secondId = req_data.get('secondId')
    if secondId is None:
        return jsonify(status='1', msg='请检查参数')

    sys = FuncModule.query.filter_by(system_id=secondId).all()
    data = []
    for i in sys:
        temp = dict()
        temp['third_id'] = i.id
        temp['third_name'] = i.name
        data.append(temp)

    return jsonify(status='0', msg='', data = data)



# 主页
@api.route('/')
def index():
    print(123)
    return current_app.send_static_file('html/index.html')




