
#### message struct: @name message


import socket
import time
import threading
import sys

def printing(socket):
    printable = " "
    while not printable == "":
        printable = socket.recv(1024).decode()
        print(printable)



username = input("Username?\n")

s = socket.socket()
print("established socket")


s.connect(("localhost", 697))
s.send(b"Debug_Client")



print(s.recv(1024).decode() + "\n")
printing_thread = threading.Thread(target = printing, args = (s,))
printing_thread.start()



    




class message_input:
    def __init__(self, content):
        self.content = content
        self.addresse = "0"
        
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

class send_thread:
    def __init__(self, user, socket):
        self.user = user
        self.socket = socket
    
    def send_message(self, addresse, message):
        self.addresse = addresse
        self.message = message


        if not len(str(self.addresse)) + len(self.message) + len(self.user) > 1024:
            self.content = "║"+ self.addresse + "" + "║" + self.user + "║" + self.message

            self.content = self.content.encode() 
        else:
            self.content = b"0"
            print("could not send: too long")

        self.socket.send(self.content)


class rec_message:
    def __init__(self, content):
        self.content = content.decode()

        self.content_parts = self.content.split("║")
        self.addresse = self.content_parts[0]
        self.user = self.content_parts[1]
        self.message = self.content_parts[2]
        if self.addresse == "0":
            self.addresse = 0






#content = ""
#while content != "end":
#    content = input()
#    s.send(content.encode())
sender = send_thread(username, s)
while True:
    message = input()
    message = message_input(message)
    sender.send_message(message.addresse, message.content)
    
