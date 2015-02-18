__author__ = 'admin'

from pretenders.client.http import HTTPMock
import json
import os
from glob import glob
import pretender_defaults
import pretend_helpers

def start_stubbing(port_number = pretender_defaults.portno,stub_name = 'webstub'):

    # Stopping and Starting the pretenders
    pretend_helpers.stop_pretend()
    pretend_helpers.start_pretend(port_number)

    stub_files_path = pretender_defaults.stub_files_path if os.environ.has_key("stub_files_path")==False else  os.environ["stub_files_path"]
    print(stub_files_path)

    # create a HTTPMock Object
    mock = HTTPMock('127.0.0.1',port_number, name=stub_name)
    mock.reset()
    mock.when('GET /thing*').reply('Hello',status=202,times=20)                  # sample web request stub

    for stub_file in glob(stub_files_path+'*.json'):
        with open(stub_file) as fp:
            stubs = json.load(fp)
        print(stub_file)
        for stub in stubs:
            # Setting the default values for the request entities
            headers = {}
            response_headers = {}
            response_body =  pretender_defaults.response_body
            response_status = pretender_defaults.response_status
            body = pretender_defaults.request_body
            method = pretender_defaults.method
            url = pretender_defaults.url
            if (stub.has_key('request')):
                url = pretend_helpers.get_url_from_json(stub['request'])                                                    # get the URL from the json
                method = stub['request']['method'] if stub['request'].has_key('method') else pretender_defaults.method      # get the request method from the json
                body = pretend_helpers.get_body_from_json(stub['request'])                                                  # get the request body from the json
                headers = pretend_helpers.get_headers_from_json(stub['request'])                                            # get the request headers from the json

            if (stub.has_key('response')):
                response_body = stub['response']['body'] if stub['response'].has_key('body') else pretender_defaults.response_body                   # get the response body from the json
                response_status = stub['response']['status'] if stub['response'].has_key('status') else pretender_defaults.response_status           # get the response status from the json
                response_headers =  pretend_helpers.get_response_headers_from_json(stub['response'])                                                 # get the response headers from the json

            mock.when(method+' '+url, headers=headers ,body=body).reply(response_body,headers=response_headers,status=response_status,times=20)
            print(method +' '+url+str(headers)+body+response_body+str(response_status))

def stop_stubbing():
    pretend_helpers.stop_pretend()