import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.21", 1234))

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("New message length: ")
            msglen = int(msg)
            new_msg = False
            
        full_msg += msg.decode("utf-8")
        
        if len(full_msg) == msglen:
            print("Full msg receved")
            print(full_msg)
            new_msg = True
            full_msg = ''
        