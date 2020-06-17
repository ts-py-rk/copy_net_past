# -*- coding: utf-8 -*-

import socket, time, pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 5050))

clients = []
print('Start Server')
print('Ждем подключения клиентов\n')

while 1:
    data, addres = sock.recvfrom(1024)
    pack = pickle.loads(data)
    print('Addres', addres, 'send:', pack)

    if addres not in clients:
        print('Connecting client ', addres)
        clients.append(addres)
        print('Connected clients: ', clients)

    for client in clients:
        if client != addres:
            sock.sendto(data, client)
            print(client, 'Send', pickle.loads(data), 'to', client)
    time.sleep(1)
