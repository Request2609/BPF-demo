import sys,socket, time, gevent
from gevent import socket,monkey
monkey.patch_all()
import threading

def server(port):
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        genevt.spawn(handle_request, cli)

def handle_request(conn):
    try:
        while True:
            data = conn.recv(1024)
            if  not data :
                conn.shutdown(socket.SHUT_WR)
            else:
                print('recv:',data.decode())
            conn.send('ok'.encode('utf-8'))
    except Exception as e:
        print(e)
    finally:
        conn.close()
if __name__=='__main__':
    server(9999)

