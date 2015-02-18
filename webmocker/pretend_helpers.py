__author__ = 'admin'
import os
import pretender_defaults
import urllib

def start_pretend(port_number = pretender_defaults.portno):
    os.system("start /b python -m pretenders.server.server --host 127.0.0.1 --port "+ str(port_number))

def stop_pretend():
    pid = os.getpid()
    print(pid)
    os.system('taskkill /fi "PID ne '+ str(pid) +'" /im python.exe /F')

def get_rx_matches_and_doesNotMatch(body_pattern=None):
    print(body_pattern)
    if('doesNotMatch' in body_pattern):
        print(body_pattern['doesNotMatch'])
     # Todo : Add code for handling doesnt match
    return body_pattern['matches']

def get_url_from_json(request_json):
    url = request_json['url'].replace('?','\?') if request_json.has_key('url') else pretender_defaults.url
    url = request_json['urlPattern'].replace('?','\?') if request_json.has_key('urlPattern') else url
    url = request_json['urlPath'].replace('?','\?')+'(/.*)?' if request_json.has_key('urlPath') else url
    query_param = ''
    # handle query params
    if(request_json.has_key('queryParameters')):
        for param,value in request_json['queryParameters'].items():
             if isinstance(value, dict):
                if(value.has_key('contains')): query_param = query_param + ('&?|' if query_param!='' else '') + param +'=.*?'+value['contains'].replace(' ','%20')+'.*?'
                elif(value.has_key('equalto')): query_param = query_param + ('&?|' if query_param!='' else '') + param +'='+value['contains'].replace(' ','%20')
             #    Todo : Add support for mateshes
             else:
                query_param = query_param + ('&|' if query_param!='' else '') + param +'='+ value.replace(' ','%20')
        query_param = '('+ query_param + '){'+ str(len(request_json['queryParameters'])) +'}'
        print(query_param)
        url = url + ('\?' if query_param!='' else '') + query_param
    return url

def get_body_from_json(request_json):
    bodypatterns = {}
    body = request_json['body'] if request_json.has_key('body') else pretender_defaults.request_body
    if(request_json.has_key('bodyPatterns')):
        for bodypattern in request_json['bodyPatterns']:
            for key in bodypattern:
                bodypatterns[key] = bodypattern[key];
        body = get_rx_matches_and_doesNotMatch(bodypatterns)
    return body

def get_headers_from_json(request_json):
    headers={}
    if(request_json.has_key('headers')):
        for header,value in request_json['headers'].items():
             if isinstance(value, dict):
                if(value.has_key('equalTo')): headers[header] = value['equalTo']
                if(value.has_key('matches')): headers[header] = value['matches']
             #    Todo : Add support for mateshes
             else:
                headers[header] = value
    print(headers)
    return headers

def get_response_headers_from_json(response_json):
    response_headers = {}
    if(response_json.has_key('headers')):
        for header,value in response_json['headers'].items():
           response_headers[header] = value
    return response_headers