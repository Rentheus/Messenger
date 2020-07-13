import socket
import threading
import time
import queue



class rec_message:
    def __init__(self, content):
        self.content = content.decode()

        self.content_parts = self.content.split("║")
        self.addresse = self.content_parts[0]
        self.user = self.content_parts[1]
        self.message = self.content_parts[2]
        if self.addresse == "0":
            self.addresse = 0









def Debug_Thread(connection, address, mainqueue):
        connection.send(b"Debug_Thread")
        content = b""
        try:

                while not content == b"end":


                        content = connection.recv(1024)
                        if not content == b"":

                                printable = "<" + str(address[1]) + "> : " + content.decode()
                                print(printable)
                                mainqueue.put(printable)
        except WindowsError:
                #print("test")
                mainqueue.put("<" + str(address[1]) + "> has disconnected")

                

                
                
                
                
                

        print("ended connection")

        time.sleep(1)
        connection.close()

def Debug_thread_listener(connection, subqueue):
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
                for i in range(len(subqueues)):
                        subqueues[i].put(item)
                        print(subqueues[i])



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket object
host = socket.gethostbyname("192.168.172.31")

port = 697

s.bind(("192.168.178.31",port))

s.listen(5)
connections = []
threads = []
listening_threads = []
main_queue = queue.Queue()
##main_queue_thread = threading.Thread(target = q)
subqueues = []
queue_thread = threading.Thread(target = queue_handling, args= (subqueues, main_queue,))
queue_thread.start()



while True:
        c,addr = s.accept() #Establish a connection with the client
        connections.append(c)
        print("Got connection from", addr)
        subqueues.append(queue.Queue())
        

        threads.append(threading.Thread(target = Debug_Thread, args = (connections[-1], addr , main_queue,)))
        threads[-1].start()
        listening_threads.append(threading.Thread(target = Debug_thread_listener, args = (connections[-1],subqueues[-1],)))
        listening_threads[-1].start()



        
        