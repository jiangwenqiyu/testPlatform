from test_platform.apis import api
from flask import request, jsonify
from test_platform.models import TestCase
from test_platform import db
import json

# 获取测试用例
@api.route('/getCases', methods=['POST'])
def getcases():
    """
    接受参数： 二级模块id secondId，三级模块id thirdId
    :return: 模块对应的所有测试用例
    """
    req_data = request.get_json()
    thirdId = req_data.get('thirdId')
    if not all([thirdId]):
        return jsonify(status='1', msg='请传入三级类id')

    cases_obj = TestCase.query.filter_by(func_module_id=thirdId).order_by(TestCase.caseOrder).all()

    data = list()
    for obj in cases_obj:
        temp = dict()
        temp['caseOrder'] = obj.caseOrder
        temp['name'] = obj.name
        temp['path'] = obj.path
        temp['header'] = obj.header
        temp['param'] = obj.param
        temp['data'] = obj.data
        temp['dataType'] = obj.dataType
        temp['exp_result'] = obj.exp_result
        temp['need_save'] = obj.need_save
        temp['id'] = obj.id
        data.append(temp)

    return jsonify(status='0', msg='', data = data)


# 保存测试用例
@api.route('/saveCases', methods=['POST'])
def savecases():
    req_data_list = request.get_json()
    for req_data in req_data_list:
        updateType = req_data.get('updateType')
        thirdId = req_data.get('thirdId')
        content = req_data.get('content')
        if updateType == 1: # 插入新数据
            pass
        else:    # 更新数据
            print(content)

            temp = dict()
            temp['caseOrder'] = content[0]
            temp['name'] = content[1]
            temp['path'] = content[2]
            temp['dataType'] = content[6]
            try:
                temp['header'] = json.loads(content[3])
                temp['param'] = json.loads(content[4])
                temp['data'] = json.loads(content[5])
                temp['exp_result'] = json.loads(content[7])
                temp['need_save'] = json.loads(content[8])
            except:
                return jsonify(status='1', msg='请检查json格式')
            try:
                TestCase.query.filter_by(func_module_id=thirdId).update(temp)
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify(status='1', msg='数据库更新失败')


    return jsonify(status='0', msg='')

