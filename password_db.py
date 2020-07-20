import sqlite3
import hashlib, os


def new_password_hash(password, user):
    password = password.encode("utf-8")
    salt = os.urandom(64)
    password_hash = hashlib.pbkdf2_hmac("sha512", password, salt, 200298)
    password = b""

    return user, password_hash, salt

class PwDatabase:
    def __init__(self):
        pass

    def open_db(self, name):
        self.name = name
        self.pdb = sqlite3.connect(name)
        self.c = self.pdb.cursor()
        try:
            self.c.execute("CREATE TABLE passwords (user text, hash bytes, salt bytes)")
        except:
            pass

    def add_user(self, username, password):
        self.username = username
        if self.check_user_duplicate(self.username):
            self.password = password
            self.userdata = new_password_hash(self.password, self.username)
            self.password = ""
            self.username = ""
            self.c.execute("INSERT INTO passwords VALUES(?,?,?)", self.userdata)
            self.pdb.commit()
            return True
        else:
            return False

    def check_user_duplicate(self, username):
        
        self.c.execute('SELECT * FROM passwords WHERE user=?', (username,))
        if self.c.fetchall() == []:
            return True
        else:
            return False
    
    def check_password(self, username, password):
        self.username = username
        self.password = password
        self.c.execute('SELECT * FROM passwords WHERE user=?', (username,))
        self.userdata = self.c.fetchone()
        self.password = self.password.encode("utf-8")
        self.salt = self.userdata[2]
        self.password_hash = hashlib.pbkdf2_hmac("sha512", self.password, self.salt, 200298)
        self.password = b""
        
        
        if self.password_hash == self.userdata[1]:
            return True
        else:
            return False
        








#pdb = PwDatabase()
#pdb.open_db("pwdb.db")
#print(pdb.add_user("user3", "HNJUIHSUIH239843297597jijj(/676%&!&5"))
#print(pdb.check_password("user", "password"))
#print(pdb.check_password("user2", "HNJUIHSUIH239843297597jijj(/676%&!&5"))

