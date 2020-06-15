import pyperclip, time, socket, pickle, threading

#  Hello! I'm macbook!

def thread(my_func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper

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
            print('Sending', local.local_bufer_now, 'to server')
            local.pack = pickle.dumps(local.local_bufer_now, protocol=2)
            sor.sendto(local.pack, server)
            local.local_bufer = local.local_bufer & local.local_bufer_now
        time.sleep(second)

print('Start client')
pyperclip.copy('Hello! I am macbook!')
server = '192.168.1.11', 5050
sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sor.bind(('', 0))
send_bufer(1)

bbuuffeerr = set()
bbuuffeerr.add(pyperclip.paste())


while True:
    data = sor.recv(1024)
    net_bufer = pickle.loads(data)
    print(net_bufer)
    if net_bufer not in bbuuffeerr:
        abc = str(net_bufer)
        bca = abc[2:len(abc) - 2]
        pyperclip.copy(bca)
        print(bca, 'add in bufer')
    time.sleep(1)

