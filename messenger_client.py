
#### message struct: @name message


import socket
import time


s = socket.socket()
print("established socket")



s.connect(("192.168.178.31", 697))







print(s.recv(1024).decode() + "\n")
    
    





class message_input:
    def __init__(self, content, user):
        self.content = content
        self.addresse = 0
        self.user = user
        if "@" in self.content:
            self.at = self.content.find("@")
            self.space = self.content.find(" ",self.at)
            self.addresse = self.content[self.at+1: self.space]
            self.message = self.content[self.space+1:len(self.content)]
        else:
            self.message = self.content



class message_received:
    def __init__(self, addresse, message, user):
        self.addresse = addresse
        self.message  = message
        self.user = user
        if not self.addresse == 0:
            self.content ="<" + self.user + "> @" + self.addresse + " " + self.message

        else: 
            self.content = "<" + self.user + "> " + self.message

class send_message:
    def __init__(self, addresse, message, user):
        self.addresse = addresse
        self.message = message
        self.user = user

        if not len(str(address)) + len(message) + len(user) > 1024:
            self.content = "║"+ self.addresse + "" + "║" + self.user + "║" + self.message

            self.content = self.content.encode() 
        else:
            self.content = b"0"
            print("could not send: too long")


class rec_message:
    def __init__(self, content):
        self.content = content.decode()

        self.content_parts = self.content.split("║")
        self.addresse = self.content_parts[0]
        self.user = self.content_parts[1]
        self.message = self.content_parts[2]
        if self.addresse == "0":
            self.addresse = 0







