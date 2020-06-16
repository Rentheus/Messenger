
#### message struct: @name message



class message_input:
    def __init__(self, content):
        self.content = content
        self.addresse = 0
        if "@" in self.content:
            self.at = self.content.find("@")
            self.space = self.content.find(" ",self.at)
            self.addresse = self.content[self.at+1: self.space]
            self.message = self.content[self.space+1:len(self.content)]
        else:
            self.message = self.content




