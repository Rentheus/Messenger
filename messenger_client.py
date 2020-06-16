
#### message struct: @name message



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





a = message_input("@d hello world", "user")
b = message_received(a.addresse, a.message, a.user)


print(a.content)
print(b.content)