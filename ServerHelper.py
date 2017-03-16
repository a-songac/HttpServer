import re
import os
from datetime import datetime

def extract_request(requestLine):
    headers = list()
    matcher = re.search("(\w+)\s(\/\w*[\/\w]*(\.\w+\/?)*)", requestLine)
    headers.append(matcher.group(1))
    headers.append(matcher.group(2))

    return headers

def extract_body(data):
    fullRequest = data.split('\r\n\r\n')
    if len(fullRequest) > 1:
        return re.sub('\r\n', '', fullRequest[1])
    return None

def extract_raw_headers(data):
    return data.split('\\r\\n\\r\\n')[0]

def extract_headers(data):
    headerBlock = data.split('\r\n\r\n')
    headers = headerBlock[0].split('\r\n')
    headerMap = {}
    
    for header in headers :
        headerArr = header.split(":")
        if len(headerArr) > 1:
            headerMap[headerArr[0].strip()] = headerArr[1].strip()
        
    return headerMap
    
    

def get_file_content(path):
    f =  open(path, 'r') 
    data = f.read()
    f.close()
    return data


def list_directory(path):
    if(os.path.isdir(path)):
        alist= os.listdir(path)
        finalList = []
        for i in alist:
            prepend = 'f'
            if os.path.isdir(''.join([path, i])) :
                prepend = 'd'
            finalList.append(''.join([prepend, ' ', i]))
        return finalList
    else:
        raise Exception('Directory not found')

def build_error_response(error, status = 404):
    return ''.join(['HTTP/1.1 ', str(status), ' ', error, '\r\n',
                    'Date: ', datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"), '\r\n',
                    'Content-Type: text/html; charset=utf-8\r\n',
                    'Content-Length: ', str(len(error.encode('utf-8'))), '\r\n\r\n',
                    error])

def build_success_response(data):
    return ''.join(['HTTP/1.1 200 OK \r\n',
                    'Date: ', datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"), '\r\n',
                    'Content-Type: text/html; charset=utf-8\r\n',
                    'Content-Length: ', str(len(data.encode('utf-8'))), '\r\n\r\n',
                    data])
    
def write_request_body(path, data):
    f = open(path, 'w')
    f.write(data+'\n')
    f.close()
    
    
