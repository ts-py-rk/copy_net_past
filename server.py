# -*- coding: utf-8 -*-

import socket, time, pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 5050))

clients = []
print('Start Server')
print('Ждем подключения клиентов\n')

while 1:
    data, addres = sock.recvfrom(1024)
    print('1', ',addres', addres, 'send data:', data)
    pack = pickle.loads(data)
    print('2 Addres', addres, 'send pack:', pack)
    print('3', clients)
    if addres not in clients:
        print('4', addres)
        print('5 Connecting client ', addres)
        clients.append(addres)
        print('6 Connected clients: ', clients)
    print('7', clients)
    for client in clients:
        print('8', client)
        if client != addres:
            print('9', client, 'data:', data, 'to', client)
            sock.sendto(data, client)
            print('10', client, 'Send', pickle.loads(data), 'to', client)
    time.sleep(1)
