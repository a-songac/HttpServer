#!/usr/bin/python3

import socket
import threading
import ArgsParser


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
    print('New client from', addr)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
    finally:
        conn.close()


# Usage python echoserver.py [--port port-number]
parser = ArgsParser.generateArgParsers()
args = parser.parse_args()
run_server('', args.port)
