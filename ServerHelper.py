import re
import os
from datetime import datetime

def extract_header(data):
    headers = list()
    lines = data.split('\\r\\n')
    matcher = re.search("b'(\w+)\s(\/\w*[\/\w]*(\.\w+)*)", lines[0])
    headers.append(matcher.group(1))
    headers.append(matcher.group(2))

    return headers

def get_file_content(path):
    f =  open(path, 'r') 
    data = f.read()
    f.close()
    return data


def list_directory(path):
    if(os.path.exists(path)):
        return os.listdir(path)
    else:
        raise Exception('Directory not found')

def build_error_response(error):
    return ''.join(['HTTP/1.1 404 ', error, '\r\n',
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
