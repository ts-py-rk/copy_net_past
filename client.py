import pyperclip, time, socket, pickle, threading, sys, select

#                                           # функция обертка для запуска потоков
def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper

#                                           # функция подключения к указанному серверу
def input_server(ip, port, sec):

    ip_def = ip
    port_def = port
    print(f'Идет подключение к {ip}\nНажмите Enter для подключения к другому серверу)')

    rlist, _, _ = select.select([sys.stdin], [], [], sec)
    if rlist:
        ip = sys.stdin.readline()
        if ip == '\n':
            ip = input(' Введите IP: ')
            port = int(input(' Введите порт:' ))
            print(f'Подключаемся к {ip}:{port} ')
        else:
            ip = ip_def
            port = port_def

    global server, sor
    server = ip, port
    sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sor.bind(('', 0))

@thread                                     # функция отправки буфера на сервер
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
            print('Sending', local.local_bufer_now, 'to server')
            local.pack = pickle.dumps(local.local_bufer_now, protocol=2)
            sor.sendto(local.pack, server)
            local.local_bufer = local.local_bufer & local.local_bufer_now
        time.sleep(second)

@thread                                     # функция бесконечного цикла приема сетевого буфера
def net_in_loc():
    while True:
        data = sor.recv(1024)
        net_bufer = pickle.loads(data)
        if net_bufer not in bufer:
            abc = str(net_bufer)
            bca = abc[2:len(abc) - 2]
            pyperclip.copy(bca)
            print(bca, 'add in bufer')
        time.sleep(1)

###################################################################################################

print('Start client')                       # стартовое приветствие
pyperclip.copy('Hello! I am macbook!')      # стартовый пакет будет таким

input_server('192.168.1.11', 5050, 3)                              # подключаемся к указанному серверу

send_bufer(1)                               # запуск потока отправки буфера на сервер

bufer = set()                               # создание множества для буфера
bufer.add(pyperclip.paste())                # добавляем во множество буфер обмена

net_in_loc()                                # запускаем  в потоке

