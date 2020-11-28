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
        self.filedata = encryption.encrypt(open(file).read())
        self.filepacket = {
            "file" : self.file,
            
            
        }

