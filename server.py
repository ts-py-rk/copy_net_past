# -*- coding: utf-8 -*-
import socket, time, pickle, select, sys

def start_server(port_def, sec):
    ip = socket.gethostbyname(socket.gethostname())
    print('Start server  - ', ip, ':', port_def)
    print('Press ENTER within', sec, 'seconds to set the port')
    global port
    port = port_def
    rlist, _, _ = select.select([sys.stdin], [], [], sec)
    if rlist:
        port = sys.stdin.readline()
        if port == '\n':
            exit = True
            while exit:
                try:
                    port = int(input(' Введите порт: '))
                except ValueError:
                    print('Неверный ввод порта')
                else:
                    exit = False
            print('Start server', ip, ':', port)
        else:
            port = port_def

start_server(666, 3)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', port))
clients = []
print('\nЖдем подключения клиентов\n')

while 1:
    data, addres = sock.recvfrom(1024)
    pack = pickle.loads(data)
    print(addres, 'send:', pack)
    if addres not in clients:
        print('Connecting client ', addres)
        clients.append(addres)
        print('Connected clients: ', clients)
    for client in clients:
        if client != addres:
            sock.sendto(data, client)
            print('Send to',client, ':', pickle.loads(data))
    time.sleep(1)
