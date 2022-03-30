#encoding=utf8

import requests
import jmespath

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
        return '789'


