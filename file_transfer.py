import socket
import queue
import cryptography.fernet as fernet
import base64
import json
import hashlib


ENCODING ='utf-8'

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

class file_to_send:
        def __init__(self, file, encryption, addresse):
                self.file = file
                self.encryption = encryption
                self.filedata = self.encryption.encrypt(open(file).read().encode(ENCODING))
                self.addresse = addresse
                self.packet = {
                        'action': 'file',
                        'to': self.addresse,
                        "filename" : self.file, 
                        "filedata" : ""
                }
                self.jmessage = json.dumps(self.packet)
                self.bmessage = self.jmessage.encode(ENCODING)
                self.p_len = len(self.bmessage)
                self.m_len = 1024-self.p_len

                self.message_packets = []


                for norway in range(int(len(self.filedata)/(self.m_len))+1):
                        self.packet = self.packet = {
                        'action': 'file',
                        'to': self.addresse,
                        "filename" : self.file,
                        "filedata" : self.filedata[norway*self.m_len:(norway+1)*self.m_len].decode(ENCODING)
                }
                        self.message_packets.append(json.dumps(self.packet).encode(ENCODING))


                #for u in self.message_packets:
                #        print(u)
                #        print(len(u))
    

        def return_message_packets(self):
                return(self.message_packets)


class recv_file:
        def __init__(self,j_message_list, encryption):
                self.j_message_list = j_message_list
                self.encryption = encryption
                self.tmp = b""

                for i in j_message_list:
                        self.tmp = self.tmp + i["filedata"].encode(ENCODING)
                

                self.filedata = self.encryption.decrypt(self.tmp).decode(ENCODING)

        def print_file(self):
                print(self.tmp)
                print(self.filedata) 

        def save_file(self):
                with open("saved_" + self.j_message_list[0]["filename"], "wb") as self.file:
                        self.file.write(self.filedata.encode(ENCODING))             






b = encr(b"setjfdjidsjhfiusdhnfuidshnfiuds")
a = file_to_send("server.py", b, "user")
tmp = a.return_message_packets()
#print(tmp)
t = []
for i in tmp:
        t.append(json.loads(i.decode(ENCODING)))

c = recv_file(t, b)
c.save_file()