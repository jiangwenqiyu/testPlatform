#encoding=utf8
import re
import requests
import jmespath
import time
import json
from test_platform.models import TestCase, ExeCaseRecord, ExeCaseRecordDetail, WaitExeCase
from test_platform import redis_store, constance, db
from sqlalchemy import and_
from test_platform.utils.extractFuncs import ishave

def exeCases(cases,exeType, db):
    '''

    :param cases: ORM用例模型, 列表
    :param exeType: 执行类型   1 单条  2  批量
    :return: 成功 res, updateTime;  失败  e
    '''

    if exeType == 1:
        # 单条，不需要考虑保存接口数据
        url = cases[0].path
        header = cases[0].header
        param = cases[0].param
        data = cases[0].data
        dataType = cases[0].dataType
        reqType = cases[0].reqType
        exp_result = cases[0].exp_result
        need_save = cases[0].need_save

        try:
            if reqType.upper() == 'GET':
                res = requests.get(url, headers = header, params=param)
                for key in exp_result:
                    result = jmespath.search(key, res.json())
                    assert result == exp_result[key],'期望值:{}\n实际值:{}'.format(exp_result[key], result)


                return res.text
            elif reqType.upper() == 'POST':
                if dataType.upper() == 'JSON':
                    res = requests.post(url, headers = header, params=param, json=data)
                    for key in exp_result:
                        result = jmespath.search(key, res.json())
                        assert result == exp_result[key],'期望值:{}\n实际值:{}'.format(exp_result[key], result)


                    return res.text
                elif dataType.upper() == 'DATA':
                    res = requests.post(url, headers = header, params=param, data=data)
                    for key in exp_result:
                        result = jmespath.search(key, res.json())
                        assert result == exp_result[key],'期望值:{}\n实际值:{}'.format(exp_result[key], result)


                    return res.text
                else:
                    return '不支持的入参类型'

            else:
                return '不支持的请求类型'
        except Exception as e:
            return str(e)

    else:
        # 批量执行，直接先插入待执行表，后台执行


        try:
            # 更新用例表，status，为执行中
            caseids = []
            for case in cases:
                caseids.append(case.id)

            TestCase.query.filter(TestCase.id.in_(caseids)).update({'status': 1})

            # 生成单据号，插入单据表
            record = 'RECORD{}'.format(int(time.time()))
            db.session.add(ExeCaseRecord(recordNo = record))

            # 每一条用例，插入到执行记录明细表
            for case in cases:
                temp = dict()
                temp['recordNo'] = record
                temp['caseId'] = case.id
                temp['caseName'] = case.name
                temp['data'] = case.data
                temp['status'] = 0
                temp['env_id'] = 0
                db.session.add(ExeCaseRecordDetail(**temp))

                # 每一条用例，插入到待执行表        后台任务扫描待执行表，执行完一条，更新明细表，用例表，删除待执行表
                temp.clear()
                temp['recordNo'] = record
                temp['caseId'] = case.id
                temp['caseOrder'] = case.caseOrder
                db.session.add(WaitExeCase(**temp))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return '执行失败，{}'.format(e)

        BatchExeCases().run()  # 后台执行
        return '执行成功，刷新查看后台执行结果'



class BatchExeCases:

    def run(self):
        # 从待执行表获取用例
        w_cases = WaitExeCase.query.outerjoin(TestCase, TestCase.id == WaitExeCase.caseId).order_by(and_(WaitExeCase.recordNo, WaitExeCase.caseOrder)).all()
        for wcase in w_cases:
            case = TestCase.query.filter_by(id=wcase.caseId).first()
            self.exeCase(case)


    def exeCase(self, case):
        # param和data，清洗出需要获取上个接口的数据
        param = self.extractData(case.param, case.func_module_id,)
        data = self.extractData(case.data, case.func_module_id)

        if param == '提取上一接口数据失败' or data == '提取上一接口数据失败':
            self.failure(case, '提取上一接口数据失败', data)
            return
        data = ishave(data)

        try:
            if case.reqType.upper() == 'GET':
                res = requests.get(case.path, headers = case.header, params=param)
            elif case.reqType.upper() == 'POST':
                if case.dataType.upper() == 'DATA':
                    res = requests.post(case.path, headers = case.header, params=param, data=data)
                elif case.dataType.upper() == 'JSON':
                    res = requests.post(case.path, headers = case.header, params=param, json=data)
        except Exception as e:
            self.failure(case, str(e), data)
        else:
            # 请求成功，断言，通过之后把res存入redis，断言失败执行failure
            try:
                for jmes in case.exp_result:
                    assert res.json()[jmes] == case.exp_result[jmes], '断言失败\n断言数据:{}\n期望:{}\n实际:{}'.format(jmes, case.exp_result[jmes], res.json()[jmes])
            except Exception as e:
                self.failure(case, res.text, data)
            else:
                self.success(case, res, data)


    def extractData(self, data, module_id):
        # 数据格式  #用例序号.jmespath#
        # redis格式：模块id_用例序号:值
        pat = '#\d+\..*?#'
        data = json.dumps(data, ensure_ascii=False)
        result = re.findall(pat, data)
        if len(result) == 0:
            return json.loads(data)
        else:
            try:
                for value in result:
                    value1 = value.replace('#', '')
                    caseorder = re.findall('(^\d+)\.', value1)[0]
                    jmespath_express = value1.replace(caseorder + '.', '')
                    last_res = json.loads(redis_store.get('{}_{}'.format(module_id, caseorder)))
                    last_value = jmespath.search(jmespath_express, last_res)
                    data = data.replace(value, last_value)
                return json.loads(data)
            except:
                return '提取上一接口数据失败'


    def failure(self, case, e, data):
        # 更新用例表  status  3  res  e
        TestCase.query.filter_by(id=case.id).update({'status':3, 'res':e  })
        # 更新批次明细表  consume  res  success 2
        ExeCaseRecordDetail.query.filter_by(caseId=case.id).update({'status':2, 'consume':'0', 'res':e})
        # 从待执行表删除
        WaitExeCase.query.filter_by(caseId=case.id).delete()
        db.session.commit()

        return

    def success(self, case, res, data):
        # 把res存入redis, 格式  模块id_order:res
        redis_store.setex('{}_{}'.format(case.func_module_id, case.caseOrder), constance.REDIS_EXPIRE_TIME, json.dumps(res.json(), ensure_ascii=False))
        # 更新用例表  status  2  res
        TestCase.query.filter_by(id=case.id).update({'status':2, 'res':res.json()})
        # 更新批次明细表  consume  res  success 1
        ExeCaseRecordDetail.query.filter_by(caseId=case.id).update({'status':1, 'consume':res.elapsed.total_seconds(), 'res':res.json()})
        # 从待执行表删除
        WaitExeCase.query.filter_by(caseId=case.id).delete()
        db.session.commit()
        return










