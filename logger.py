import datetime
import time
import random

class logfile:
    def __init__(self):
        self.logname = "log"
        

        self.f = open(self.datetime_filesafe() + "_LOG.log", "w+")
        

        self.f.write("Logfile\n")

        
        self.f.write(datetime.datetime.today().isoformat() + "\n \n \n \n")
#

    def datetime_filesafe(self):
        'returns a datetime suitable for filenames'
        self.d = datetime.datetime.today().isoformat()
        self.d_list = self.d.split(":")
        self.d = "-".join(self.d_list)
        self.d_list = self.d.split(".")
        self.d = "-".join(self.d_list)
        return self.d

    def log(self, log_message):
        self.log_message = log_message

        self.f.write(datetime.datetime.today().isoformat() + ":  " + self.log_message+"\n")
        

#a = logfile()
#a.log("test")
#
#for i in range(10):
#    b = random.randint(0, 1)
#    time.sleep(b)
#    a.log("Time elapsed: " + str(b))