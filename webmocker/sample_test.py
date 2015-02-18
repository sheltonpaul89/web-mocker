__author__ = 'admin'
from webmocker import mock_server
import unittest
import requests
import os

class WebTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ["stub_files_path"] = 'web_stubs/'
        mock_server.start_stubbing(stub_name='shel',port_number=8001)

    @classmethod
    def tearDownClass(cls):
        # time.sleep(100000)
        mock_server.stop_stubbing()

    def test_case1(self):
        capture = {}
        captured = requests.get('http://127.0.0.1:8001/mockhttp/shel/with/query?search=Some text&searchtext=sheltonpaulinfant')
        print(captured.status_code)
        print(captured.text)
        self.assertEqual(captured.status_code, 230)

        # captured = requests.get('http://localhost:8998/address/12')
        # print(captured.status_code)
        # status_code(captured.text)

    def test_case2(self):
        capture = {}
        payload = "<status>OK</status>";
        captured = requests.post('http://127.0.0.1:8001/mockhttp/shel/with/body', data=payload)
        print(captured.status_code)
        print(captured.text)
        self.assertEqual(captured.status_code, 270)
        self.assertEqual(captured.text, "This is a POST Request")

    def test_case3(self):
        capture = {}
        captured = requests.get('http://127.0.0.1:8001/mockhttp/shel/with/query/extra/path?search=Some text&searchtext=sheltonpaulinfant')
        print(captured.status_code)
        print(captured.text)
        self.assertEqual(captured.status_code, 230)
        self.assertEqual(captured.text, "This is a URL Path")

    def test_case4(self):
        capture = {}
        captured = requests.get('http://127.0.0.1:8001/mockhttp/shel/some/thing')
        print(captured.headers)
        print(captured.text)
        self.assertEqual(captured.status_code, 210)
        self.assertEqual(captured.text,"Hello world! This request has respnse headers")
        self.assertEqual(captured.headers["header1"],'respose Headers')
        self.assertEqual(captured.headers["content-type"],'text/plain')
        print(captured.headers)

    def test_case5(self):
        capture = {}
        headers = {'content-type': 'text/xml','Accept' : 'text/json','ramp' : 'thissample'}
        captured = requests.post('http://127.0.0.1:8001/mockhttp/shel/with/headers',headers = headers)
        print(captured.status_code)
        print("Response Text : " +captured.text)
        self.assertEqual(captured.status_code, 250)
        self.assertEqual(captured.text, "This request URL has headers")


if __name__ == '__main__':
    unittest.main()
