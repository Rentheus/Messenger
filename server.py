import socket
import threading
import time
import queue
import pyDHE
import cryptography.fernet as fernet
import hashlib
import base64
import password_db
import Crypto
import json

ENCODING = 'utf-8'

class encr:
        def __init__(self, key):
                
                self.key = key
                self.m = hashlib.sha256()
                self.m.update(str(key).encode())
                
                self.fernet = fernet.Fernet(base64.urlsafe_b64encode(self.m.digest()))

        def encrypt(self, message):
                self.message = message
                
                self.message = self.fernet.encrypt(message)
                return self.message

        def decrypt(self, message):
                self.message = message

                return self.fernet.decrypt(self.message)



class decoded_message:
    def __init__(self, content, encryption):
        self.content = content

        self.content_parts = self.content.split("║")
        self.addresse = self.content_parts[1]
        self.user = self.content_parts[2]
        self.message = self.content_parts[3]
        self.encryption = encryption
        self.message = self.encryption.decrypt(self.message.encode()).decode()
        if self.addresse == "0":
            self.addresse = "0"



def debug_handshake(userlist, connection, passwd_db):
        truth_value = False
        alice = pyDHE.new()
        value = alice.negotiate(connection)
        e = encr(value)
        print(1)

        

        username_recv = e.decrypt(connection.recv(1024))
        time.sleep(0.13)
        print(2)
        passwd_recv = e.decrypt(connection.recv(1024))
        print(3)
        #print(username_recv)
        username_parts = username_recv.decode().split(":")
        passwd_parts = passwd_recv.decode()
        print(passwd_parts)

        if passwd_db.add_user(username_parts[1],passwd_parts) == True:
                truth_value = True
                print(1)
        elif passwd_db.check_password(username_parts[1],passwd_parts) == True:
                truth_value = True
                print(2)

        if username_parts[0] == "Username"  and truth_value == True:
                userlist.append(username_parts[1])
                connection.send("1:Username Accepted".encode())
                passwd_parts = []
                return e
        else:
                connection.send("0:Authentification failed".encode())
                debug_handshake(userlist, connection)

        


def Debug_Thread_listener(connection, address, mainqueue, encryption ):
        #connection.send(b"Debug_Thread")
        content = b""
        try:

                while not content == b"end":


                        content = connection.recv(1024)
                        if not content == b"":

                                printable = content.decode()
                                print(printable)
                                message_data = decoded_message(printable, encryption)
                                print(message_data.user +": " + message_data.message)
                                mainqueue.put(message_data)
        except WindowsError:
                pass
                #print("test")
                #mainqueue.put("<" + str(address[1]) + "> has disconnected")

                

                
                
                
                
                

        print("ended connection")

        time.sleep(1)
        connection.close()

def Debug_thread(connection, subqueue, encryption):
        try:
                while True:
                        if not subqueue.qsize == 0:
                                        
                                        msg, message = subqueue.get()
                                        message = encryption.encrypt(message.encode())
                                        sendable_data = msg.encode() +"║".encode()+ message
                                        connection.send(sendable_data)
        except WindowsError:
                pass






def queue_handling(subqueues, mainqueue):
        while True:
                item = mainqueue.get()
                
                
                #msg = "<" +item.user+ "> @" +item.addresse + " " +  item.message
                try:
                        if item.addresse == "0":
                                msg = ("║0║"+item.user  ,  item.message)
                                for i in subqueues:
                                        i.put(msg)
                                        #print(subqueues[i])
                        else:
                                msg = ("║" +item.addresse+ "║" +item.user, item.message)
                                for i in range(len(userlist)):
                                        if item.addresse == userlist[i]:
                                                subqueues[i].put(msg)
                except AttributeError:
                        pass
                        






pdb = password_db.PwDatabase()
pdb.open_db("pwdb.db")

print(0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create a socket object
host = socket.gethostbyname("192.168.172.31")

port = 3569

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
encryptionlist = []



while True:
        c,addr = s.accept() #Establish a connection with the client
        connections.append(c)
        print("Got connection from", addr)
        print(9)
        encryption = debug_handshake(userlist,c,pdb)
        print(2)
        encryptionlist.append(encryption)
        print(1)

        subqueues.append(queue.Queue())
        

        listening_threads.append(threading.Thread(target = Debug_Thread_listener, args = (connections[-1], addr , main_queue, encryptionlist[-1], )))
        listening_threads[-1].start()
        threads.append(threading.Thread(target = Debug_thread, args = (connections[-1],subqueues[-1],encryptionlist[-1],)))
        threads[-1].start()



        
        
