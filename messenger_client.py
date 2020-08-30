
#### message struct: @name message


import socket
import time
import threading
import sys
import pyDHE
import hashlib
import base64
import cryptography.fernet as fernet


class encryption:
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



class rec_message:
    def __init__(self, content, encryption):
        self.content = content.decode()
        self.encryption = encryption

        self.content_parts = self.content.split("║")
        print(self.content_parts)
        self.addresse = self.content_parts[1]
        self.user = self.content_parts[2]
        self.message = self.encryption.decrypt(self.content_parts[3].encode()).decode()
        


def printing(socket, encryption):

    printable = " "
    while not printable == "":
        p = rec_message(socket.recv(1024), encryption)
        printable = "<" +p.user+ "> @" +p.addresse + " " + p.message
        print(printable)


def debug_handshake(username, socket):
    bob = pyDHE.new()
    value = bob.negotiate(socket)
    e = encryption(value)
    socket.send(("Username:"+username).encode())
    response = socket.recv(1024).decode()
    if response.split(":")[0] == "0":
        debug_handshake(username, socket)
    else:
        return e
        



username = input("Username?\n")

s = socket.socket()
print("established socket")


s.connect(("localhost", 697))
encryption = debug_handshake(username, s)



print(s.recv(1024).decode() + "\n")
printing_thread = threading.Thread(target = printing, args = (s,encryption, ))
printing_thread.start()





class message_received:
    def __init__(self, addresse, message, user):
        self.addresse = addresse
        self.message  = message
        self.user = user
        if not self.addresse == 0:
            self.content ="<" + self.user + "> @" + self.addresse + " " + self.message

        else: 
            self.content = "<" + self.user + "> " + self.message

class send_thread:
    def __init__(self, user, socket, encryption):
        self.user = user
        self.socket = socket
        self.encryption = encryption
    
    def send_message(self, content):
        self.content = content
        self.addresse = "0"
        
        if "@" in self.content:
            self.at = self.content.find("@")
            self.space = self.content.find(" ",self.at)
            self.addresse = self.content[self.at+1: self.space]
            self.message = self.content[self.space+1:len(self.content)]
        else:
            self.message = self.content

        self.message = self.encryption.encrypt(self.message.encode())


        if not len(str(self.addresse)) + len(self.message.decode()) + len(self.user) > 1024:
            self.content = "║"+ self.addresse + "" + "║" + self.user + "║" + self.message.decode()

            self.content = self.content.encode() 
        else:
            self.content = b"0"
            print("could not send: too long")

        self.socket.send(self.content)







#content = ""
#while content != "end":
#    content = input()
#    s.send(content.encode())
sender = send_thread(username, s, encryption)
while True:
    message = input()
    
    sender.send_message(message)
    
