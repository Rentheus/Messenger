
#### message struct: @name message


import socket
import time
import threading
import sys
import pyDHE
import hashlib
import base64
import cryptography.fernet as fernet
import json
import time
#first install pycryptodome then cryptography

ENCODING = 'utf-8'

def dict_to_bytes(message_dict):
    """
    Convert dict to bytes
    :param message_dict: dict
    :return: bytes
    """
    if not isinstance(message_dict, dict):
        raise TypeError

    jmessage = json.dumps(message_dict)

    bmessage = jmessage.encode(ENCODING)
    return bmessage

def byte_to_dict(message_byte):
    """
    Convert bytes to dict
    :param message_byte: bytes
    :return: dict
    """
    if not isinstance(message_byte, bytes):
        raise TypeError

    jmessage = message_byte.decode(ENCODING)

    message_dict = json.loads(jmessage)
    return message_dict

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



class rec_message:
    def __init__(self, content, encryption):
        self.content = byte_to_dict(content)
        self.encryption = encryption

        #self.content_parts = self.content.split("║")
        #print(self.content_parts)
        self.addresse = str(self.content['to'])
        self.user = self.content['from']
        self.message = self.encryption.decrypt(self.content['msg'].encode()).decode()
        


def printing(socket, encryption):

    printable = " "
    while not printable == "":
        p = rec_message(socket.recv(1024), encryption)
        printable = "<" +p.user+ "> @" +p.addresse + " " + p.message
        print(printable)


def debug_handshake(username, passw, socket):
    bob = pyDHE.new()
    value = bob.negotiate(socket)
    e = encr(value)
    
    
    socket.send(e.encrypt(("Username:"+username).encode()))
    time.sleep(0.12)
    socket.send(e.encrypt((passwd).encode()))
    passw = ""
    response = socket.recv(1024).decode()
    print("test")
    if response.split(":")[0] == "0":
        debug_handshake(username, passw, socket)
    else:
        return e
        



username = input("Username?\n")
passwd = input("Password?\n")

s = socket.socket()
print("established socket")


s.connect(("localhost", 3569))
encryption = debug_handshake(username, passwd, s)

passwd = ""

#print(s.recv(1024).decode() + "\n")
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
            self.packet = {
                'action': 'msg',
                'time': time.time(),
                'from': self.user,
                'to': self.addresse,
                'msg': self.message.decode()
                }
            self.socket.send(dict_to_bytes(self.packet))
        else:
            self.packet = b"0"
            print("could not send: too long")








#content = ""
#while content != "end":
#    content = input()
#    s.send(content.encode())
sender = send_thread(username, s, encryption)
while True:
    message = input()
    
    sender.send_message(message)
    
