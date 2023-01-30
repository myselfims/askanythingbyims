import socket

ip = socket.gethostname()
ipadd = socket.gethostbyname(ip)
print(ipadd)