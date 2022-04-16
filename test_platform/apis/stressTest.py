#encoding=utf8
from test_platform.apis import api_stress
from flask import request, jsonify
import os
from test_platform.stressScript import stress
import threading



@api_stress.route('/generateScript', methods = ['POST'])
def test():
    '''
    接收：data:[]
    :return:
    '''
    data = request.get_json()
    urls = data['data']
    generate(urls)

    return jsonify(status = '0', msg='生成脚本成功')


@api_stress.route('/exeScript', methods = ['POST'])
def test1():
    # 重启locust服务
    os.system('')

    return jsonify(status = '0', msg='生成脚本成功')


# urls = [('http://127.0.0.1:5000/stress', 'post', 'data', '{1}', '{2}', {'int_a':789, 'int_abc':111}), ('http://192.168.0.105:7079/usercenter/webapi/tool/getUserPermissionInfo?jobNumber=10001897', 'post', 'json', '{3}', '{3}', {'string_ret.status':'2'})]

def generate(urls):

    word = ''
    word += 'from locust import HttpUser, between, task\n'
    word += 'import os\n\n'
    word += 'class StressTest(HttpUser):\n\twait_time = between(0,0)\n\thost=""\n'
    for i in range(len(urls)):
        word += '\t@task(1)\n'
        word += '\tdef run{}(self):\n'.format(i)
        word += '\t\turl = "{}"\n'.format(urls[i][0])
        if urls[i][1].lower() == 'post':
            if urls[i][2].lower() == 'data':
                word += '\t\twith self.client.post("{}", headers = {}, data = {}, catch_response=True) as res:\n'.format(urls[i][0], urls[i][3], urls[i][4])
            else:
                word += '\t\twith self.client.post("{}", headers = {}, json = {}, catch_response=True) as res:\n'.format(urls[i][0], urls[i][3], urls[i][4])
        else:
            word += '\t\twith self.client.get("{}", headers = {}, catch_response=True) as res:\n'.format(urls[i][0], urls[i][3])

        word += '\t\t\tif res.status_code==200:\n'
        word += '\t\t\t\ttry:\n'
        for key in urls[i][5]:
            __key = key.split('_')

            if __key [0] == 'int':
                word += '\t\t\t\t\tassert res.json()["{}"] == {}\n'.format(__key[1], urls[i][5][key])
            else:
                word += '\t\t\t\t\tassert res.json()["{}"] == "{}"\n'.format(__key[1], urls[i][5][key])
        word += '\t\t\t\t\tres.success()\n'
        word += '\t\t\t\texcept:\n'
        word += '\t\t\t\t\tres.failure(res.text)\n'
        word += '\t\t\telse:\n'
        word += '\t\t\t\tres.failure(res.text)\n'
    word += '\n\n'
    # word += "def main():\n"
    # word += "\tos.system('locust -f ./test_platform/stressScript/stress.py')\n"


    with open('/data/Jiangjiang/testPlatform/test_platform/stressScript/stress.py', 'w') as f:
        f.write(word)




