# -*- coding: utf-8 -*-

import socket, time, pickle, time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 5050))

clients = []
print('Start Server')
print('Ждем подключения клиентов')
print('')
while 1:
    data, addres = sock.recvfrom(1024)
    pack = pickle.loads(data)
    print('Adres', addres, 'send:', pack)

    if addres not in clients:
        print('Connecting client ', addres)
        clients.append(addres)
#        for i in range(8):
#            print('. ', end='')
#            time.sleep(0.1)
#        print('')
        print('Connected clients: ', clients)

    for client in clients:
        if client != addres:
            sock.sendto(data, client)
            print(client, 'Send', pickle.loads(data), 'to', client)
#            print('')
    time.sleep(1)
