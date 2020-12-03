import socket
import queue
import cryptography.fernet as fernet
import base64
import json
import hashlib


ENCODING ='utf-8'

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

class file_to_send:
    def __init__(self, file, encryption):
        self.file = file
        self.encryption = encryption
        self.filedata = encryption.encrypt(open(file).read().encode(ENCODING))
        self.packet = {
                "filename" : self.file,
                "number" : "0000000", 
                "filedata" : ""
        }
        self.jmessage = json.dumps(self.packet)
        self.bmessage = self.jmessage.encode(ENCODING)
        self.p_len = len(self.bmessage)
        self.m_len = 1024-self.p_len

        self.message_packets = []
        
        
        for norway in range(int(len(self.filedata)/(self.m_len))+1):
                self.packet = self.packet = {
                "filename" : self.file,
                "number" : "0000000", 
                "filedata" : self.filedata[norway*self.m_len:(norway+1)*self.m_len].decode(ENCODING)
        }
                self.message_packets.append(json.dumps(self.packet).encode(ENCODING))

        
        for u in self.message_packets:
                print(u)
                print(len(u))





b = encr(b"setjfdjidsjhfiusdhnfuidshnfiuds")
a = file_to_send("server.py", b)