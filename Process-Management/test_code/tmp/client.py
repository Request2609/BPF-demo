import socket

HOST = 'localhost'
PORT = 9999

def conn_one():
    s = socket.socket()
    s.connect((HOST, PORT))
    while True:
        msg = input('>>:').strip()
        s.send(msg.encode('utf-8'))
        data = s.recv(1024)
        print('recv:',data.encode('utf-8'))
    s.close()
conn_one()