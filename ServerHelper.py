import re
import os

def extract_header(data):
    headers = list()
    lines = data.split('\\r\\n')
    matcher = re.search("b'(\w+)\s(\/\w*[\/\w]*(\.\w+)*)", lines[0])
    print(lines[0])
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

def build_error_response(path, error):
    return ''.join(['HTTP', path,'1.1', ' 404 ', error, '\r\n'])
