import socket
import threading
import time
import queue



def Debug_Thread(connection, address, mainqueue, subqueue):
        connection.send(b"Debug_Thread")
        content = b""

        while not content == b"end":

                content = connection.recv(1024)
                if not content == b"":
                        
                        printable = "<" + str(address[1]) + "> : " + content.decode()
                        print(printable)
                        mainqueue.put(printable)

                

                print(subqueue.qsize())
                time.sleep(0.07)
                if not subqueue.qsize == 0:
                        sendable_data = subqueue.get().encode()
                        connection.send(sendable_data)
                
                

        print("ended connection")

        time.sleep(1)
        connection.close()



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
        

        threads.append(threading.Thread(target = Debug_Thread, args = (connections[-1],addr,main_queue,subqueues[-1],)))
        threads[-1].start()
        
        