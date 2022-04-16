#encoding=utf8
from locust import HttpUser, between, task
import os
import jmespath



class StressTest(HttpUser):
	wait_time = between(0,0)
	host=""
	@task(1)
	def run0(self):
		url = "http://127.0.0.1:5000/loginInfo/getthirdlist"
		with self.client.post("http://127.0.0.1:5000/loginInfo/getthirdlist", headers = {'contentType': 'application/json'}, json = {'secondId': '1'}, catch_response=True) as res:
			if res.status_code==200:
				try:
					assert res.json()["status"] == "0"
					res.success()
				except:
					res.failure(res.text)
			else:
				res.failure(res.text)
	@task(1)
	def run1(self):
		url = "http://192.168.0.105:7079/usercenter/webapi/tool/getUserPermissionInfo?jobNumber=10001897"
		with self.client.get("http://192.168.0.105:7079/usercenter/webapi/tool/getUserPermissionInfo?jobNumber=10001897", headers = {}, catch_response=True) as res:
			if res.status_code==200:
				try:
					assert res.json()["code"] == "0"
					res.success()
				except:
					res.failure(res.text)
			else:
				res.failure(res.text)


