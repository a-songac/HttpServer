#!/usr/bin/python3
import os
import socket
import threading
import ArgsParser
import ServerHelper

CONTENT_LENGTH = "Content-Length"
BUFF_SIZE = 1024

def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Server is listening at', port)
        while True:
            conn, addr = listener.accept() #blocked until receives connection request 
            conn.settimeout(1.0)
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    path = os.getcwd()
    print('New client from', addr)
    try:
        clientDataBytes =  conn.recv(BUFF_SIZE)
        clientData = requestData = str(clientDataBytes)
        print(clientData)
        headers = ServerHelper.extract_headers(clientData)
        
        bodyLength = 0
        if CONTENT_LENGTH in headers :
            bodyLength = int(headers[CONTENT_LENGTH])
                             
        rawHeadersLen = len(ServerHelper.extract_raw_headers(clientData))   
        print("raw headers str: ", rawHeadersLen)
        print("body: ", bodyLength)
        print("full: ", len(clientDataBytes))
        while len(clientDataBytes) >= BUFF_SIZE:
            print("looping")
            try:
                clientDataBytes = conn.recv(BUFF_SIZE)
            except socket.timeout:
                break
            requestData += str(clientDataBytes)
        
        requestLine = list()
        requestLine = ServerHelper.extract_request(requestData)
        verb = requestLine[0]
        path = path + requestLine[1]
        body = ServerHelper.extract_body(requestData)

        data = ''
        try:
            if(verb == 'GET'):
                if(path[len(path)-1] == '/'):
                    directories = ServerHelper.list_directory(path)

                    for directory in directories:         
                        data = ''.join([data, directory, '\r\n'])
                else:
                    data = ServerHelper.get_file_content(path)
            elif verb == 'POST':
                if body is not None:
                    print(body)
                    
            
            data = ServerHelper.build_success_response(data)
                
        except OSError:
            data = ServerHelper.build_error_response('File does not exists')
        except Exception as error:
            data = ServerHelper.build_error_response(error.args[0])
        finally:
            conn.sendall(data.encode())
    finally:
        conn.close()


# Usage python echoserver.py [--port port-number]
parser = ArgsParser.generateArgParsers()
args = parser.parse_args()
run_server('', args.port)
