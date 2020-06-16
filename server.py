import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket object

host = socket.gethostbyname("192.168.172.31")

port = 697

s.bind(("192.168.178.31",port))

s.listen(5)

while True:
        c,addr = s.accept() #Establish a connection with the client
        print("Got connection from", addr)

        c.send(b"Thank you for connecting!")
        
        c.close()