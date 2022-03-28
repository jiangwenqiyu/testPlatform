#encoding=utf8

import requests

def exeCases(cases,exeType, db):
    '''

    :param cases: ORM用例模型, 列表
    :param exeType: 执行类型   1 单条  2  批量
    :return:
    '''

    if exeType == 1:
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
                return res.text
            elif reqType.upper() == 'POST':
                if dataType.upper() == 'JSON':
                    res = requests.post(url, headers = header, params=param, json=data)
                    return res.text
                elif dataType.upper() == 'DATA':
                    res = requests.post(url, headers = header, params=param, data=data)
                    return res.text
                else:
                    return '不支持的入参类型'

            else:
                return '不支持的请求类型'
        except Exception as e:
            return str(e)

    else:
        return '789'


