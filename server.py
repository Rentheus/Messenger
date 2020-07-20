import socket
import threading
import time
import queue



class decoded_message:
    def __init__(self, content):
        self.content = content

        self.content_parts = self.content.split("║")
        self.addresse = self.content_parts[1]
        self.user = self.content_parts[2]
        self.message = self.content_parts[3]
        if self.addresse == "0":
            self.addresse = "0"

def debug_handshake(userlist, connection):
        username_recv = connection.recv(1024).decode()
        print(username_recv)
        username_parts = username_recv.split(":")
        if username_parts[0] == "Username":
                userlist.append(username_parts[1])
                connection.send("1:Username Accepted".encode())
        else:
                connection.send("0:Username requested".encode)
                debug_handshake(userlist, connection)

        


def Debug_Thread_listener(connection, address, mainqueue):
        connection.send(b"Debug_Thread")
        content = b""
        try:

                while not content == b"end":


                        content = connection.recv(1024)
                        if not content == b"":

                                printable = content.decode()
                                print(printable)
                                message_data = decoded_message(printable)
                                mainqueue.put(message_data)
        except WindowsError:
                #print("test")
                mainqueue.put("<" + str(address[1]) + "> has disconnected")

                

                
                
                
                
                

        print("ended connection")

        time.sleep(1)
        connection.close()

def Debug_thread(connection, subqueue):
        try:
                while True:
                        if not subqueue.qsize == 0:
                                        sendable_data = subqueue.get().encode()
                                        connection.send(sendable_data)
        except WindowsError:
                pass






def queue_handling(subqueues, mainqueue):
        while True:
                item = mainqueue.get()
                
                
                #msg = "<" +item.user+ "> @" +item.addresse + " " +  item.message
                if item.addresse == "0":
                        msg = "<" +item.user+ "> " +  item.message
                        for i in subqueues:
                                i.put(msg)
                                #print(subqueues[i])
                else:
                        msg = "<" +item.user+ "> @" +item.addresse + " " +  item.message
                        for i in range(len(userlist)):
                                if item.addresse == userlist[i]:
                                        subqueues[i].put(msg)
                        






s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket object
host = socket.gethostbyname("192.168.172.31")

port = 697

s.bind(("localhost",port))

s.listen(5)
connections = []
threads = []
listening_threads = []
main_queue = queue.Queue()
##main_queue_thread = threading.Thread(target = q)
subqueues = []
queue_thread = threading.Thread(target = queue_handling, args= (subqueues, main_queue,))
queue_thread.start()
userlist = []



while True:
        c,addr = s.accept() #Establish a connection with the client
        connections.append(c)
        print("Got connection from", addr)
        debug_handshake(userlist,c)
        print(1)

        subqueues.append(queue.Queue())
        

        listening_threads.append(threading.Thread(target = Debug_Thread_listener, args = (connections[-1], addr , main_queue,)))
        listening_threads[-1].start()
        threads.append(threading.Thread(target = Debug_thread, args = (connections[-1],subqueues[-1],)))
        threads[-1].start()



        
        