from test_platform.apis import api
from flask import request, jsonify
from test_platform.models import TestCase

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
        temp['caseName'] = obj.name
        temp['casePath'] = obj.path
        temp['caseHeader'] = obj.header
        temp['caseParam'] = obj.param
        temp['caseData'] = obj.data
        temp['caseDataType'] = obj.dataType
        temp['caseOrder'] = obj.caseOrder
        data.append(temp)

    return jsonify(status='0', msg='', data = data)






# 保存测试用例
@api.route('/saveCases', methods=['POST'])
def savecases():
    pass

