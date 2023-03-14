import bluetooth

server_address = "B8:27:EB:E0:63:91"  # replace with the MAC address of the Linux server
port = 1

client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect((server_address, port))

while True:
    message = input()

    client_socket.send(message)

    recipt = client_socket.recv(1024)
    print(recipt)
    recipt = client_socket.recv(1024)
    print(recipt)


client_socket.close()
