#!/usr/bin/python3
import os
import socket
import threading
import ArgsParser
import ServerHelper


def run_server(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen(5)
        print('Server is listening at', port)
        while True:
            conn, addr = listener.accept() #blocked until receives connection request 
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()


def handle_client(conn, addr):
    path = os.getcwd()
    print('New client from', addr)
    try:
        while True:
            data = ''
            headers = ServerHelper.extract_header(str(conn.recv(1024)))
            verb = headers[0]
            print(headers[1])
            path = path + headers[1]

            print(path)
            try:
                if(verb == 'GET'):
                    if(path[len(path)-1] == '/'):
                        directories = ServerHelper.list_directory(path)

                        for directory in directories:         
                            data = ''.join([data, directory, '\r\n'])
                    else:
                        data = ServerHelper.get_file_content(path)
                elif verb == 'POST':
                    print("TODO")
                
                data = ServerHelper.build_success_response(data)
                    
            except OSError:
                data = ServerHelper.build_error_response('File does not exists')
            except Exception as error:
                data = ServerHelper.build_error_response(error.args[0])
            finally:
                print (data)
                conn.sendall(data.encode())
                break
    finally:
        conn.close()


# Usage python echoserver.py [--port port-number]
parser = ArgsParser.generateArgParsers()
args = parser.parse_args()
run_server('', args.port)
