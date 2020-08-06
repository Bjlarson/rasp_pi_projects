import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.1.24",1234))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    
    msg = "Welcome to the server!"
    
    clientsocket.send(bytes(msg, "utf-8"))
    
    while True:
        incomeing = clientsocket.recv(16).decode()
        print (incomeing)