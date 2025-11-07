import socket       #Socket for Server and client communication 
import os           #for terminal commands 
import time         #For controlling sleep and server functions 
from threading import Thread    #thread for multiple client connections 
import ssl          #ssl/tls connection for secure communication
import re           #checking fort special characters 
import bcrypt       #Encryption for password 

class Server: 
    #creates the server
    #accepts the client at the insecure state of the client and makes it secure 
    threadClient = {}
    countThread = 0
    dirCa = os.getcwd()
    def __init__(self, server, insecure, client, address, db, thread, authBit, authUser):
        self.server = server
        self.insecure = insecure
        self.client = client
        self.address = address 
        self.db = db
        self.thread = thread
        self.authBit = 0
        self.authUser = 0
    #connects to sql cursor         
    def sqlDatabase(self):
        dir = os.getcwd()
        saltPass = bcrypt.gensalt()
        passwd = "admin$et561"
        passwd = bcrypt.hashpw(passwd.encode(), saltPass)
        secureQ = "2000" + "Coffee" + "BMW2015"
        saltQ = bcrypt.gensalt()
        hSecure = bcrypt.hashpw(secureQ.encode(), saltQ)
        dir = os.getcwd()
        dir += "/Katherine(Server)/admin"
        self.db = {'admin':{'username': 'admin', 'passwd': passwd, 'SaltPass': saltPass, 'secureQ': hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dir}}
        dir = os.getcwd()
        saltPass = bcrypt.gensalt()
        passwd = "Fish$!NThe3"
        passwd = bcrypt.hashpw(passwd.encode(), saltPass)
        secureQ = "2019" + "Hager" + "HONDA2012"
        saltQ = bcrypt.gensalt()
        hSecure = bcrypt.hashpw(secureQ.encode(), saltQ)
        dir = os.getcwd()
        dir += "/Katherine(Server)/Katherine"
        self.db['Katherine'] = {'username': 'Katherine', 'passwd': passwd, 'SaltPass': saltPass, 'secureQ': hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dir}
        # self.db = sqlite3.connect('KatherineSrver.db', autocommit=True)
        
        # self.db.execute("""CREATE TABLE IF NOT EXISTS USER (username TEXT PRIMARY KEY NOT NULL, passwd TEXT NOT NULL, SaltPasswd TEXT NOT NULL, secureQ TEXT NOT NULL, SaltSecure TEXT NOT NULL, lockedBit INTEGER NOT NULL, FOREIGN KEY (username) REFERENCES directory(username))""")
        #self.db.execute(''' 
                #CREATE TABLE IF NOT EXISTS directory(
                    #username TEXT NOT NULL,
                    #FILE TEXT 
                #)
            #''')
        self.createServer()
        
    #Creates socket server
    #Binds it to ip address =  0.0.0.0 and port = 5001
    #Listens for clients    
    def createServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket was created")
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', 5001))
        self.server.listen()
        while (True):
            try:
                self.insecure, self.address = self.server.accept()
                Server.countThread += 1
                try:
                    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                    context.verify_mode = ssl.CERT_REQUIRED 
                    ca = Server.dirCa + "/ca.crt"
                    pem = Server.dirCa + "/server.pem"
                    key = Server.dirCa + "/server.key"
                    context.load_verify_locations(ca)

                    context.load_cert_chain(pem, keyfile=key ,password="cookie")
                    context.verify_flags = context.verify_flags & ~ssl.VERIFY_X509_STRICT
                    Server.threadClient[Server.countThread] = {'client': self.insecure, 'username': None, 'loggedIn': 0, 'thread': self.thread, 'dir': Server.dirCa}
                    self.thread = Thread(target=self.serverAuth, args=(context, )).start()
                    #while (True):  
                except FileNotFoundError as e:
                    print(e)
                    print(os.getcwd())
                    self.insecure.close()
                    time.sleep(3)
            except IOError: 
                print("connection error")
                print("Client '%s' disconnected." % self.insecure)
                #Out of Server directory
                #close thread and secure client connect
                #calls on server to close the insecure connection 
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        server = Server.threadClient.pop(i)
                        print(server)
                self.insecure.close()
                time.sleep (3)
            except ConnectionRefusedError: 
                print("Waiting for connection.....")
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        server = Server.threadClient.pop(i)
                        print(server)
                self.insecure.close()
                time.sleep(3)
            except ConnectionResetError:
                print("Server lost a client waiting for new connection")
                #close thread and secure client connect
                #calls on server to close the insecure connection 
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        server = Server.threadClient.pop(i)
                        print(server)
                self.insecure.close()
                time.sleep(3)
            except KeyboardInterrupt:
                print("Server closed")
                self.authBit = 0 
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        server = Server.threadClient.pop(i)
                        print(server)
                        self.insecure.close()
                        break
                    elif (Server.threadClient[i]['client'] == self.client):
                        server = Server.threadClient.pop(i)
                        print(server)
                        self.client.close()
                        break
                break
    
    def serverAuth(self, context):
        #insecure client is not secured client. 
                
        try:
            self.client = context.wrap_socket(self.insecure, server_side=True)
            cert = self.client.getpeercert()
            
            if (cert == None):
                print("Connection Failed. No Cert")
                self.client.close()
                time.sleep(3)
            elif(cert != None):
                print("Certificate Verified!")
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        Server.threadClient[i]['client'] = self.client
                try:
                    os.chdir("Katherine(Server)")
                    print("Inside Katherine(Server) directory!")
                    try: 
                        os.mkdir("admin")
                        os.mkdir("Katherine")
                        print("Admin user has be created!")
                        print("Katherine user has be created!")
                    except FileExistsError:
                        print("Admin user has already been created!")
                        print("Katherine user has already been created!")
                    self.logIn()
                except FileExistsError:
                    print("User has already visited!")
                    os.chdir("Katherine(Server)")
                    try: 
                        os.mkdir("admin")
                        print("Admin user has be created!")
                    except FileExistsError:
                        print("Admin user has already be created!")
                    self.logIn()
        except ConnectionError as e:
            print(e)
            print("server is not secure")
            print("connection error")
            #Out of Server directory
            print("Client '%s' disconnected." % self.client)
            #close thread and secure client connect
            #calls on server to close the insecure connection 
            self.authBit = 0
            self.authUser = 0
            for i in Server.threadClient:
                if (Server.threadClient[i]['client'] == self.client):
                    server = Server.threadClient.pop(i)
                    print(server)
            self.client.close()
            time.sleep(3)
        except ssl.SSLEOFError:
            print("Client disconnected. No Cert")
            self.authBit = 0
            self.authUser = 0
            for i in Server.threadClient:
                if (Server.threadClient[i]['client'] == self.client):
                    server = Server.threadClient.pop(i)
                    print(server)
            self.client.close()
            time.sleep(3)

    #Asks user where to create an account or Login
    def logIn(self):
        login = "  _          _          _          _          _\n>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,\n  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'\n  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs\n\n************ WELCOME TO KATHERINE'S SERVER ************\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        self.client.sendall(login.encode())
        self.clientResponse()
        
    #Check for username; 3 tries 
    #Check Password; 3 tries 
    def clientAuth(self):
        tries = 3
        self.client.sendall(b"account")
        self.client.sendall(b"~~~~~~~~~~~~ LOGIN ON KATHERINE'S SERVER ~~~~~~~~~~~~ ")
        while tries != 0:
            self.client.sendall(b"Enter Username: ")
            self.username = self.client.recv(1024).decode()
            if (len(self.db) == 0):
                find = None
            elif(self.username in self.db):
                find = self.db[self.username]
            else:
                find = None
            if (find == None and tries == 1):
                print("Authentication error! No such user exists")
                self.client.sendall(b"stop")
                self.username = "Guest User" 
                message = "========== USER NOT FOUND ==========\n--------- NO ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
            elif(find == None): 
                if (tries == 3):
                    message = "========== USERNAME DOES NOT EXIST ==========\n--------- 2 ATTEMPTS LEFT ---------\n"
                else:
                    
                    message = "========== USERNAME DOES NOT EXIST ==========\n--------- 1 ATTEMPT LEFT ---------\n"
                tries -= 1
                self.client.sendall(message.encode())
            elif(find != None):
                lockedBit = find['lockedBit']
                if (lockedBit == 1):
                    print("Account Locked!")
                    if (tries == 3):
                        message = "========== USERNAME PERMISSION DENIED ==========\n--------- 2 ATTEMPTS LEFT ---------\n"
                    else:
                        message = "========== USERNAME PERMISSION DENIED ==========\n--------- 1 ATTEMPT LEFT ---------\n"
                    tries -= 1
                    self.client.sendall(message.encode())
                else:
                    tries = 3
                    print("Username found!!")
                    self.authUser = 1
                    self.authBit = 0
                    pssWd = self.db[self.username]['passwd']
                    salt = self.db[self.username]['SaltPass']
                    #self.db.close()
                    self.client.sendall(b"secure")
                    while tries != 0:
                        self.client.sendall(b"Enter Password: ")
                        #must encrypt password to get answer
                        passwd = self.client.recv(1024)
                        passwd = bcrypt.hashpw(passwd, salt)
                        if ((pssWd != passwd) and (tries == 1)):
                            print("Authentication error! No such user exists")
                            self.client.sendall(b"stop")
                            self.client.sendall(b"stop")
                            self.client.sendall(b"!!!PASSWORD INCORRECT!!!\n--------- 0 ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (F)Forgot Password\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                            self.clientResponse()
                        elif(pssWd != passwd):
                            print("Password incorrect!")
                            if (tries == 3):
                                message = ("!!!PASSWORD INCORRECT!!!\n--------- 2 ATTEMPTS LEFT ---------\n")
                            else:
                                message = ("!!!PASSWORD INCORRECT!!!\n--------- 1 ATTEMPTS LEFT ---------\n")
                            tries -= 1
                            self.client.sendall(message.encode())
                        else: 
                            self.client.sendall(b"stop")
                            print("User is authenticated!!")
                            self.client.sendall(b"authenticated")
                            os.chdir(self.username)
                            print(os.getcwd())
                            self.authBit = 1
                            for i in Server.threadClient:
                                if (Server.threadClient[i]['client'] == self.client):
                                    Server.threadClient[i]['username'] = self.username
                                    Server.threadClient[i]['loggedIn'] = self.authBit
                                    Server.threadClient[i]['dir'] = os.getcwd()
                            message = self.username + ": "
                            self.client.sendall(message.encode())
                            self.welcomeMessage()

                        
    #resets user password then asks them to login again or they can exit.
    def forgotPassword(self):
        #check that the user is 
        #connect = sqlite3.connect('KatherineSrver.db')
        #self.db = connect.cursor()
        #self.db.execute("BEGIN")
        self.client.sendall(b"account")
        self.client.sendall(b"secure")
        tries = 3
        if (len(self.db) == 0):
            find = None
        elif(self.username in self.db):
                find = self.db[self.username]
        else:
            find = None
        saltQ = find['SaltSecure']
        secureQ = find['secureQ']
        self.client.sendall(b"~~~~~~~~~~~~ RESET PASSWORD ~~~~~~~~~~~~\n======= Security Questions =======\n--------- Case Sensitive ---------\n")
        while tries != 0:
            self.client.sendall(b"What year did you graduate from High School: ")
            message = self.client.recv(1024)
            self.client.sendall(b"What was your mothers maiden name: ")
            message += self.client.recv(1024)
            self.client.sendall(b"What was your first cars' make and year (Example:HONDA2012): ")
            message += self.client.recv(1024)  
            #encyprt message 
            message = bcrypt.hashpw(message, saltQ)
            if (message != secureQ and tries == 1):
                self.username = "Guest User"
                print("Authentication error! No such account exists")
                self.client.sendall(b"stop")
                self.client.sendall(b"stop")
                message = "--------- SECURITY QUESTIONS INVALID ---------\n======= ACCOUNT "+ self.username +" LOCKED ======= \n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n Guest User: "
                self.client.sendall(message.encode())
                    
                find['lockBit'] = 1
                #self.db.close()
                self.username = "Guest User"
                self.clientResponse(self)
            elif(message != secureQ): 
                print("Authentication error! No such account exists")
                if (tries == 3):
                    message = ("--------- SECURITY QUESTIONS INVALID ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                else:
                    message = ("--------- SECURITY QUESTIONS INVALID ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                tries -= 1
                self.client.sendall(message.encode())
            else:
                self.client.sendall(b"stop")
                print("Security questions passed!!")
                passwd, salt = self.checkPasswd()
                    
                find[self.username]['passwd'] = passwd
                find[self.username]['SaltPass'] = salt
                    
                    #self.db.close()
                
                #if (self.authBit == 1 and self.authUser == 1):
                    
                    #message = "======= PASSWORD UPDATED =======\nn~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" + self.username + ": "
 
                    #self.client.sendall(message.encode())
                    #self.clientResponse()
                #else:
                self.username = "Guest User"
                self.client.sendall(b"======= PASSWORD UPDATED =======\n")
                self.client.sendall(b"stop")
                self.client.sendall(b"~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                self.clientResponse()
                break
    # checks if password has all critria
    # One lowercase
    # One Uppercase
    # One special Character
    # One number 
    # 8 characters long
    def checkPasswd(self):
        tries = 3
        self.client.sendall(b"secure")
        while tries != 0: 
            self.client.sendall(b"~~~~~~~~~~~~~~~~ PASSWORD MUST CONTAIN ~~~~~~~~~~~~~~~~\nONE lowercase letter\nONE uppercase letter\nONE number (0123456789)\nONE special character(~!@#$%^&*()_-+=><[{]}|/?)\n\nEnter Password: ")
            passwd = self.client.recv(1024).decode()
            digit = any(char.isdigit() for char in passwd)
            upper = any(char.isupper() for char in passwd)
            lower = any(char.islower() for char in passwd)
            special = "~!@#$%^&*()_-+=><[{]}|/?"
            spec = False
            for c in passwd:
                for s in special:
                    if (c == s):
                        spec = True
                        
            if(len(passwd) >= 8 and digit and lower and upper and spec):
            
                print("Password accepted!")
                passwd = passwd.encode()
                salt = bcrypt.gensalt()
                passwd = bcrypt.hashpw(passwd, salt)
                tries = 3
                while tries != 0:
                    self.client.sendall(b"Verify Password: ")
                    verPass = self.client.recv(1024).decode()
                    verPass = verPass.encode()
                    verPass = bcrypt.hashpw(verPass, salt)
                    if (verPass != passwd and tries == 1):
                        self.client.sendall(b"stop")
                        
                        self.username = "Guest User"
                        self.client.sendall(b"stop")
                        self.client.sendall(b"--------- PASSWORDS DO NOT MATCH ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n Guest User: ")
                        self.clientResponse()
                    elif(verPass != passwd):
                        print("Password DO NOT match!")
                        if (tries == 3):
                            message = ("--------- PASSWORDS DO NOT MATCH ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                        else:
                            message = ("--------- PASSWORD DO NOT MATCH ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                        tries -= 1
                        self.client.sendall(message.encode()) 
                    elif(verPass == passwd):
                        print("Password is verified.")
                        if (self.authBit == 1 and self.authUser == 1 ):
        
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ PASSWORD ACCEPTED ~~~~~~~~~~~~~~~~\n")
                            return passwd, salt
                        else:
                            self.client.sendall(b"stop")
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ PASSWORD ACCEPTED ~~~~~~~~~~~~~~~~\n")
                            return passwd, salt
            elif( tries == 1):
                self.client.sendall(b"stop")
                
            
                self.username = "Guest User"
                self.client.sendall(b"--------- PASSWORD IS NOT ADEQUATE ---------\n--------- NO ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n          (C)Create Account\n          (F)Forgot Password\n        (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n Guest User: ")
            
                self.clientResponse()
            else:
                if (tries == 3):
                    message = ("--------- PASSWORD IS NOT ADEQUATE ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                else:
                    message = ("--------- PASSWORD IS NOT ADEQUATE ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                tries -= 1
                self.client.sendall(message.encode())      
                
    #create a client account
    def clientCreate(self):
        self.client.sendall(b"account")
        self.client.sendall(b"~~~~~~~~~~~~ CREATE ACCOUNT TO KATHERINE'S SERVER ~~~~~~~~~~~~")
        tries = 3
        find = 0
        while (tries > 0):
            
            self.client.sendall(b"Enter username: ")
            self.username = self.client.recv(1024).decode()
            if (len(self.db) == 0 ):
                find = 0
            elif(self.username in self.db):
                find = 1
            if (find != 0 and tries == 1):
                self.client.sendall(b"stop")
                message = "--------- USER NAME MUST BE UNIQUE ---------\n--------- NO ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
            elif (find != 0):
                if (tries == 3):
                    message = ("--------- USER NAME MUST BE UNIQUE ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                else:
                    message = ("--------- USER NAME MUST BE UNIQUE ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                self.client.sendall(message.encode())
                tries -= 1
            else: 
                print("Username is unique and accepted!")
                break
        #self.client.sendall(b"stop")
        passwd, salt = self.checkPasswd() 
        if (len(passwd) > 0):  

            self.client.sendall(b"======= Security Questions =======\n")
            self.client.sendall(b"--------- Case Sensitive ---------")
            self.client.sendall(b"secure")
            self.client.sendall(b"What year did you graduate from High School: ")
            message = self.client.recv(1024)
            self.client.sendall(b"What was your mothers maiden name: ")
            message += self.client.recv(1024)
            self.client.sendall(b"What was your first cars make and year (Example:HONDA2012): ")
            message += self.client.recv(1024)
            self.client.sendall(b"stop")
            self.client.sendall(b"~~~~~~~~~~~~~~~~~ SECURITY ANSWERS ACCEPTED ~~~~~~~~~~~~~~~~\n")
            secureQ = message
            saltQ = bcrypt.gensalt()
            hSecure = bcrypt.hashpw(secureQ, saltQ)
            try:
                thisDir = os.getcwd()
                os.mkdir(self.username)
                print("Directory create " + self.username)
                print("New user directory made!")
                os.chdir(self.username)
                dirClient = os.getcwd()
                self.db[self.username] = {'passwd': passwd, 'SaltPass':salt, 'secureQ':hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dirClient}
                os.chdir("..")
                if(thisDir == os.getcwd()):
                    self.client.sendall(b"stop")
                    message = "~~~~~~~~~~~~ " + self.username +" USER CREATED ON SERVER ~~~~~~~~~~~~\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    self.client.sendall(message.encode())
                    self.username = "Guest User"
                    self.clientResponse()
            except FileExistsError:
                thisDir = os.getcwd()
                os.chdir(self.username)
                dirClient = os.getcwd()
                self.db[self.username] = {'username': self.username, 'passwd': passwd, 'SaltPass':salt, 'secureQ':hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dirClient}
                os.chdir("..")
                print(thisDir)
                print(os.getcwd())
                print("Server has this user saved")
                if(thisDir == os.getcwd()):
                    self.client.sendall(b"stop")
                    message = "~~~~~~~~~~~~ " + self.username +" USER CREATED ON SERVER ~~~~~~~~~~~~\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    self.client.sendall(message.encode())
                    self.username = "Guest User"
                    self.clientResponse()
                    

                
            
    #Reset security questions  
    #Verify Password and then this can happen.          
    def resetSecureQ(self):
            tries = 3
            pssWd = self.db[self.username]['passwd']
            salt = self.db[self.username]['SaltPass']
            #self.db.close()
            self.client.sendall(b"account")
            self.client.sendall(b"secure")
            while tries != 0:
                self.client.sendall(b"Enter Password: ")
                        #must encrypt password to get answer
                passwd = self.client.recv(1024)
                passwd = bcrypt.hashpw(passwd, salt)
                if ((pssWd != passwd) and (tries == 1)):
                    print("Authentication error! No such user exists")
                    self.username = "Guest User"
                    self.client.sendall(b"stop")
                    self.client.sendall(b"!!!PASSWORD INCORRECT!!!\n--------- 0 ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (F)Forgot Password\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    self.authUser = 0
                    self.clientResponse()
                elif(pssWd != passwd):
                    print("Password incorrect!")
                    if (tries == 3):
                        message = ("!!!PASSWORD INCORRECT!!!\n--------- 2 ATTEMPTS LEFT ---------\n")
                    else:
                        message = ("!!!PASSWORD INCORRECT!!!\n--------- 1 ATTEMPTS LEFT ---------\n")
                        tries -= 1
                    self.client.sendall(message.encode())
                else: 
                    tries = 3
                
                    while tries != 0:
                        self.client.sendall(b"Verify Password: ")
                        verPass = self.client.recv(1024).decode()
                        verPass = verPass.encode()
                        verPass = bcrypt.hashpw(verPass, salt)
                        if (verPass != passwd and tries == 1):
                            self.client.sendall(b"stop")
                            self.client.sendall(b"stop")
                            self.client.sendall(b"--------- PASSWORDS DO NOT MATCH ---------\n=========== PASSWORD NOT VERIFIED CANT CHANGE SECURITY QUESTIONS ===========\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                            self.clientResponse()
                        elif(verPass != passwd):
                            print("Password DO NOT match!")
                            if (tries == 3):
                                message = ("--------- PASSWORDS DO NOT MATCH ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                            else:
                                message = ("--------- PASSWORD DO NOT MATCH ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                            tries -= 1
                            self.client.sendall(message.encode()) 
                        elif(verPass == passwd):
                            print("Password is verified.")
                        
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ PASSWORD ACCEPTED ~~~~~~~~~~~~~~~~\n")
                            self.client.sendall(b"======= Security Questions =======\n")
                            self.client.sendall(b"--------- Case Sensitive ---------\n")
        
                            self.client.sendall(b"What year did you graduate from High School: ")
                            message = self.client.recv(1024)
                            self.client.sendall(b"What was your mothers maiden name: ")
                            message += self.client.recv(1024)
                            self.client.sendall(b"What was your first cars make and year (Example:HONDA2012): ")
                            message += self.client.recv(1024)
                            secureQ = message 
                            self.client.sendall(b"stop")
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ SECURITY QUESTIONS ACCEPTED ~~~~~~~~~~~~~~~~")
                            self.client.sendall(b"stop")
                            message = "--------- SECURITY QUESTIONS UPDATED ---------\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                            self.client.sendall(message.encode())
                            saltQ = bcrypt.gensalt()
                            hSecure = bcrypt.hashpw(secureQ, saltQ)
                            self.db[self.username] = {'passwd': passwd, 'SaltPass':salt, 'secureQ':hSecure, 'SaltSecure': saltQ, 'lockedBit': 0}
                            self.clientResponse()
            
    def welcomeMessage(self): 
        message ="============= WELCOME " + self.username + " TO "
        message += "\n"
        message += r" _  __     _   _               _            _       ____"
        message += "\n"
        message += r"| |/ /__ _| |_| |__   ___ _ __(_)_ __   ___( )___  / ___|  ___ _ ____   _____ _ __" 
        message += "\n"
        message += r"| ' // _` | __| '_ \ / _ \ '__| | '_ \ / _ \// __| \___ \ / _ \ '__\ \ / / _ \ '__|"
        message += "\n"
        message += r"| . \ (_| | |_| | | |  __/ |  | | | | |  __/ \__ \  ___) |  __/ |   \ V /  __/ |"   
        message += "\n"
        message += r"|_|\_\__,_|\__|_| |_|\___|_|  |_|_| |_|\___| |___/ |____/ \___|_|    \_/ \___|_|"   
        message += "\n\n\n"                                                                                    
        message += "  _          _          _          _          _\n>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,\n  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'\n  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs\n\n\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"                                                                                                                   
        self.client.sendall(message.encode())
        time.sleep(3)
        self.clientResponse()        
            
    def clientResponse(self): 
        message = self.client.recv(1024).decode()
        print(message)
    
        if (self.authUser == 1 and self.authBit == 1): 
            if ((message == "D") or (message == "d") or (message == "Download") or (message == "download")):
                self.clientDownload()
            elif ((message == "U" ) or  (message == "u") or (message == "Upload") or (message == "upload")): 
                self.clientUpload()
            elif ((message == "R" ) or ( message == "r") or (message == "Reset") or (message == "reset")): 
                self.resetSecureQ()

            elif((message =="*")):
                self.logOut()
            elif(self.authBit == 1):
                if(len(message) == 0):
                    self.client.sendall(b"start")
                    time.sleep(1)
                    self.client.sendall(b"======= NOT AN OPTION =======\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    self.clientResponse()
                else:
                    self.client.sendall(b"start")
                    time.sleep(1)
                    self.client.sendall(b"======= NOT AN OPTION =======\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    self.clientResponse() 
        
        elif((self.authUser == 0 and self.authBit == 0) or (self.authUser == 1 and self.authBit == 0)):
            if ((message == "L" ) or ( message == "l") or (message == "Login") or (message == "login")): 
                self.clientAuth()
            elif ((message == "C" ) or ( message == "c") or (message == "Create") or (message == "create")): 
                self.clientCreate()
            elif ((message == "F" ) or ( message == "f") or (message == "Forgot") or (message == "forgot")): 
                self.forgotPassword()
            elif ((message == "E") or (message ==  "e") or (message == "Exit") or (message == "exit")):
                self.client.sendall(b"end")
                time.sleep(1)
                #Out of user directory
                message = "========== BYE HOPE YOU HAD FUN ==========\n"
                message += "  _          _          _          _          _\n>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,\n  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'\n  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs\n\n\n~~~~~~~~~~~~~~~~ KATHERINE SERVER CLOSED ~~~~~~~~~~~~~~~~"                                                                                                                   
                self.client.sendall(message.encode()) 
                if (os.getcwd == self.username):
                    os.chdir("..")
                    os.chdir("..")
                    #Out of Server directory
                else:
                    os.chdir("..")
                    print("Client '%s' disconnected." % self.client)
                #close thread and secure client connect
                #calls on server to close the insecure connection 
                self.authBit = 0
                self.authUser = 0
                self.username = "Guest User"
                Server.threadClient.pop(self.client)
                self.client.close()
            
    #logOut the user
    #They will then be asked if they would like to:
    #Login
    #Create Account
    #Exit
    def logOut(self):
        self.authUser = 0
        os.chdir("..")
        self.authBit = 0
        self.client.sendall(b"logout")
        for i in Server.threadClient:
            if (Server.threadClient[i]['username'] == self.username):
                Server.threadClient[i]['username'] = None
                Server.threadClient[i]['loggedIn'] = self.authBit
                Server.threadClient[i]['dir'] = os.getcwd()
        self.username = "Guest User"
        message = "======= "+ self.username+" Logged Out =======\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n           (C)Create Account\n           (L)Login\n           (E)Exit\n~~~~~~~~~~~~~~~~"
        self.client.sendall(message.encode())
        self.clientResponse()

    #Prints out files for the client to choose from for Downloading.
    def printServerFiles(self):
        dir = os.getcwd()
        fileList = os.listdir(dir)
        count = 0 
        message = "======= PRINTING FILES ON " + self.username+ " SERVER =======\n"
        self.client.sendall(message.encode())
        for file in fileList:
            if (os.path.isfile(file)):
                fileName = file.encode()
                size = len(fileName)
                self.client.sendall(bin(size).encode())
                time.sleep(1)
                self.client.sendall(fileName)
                print(fileName)
                count += 1
            else: 
                count = count
        return count   
    
    #Finds the on the machine to make sure it exists.
    #Downloading file function        
    def findFile(self, fileName):
        if (os.path.exists(fileName)):
            print("File found!")
            return True
        else:
            return False

    #Checks to make sure File is specifically a file on the Server.     
    def fileOnServer(self, fileName, fileList):
        if (self.findFile(fileName)):
            for file in fileList:
                if ((fileName == file) and (os.path.isfile(file))):
                    print("File in user Directory, User may download!")
                    return True
        else:
            return False
            
    #Client Downloads file.
    #Will print all files on the Server
    #Ask client which file they would like.
    #Checks that file is an option
    #Sends the client the file.            
    def clientDownload(self):
        dir = os.getcwd()
        print(dir)
        self.client.sendall(b"Downloading")
        time.sleep(1)
        print("Listing out files in '% s'" % dir)   
        fileList = os.listdir(dir)
        if(self.printServerFiles() == 0):
            message = "--------- FAILED: NO FILES ON "+self.username+" ACCOUNT ---------\n        (TRY TO UPLOAD FILES TO CLOUD)\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            self.client.sendall(b"NOFile")
            time.sleep(1)
            self.client.sendall(message.encode())
            self.clientResponse()
        else: 
            print("Stop printing cloud files.")
            self.client.sendall(b"stop")
            time.sleep(1)
            self.client.sendall(b"~~~~~~~~~~~~~~~~ WHAT FILE WOULD YOU LIKE TO DOWNLOAD? ~~~~~~~~~~~~~~~~\n")
            time.sleep(2)
            fileName = self.client.recv(100).decode()
            print(fileName)
            if (self.fileOnServer(fileName, fileList) == True):
                self.writeFile(fileName)
            else:
                self.client.sendall(b"start")
                time.sleep(1)
                message = "--------- FAILED: FILE "+ fileName +" NOT ON SERVER ---------\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
                
    #Client has chosen file to download from server 
    #This method checks that this file can be opened 
    #Then sends the size and the contents of the file to client
    #Checks that the client has received all the content of the file.            
    def writeFile(self, fileName):
        try:
            file = open(fileName, 'rb')
            time.sleep(1)
            self.client.sendall(fileName.encode())
            time.sleep(3)
            message = file.read()
            print("Downloading .........")
            allSent = os.path.getsize(fileName)
            allSent = bin(allSent).encode()
            self.client.sendall(allSent)
            time.sleep(1)
            print("File is '% s' " % allSent)
            self.client.sendall(message)
            file.close()
            print("User has received all data.")
            allSent = os.path.getsize(fileName)
            binaryTest = bin(allSent)
            response = self.client.recv(1024).decode()
            print(response, binaryTest)
            if (response == binaryTest):
                print("File Downloaded")
                message = "~~~~~~~~~ " + r"₍ᐢ•(ܫ)•ᐢ₎" +" SUCCESS: FILE "+ fileName +" DOWNLOADED " + r'₍ᐢ•(ܫ)•ᐢ₎'+ " ~~~~~~~~~ \n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()         
            else: 
                print("File Not Complete!!")
                self.client.sendall(b"start")
                time.sleep(1)
                message = "--------- FAILED: FILE "+ fileName +" INCOMPLETE DOWNLOAD ---------\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
        except IOError:
            print("I can't read " + fileName)
            self.client.sendall(b"start")
            time.sleep(1)
            message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE OPENED ---------\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (D)Download\n           (U)Upload\n         (A)Account Settings\n           (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            self.client.sendall(message.encode())
            self.clientResponse()
        
    #Client would like to upload a file onto server
    #Asks client for file they would like to Upload 
    #(Most of this process takes place on client)
    #Server then creates a file with that name and writes all received data from client into file.             
    def clientUpload(self):
        dir = self.db[self.username]['dirClient']
        if (os.getcwd() != dir):
            os.chdir(dir)
        self.client.sendall(b"uploading")
        time.sleep(1)
        message = "~~~~~~~~~~~~~~~~ UPLOAD FILE TO "+ self.username+" SERVER ~~~~~~~~~~~~~~~~\nWhat file would you like to upload?"
        self.client.sendall(message.encode())
        fileName = self.client.recv(200).decode()
        if (fileName == "failed"):
            self.client.sendall(b"\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            self.clientResponse()
        else: 
            print("Client will upload " + fileName)
            if (os.path.exists(fileName)):
                print("File already on Server.\nWill over write the original file.")
                os.remove(fileName)
            try: 
                file = open(fileName, 'wb')
                fileSize = self.client.recv(50).decode()
                bytes = int(fileSize, 2)
                time.sleep(1)
                #Need to account for large files and break them apart in a logical manner.          
                print(fileName + " is '%s' in size" % bytes)
                write = self.client.recv(bytes)
                file.write(write)
                file.close()
                full = os.path.getsize(fileName)
                if (full == bytes):
                    print("File has been Uploaded")
                    message = "~~~~~~~~~~~~~~~~ " + r"₍ᐢ•(ܫ)•ᐢ₎" +" SUCCESS: FILE "+ fileName +" UPLOADED TO CLOUD " + r'₍ᐢ•(ܫ)•ᐢ₎'+ " ~~~~~~~~~~~~~~~~"
                    message += "\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    self.client.sendall(message.encode())
                    self.clientResponse()
                else: 
                    print("Upload failed only '%s' bytes downloaded" % full)
                    os.remove(fileName)
                    uploadFail = "--------- FAILED: FILE "+ fileName +" CAN NOT UPLOADED ---------\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n          (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    self.client.sendall(uploadFail.encode())
                    self.clientResponse()
            except IOError:
                print("I can't open " + fileName) 
                message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE OPENED ---------\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
            
    #Deletes all files and directories for this account.        
    def deleteAcc(self):
        dir = self.db[self.username]['dirClient']
        if (os.getcwd() != dir):
            os.chdir(dir)
        fileList = os.listdir(dir)
        for file in fileList:
            os.remove(file)
            fileList = os.listdir(dir)
        if (fileList == 0):
            os.chdir("..")
            os.removedirs(self.username)
            self.client.sendall(b"stop")
            message = "~~~~~~~~~~~~~~~~ " + r"₍ᐢ•(ܫ)•ᐢ₎" + self.username + " USER HAS BEEN DELETED " + r'₍ᐢ•(ܫ)•ᐢ₎'+ " ~~~~~~~~~~~~~~~~"
            message += "\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            self.client.sendall(message.encode())
            self.clientResponse()
        else:
            self.client.sendall(b"stop")
            message = "--------- FAILED: USER "+ self.username +" CAN NOT BE DELETED ---------\n!!!!!!!!!! MAY RESULT IN LOST USER FILES !!!!!!!!!!\n         (U)Upload\n         (D)Download\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            self.client.sendall(message.encode())
            self.clientResponse()
def main(): 
    s = Server(server=None, insecure = None, client=None, address=None, db=None, thread=None, authBit = 0, authUser = 0)
    s.sqlDatabase()
if __name__ == "__main__":
    main()