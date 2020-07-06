import socket
import threading
import time



def Debug_Thread(connection):
        connection.send(b"Debug_Thread")
        content = b""

        while not content == b"end":

                content = connection.recv(1024)
                if not content == b"":
                        print(content)

        print("ended connection")

        time.sleep(1)
        connection.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket object

host = socket.gethostbyname("192.168.172.31")

port = 697

s.bind(("192.168.178.31",port))

s.listen(5)
connections = []
threads = []

while True:
        c,addr = s.accept() #Establish a connection with the client
        connections.append(c)
        print("Got connection from", addr)

        threads.append(threading.Thread(target = Debug_Thread, args = (connections[-1],)))
        threads[-1].start()
        
        