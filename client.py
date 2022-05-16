# -*- coding: utf-8 -*-
import pyperclip
import time
import socket
import pickle
import threading
import sys
import select


# функция обертка для запуска потоков
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper


# функция подключения к указанному серверу
def input_server(ip, port, sec):
    ip_def = ip
    port_def = port
    print(f'Начинается автоматическое подключение к {ip}:{port}\nНажмите '
          f'Enter для ручной настройки подключения в течении {sec} секунд)')
    rlist, _, _ = select.select([sys.stdin], [], [], sec)
    if rlist:
        ip = sys.stdin.readline()
        if ip == '\n':
            ip = input(' Введите IP: ')
            exit = True
            while exit:
                try:
                    port = int(input(' Введите порт: '))
                except ValueError:
                    print('Неверный ввод порта')
                else:
                    exit = False
            print(f'Подключаемся к {ip}:{port} ')
        else:
            ip = ip_def
            port = port_def
    global server, sor
    server = ip, port
    sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sor.bind(('', 0))


# функция отправки буфера на сервер
@thread
def send_bufer(second):
    local = threading.local()
    local.local_bufer = set()
    while True:
        local.local_bufer_now = {pyperclip.paste()}
        local.start_len = len(local.local_bufer)
        if local.local_bufer_now not in local.local_bufer:
            local.local_bufer = local.local_bufer | local.local_bufer_now
            local.add_len = len(local.local_bufer)
        if local.start_len != local.add_len:
            print('Send to server', local.local_bufer_now)
            local.pack = pickle.dumps(local.local_bufer_now, protocol=2)
            sor.sendto(local.pack, server)
            local.local_bufer = local.local_bufer & local.local_bufer_now
        time.sleep(second)


# функция бесконечного цикла приема сетевого буфера
@thread
def net_in_loc():
    while True:
        data = sor.recv(1024)
        net_bufer = pickle.loads(data)
        if net_bufer not in bufer:
            for i in net_bufer:
                print(f'{i} копируем в буфер')
                pyperclip.copy(i)
        time.sleep(1)


start_message = 'Start client'
server_ip = '192.168.88.210'
server_port = 666
period = 3

print(start_message)
hello = socket.gethostbyname(socket.gethostname())
pyperclip.copy(hello)                           # стартовый пакет c ip клиента
input_server(server_ip, server_port, period)    # подключаемся к серверу
send_bufer(period)                              # запуск потока отправки буфера
bufer = set()                                   # создание множества для буфера
bufer.add(pyperclip.paste())                    # добавляем во множество буфер
net_in_loc()                                    # запускаем  в потоке
