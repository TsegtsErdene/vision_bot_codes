import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 9090))
serv.listen(1)

while True:
    conn, addr = serv.accept()
    print('client connected to :', addr)
    conn.close()
