#encoding=utf8
import re
import requests
import jmespath
import time
from test_platform.models import TestCase, ExeCaseRecord, ExeCaseRecordDetail, WaitExeCase

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

        # 更新用例表，status，为执行中
        try:
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
                temp['success'] = 0
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

        BatchExeCases().run()
        return '执行成功，刷新查看后台执行结果'



class BatchExeCases:

    def run(self):
        # 从待执行表获取用例
        w_cases = WaitExeCase.query.order_by(and_(WaitExeCase.recordNo, WaitExeCase.caseOrder)).all()


    def exeCase(self, case):
        # 判断param和data，是否有需要提取的数据


        try:
            if case.reqType.upper() == 'GET':
                res = requests.get(case.path, headers = case.header, params=case.param)
            elif case.reqType.upper() == 'POST':
                if case.dataType.upper() == 'DATA':
                    res = requests.post(case.path, headers = case.header, params=case.param, data=case.data)
                elif case.dataType.upper() == 'JSON':
                    res = requests.post(case.path, headers = case.header, params=case.param, json=case.data)
        except Exception as e:
            pass
        else:
            # 如果有需要保存的值，存入redis
            pass

    def extractData(self, data):
        # 数据格式  #用例序号.jmespath#
        # redis格式：模块id_用例序号_jmespah:值
        pat = '#\d+\..*#'










