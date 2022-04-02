#encoding=utf8

from test_platform.apis import api_case
from flask import request, jsonify
from test_platform.models import TestCase
from test_platform import db
import json
from test_platform.utils.run_test_case import exeCases

# 获取测试用例
@api_case.route('/getCases', methods=['POST'])
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
        temp['status'] = obj.status
        temp['dataReqType'] = obj.reqType
        temp['updateTime'] = obj.updateTime
        temp['res'] = str(obj.res)
        data.append(temp)

    return jsonify(status='0', msg='', data = data)


# 保存测试用例
@api_case.route('/saveCases', methods=['POST'])
def savecases():
    req_data_list = request.get_json()
    for req_data in req_data_list:
        updateType = req_data.get('updateType')
        thirdId = req_data.get('thirdId')
        content = req_data.get('content')
        caseId =  req_data.get('id')
        if updateType == 1: # 插入新数据
            temp = dict()
            temp['user_id'] = 1  # 用户id暂时写死
            temp['caseOrder'] = content[0]
            temp['name'] = content[1]
            temp['path'] = content[2]
            temp['dataType'] = content[6]
            temp['reqType'] = content[7]
            temp['func_module_id'] = thirdId
            try:
                temp['header'] = json.loads(content[3])
                temp['param'] = json.loads(content[4])
                temp['data'] = json.loads(content[5])
                temp['exp_result'] = json.loads(content[8])
                if content[9] == '' or content[9] == None:
                    temp['need_save'] = content[9]
                else:
                    temp['need_save'] = json.loads(content[9])
            except Exception as e:
                print(e)
                return jsonify(status='1', msg='请检查json格式')

            try:
                case = TestCase(**temp)
                db.session.add(case)
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify(status='1', msg='数据库更新失败')


        else:    # 更新数据

            temp = dict()
            temp['caseOrder'] = content[0]
            temp['name'] = content[1]
            temp['path'] = content[2]
            temp['dataType'] = content[6]
            temp['reqType'] = content[7]
            try:
                temp['header'] = json.loads(content[3])
                temp['param'] = json.loads(content[4])
                temp['data'] = json.loads(content[5])
                temp['exp_result'] = json.loads(content[8])
                if content[9] == '' or content[9] == None:
                    temp['need_save'] = content[9]
                else:
                    temp['need_save'] = json.loads(content[9])
            except Exception as e:
                return jsonify(status='1', msg='请检查json格式')
            try:
                TestCase.query.filter_by(id=caseId).update(temp)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
                return jsonify(status='1', msg='数据库更新失败')


    return jsonify(status='0', msg='')


# 执行测试用例
@api_case.route('/runCases', methods=['POST'])
def runTestCase():
    '''
    接收测试用例[用例id]
    用例表中，标记状态  1  进行中   0  就绪
    如果传进来的用例，只要有一个在执行中，不允许执行，返回前端，有用例在进行中，不允许批量执行
    判断是单次执行还是批量执行，单次执行，只进记录表； 批量执行，更新用例表状态，生成单号，插入记录表，后台执行，执行后也需要更新用例表状态
    :return:
    '''
    req_data = request.get_json()
    # 先判断，用例表是否有进行中的
    cases = TestCase.query.filter(TestCase.id.in_(req_data)).order_by(TestCase.caseOrder).all()
    if cases == []:
        return jsonify(status='1', msg='没有查询到用例')

    for i in cases:
        if i.status == 1:
            return jsonify(status='1', msg='有进行中的用例')



    if len(req_data) == 1:  # 单条执行，返回  返回值  状态   执行时间
        return jsonify(status='0', msg = exeCases(cases, 1, db))
    else:
        return jsonify(status='0', msg=exeCases(cases, 2, db))


# 删除测试用例
@api_case.route('/deletecase', methods = ['POST'])
def deletecase():
    '''
    :param id:
    :return:
    '''

    req_data = request.get_json()
    id = req_data.get('id')
    try:
        case = TestCase.query.filter_by(id=id).delete()
    except:
        return jsonify(status='1', msg='访问数据库失败')

    db.session.commit()
    return jsonify(status='0', msg='删除成功')







