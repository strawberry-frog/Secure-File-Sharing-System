README 

You can either run this code on the same machine or separate I have the files in folders to make it easier depending on the set up. 

Project files for same machine:
    client.py
    server.py
    ca.key
    ca.crt
    server.sh
    client.sh

Project files for implementation on separate machines: 
    client-Projects:
        ca.key
        ca.crt
        client.sh
        client.py

    server-Projects:
        ca.key
        ca.crt
        server.sh
        server.py

Just-In-Case files:
    client.crt
    client.key
    client.pem
    client-extensions.txt
    server.pem
    server.key
    server.crt
    server-extensions.text

The first step is placing these into a 

Linux system for the server and using the command:
    
Ready for the certificate creation:
    bash server.sh

You will be asked for prompts here is what I suggest:

    Country Name: US
    State or Province: VA
    Locality Name: Harrisonburg
    Organization Name: KatherineServerLLC
    Organizational Unit: Security
    Common Name: Server
    Email: your email
    challenge Password: cookie
    company name: Blank 


The Common Name and password MUST Be those or this will not work. 

Linux system for client and using the command:

Ready for the certificate creation:
    bash client.sh 

You will be asked for prompts here is what I suggest: 
    Country Name: US
    State or Province: VA
    Locality Name: Harrisonburg
    Organization Name: KatherineServerLLC
    Organizational Unit: Security
    Common Name: Client
    Email: your email
    challenge Password: cookie
    company name: Blank 

The Common Name and password MUST Be those or this will not work. 

This program moves all files into the designated folders. 

Server machine:
Commands:
    cd ~/server
    source bin/activate
results:
    (python)username@hostname: 
Now server is ready! Run code with command:
    python server.py 

Client machine:
Commands:
    cd ~/client
    source bin/activate
results:
    (python)username@hostname: 
Now client is ready! Run code with command:
    python client.py 

**** For more then one client just run client.bash is a different folder then server or any other client!****

(I have given you server-extension.txt and client-extensions.txt encase their is an issue and you need to run this is your environment before you execute server or client make sure to not have these their or change the name because I believe that will throw an error from the bash script.
I have also included server.pem, server.key, server.crt, client.pem, client.key, client.crt, client-extension.txt, and server-extension.txt. Just encase Bash script doesn't work.)



For testing: 
Username: Katherine 
Password: Fish$!NThe3
Security Questions: 

What year did you graduate from High School: 2019                  
What was your mothers maiden name: Hager                           
What was your first cars make and year (Example:HONDA2012): HONDA2012 - your view


username: admin
password: admin$et561

What year did you graduate from High School: 2000                  
What was your mothers maiden name: Coffee                           
What was your first cars make and year (Example:HONDA2012): BMW2015 


Once Server is connected and listening it will say: 
    Socket was created

Once your client is running it will connect with the server and the server will print the clients certificate. 
The server will print:
    Inside Katherine(Server) directory!
    Admin user has been created!
    Katherine user has been created!
    Waiting for connection.....

The client will print: 

  _          _          _          _          _
>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,
  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'
  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs

************ WELCOME TO KATHERINE'S SERVER ************
~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~
         (L)Login
         (C)Create account
         (E)Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Inputs can be:
L, l, Login, login, C, c, Create, create, E, e, Exit, exit
 There are 2 automatically created clients:
    admin 
    Katherine 
    
Login is selected: L, l. Login,login
User will get prompted by server:

username: admin 

- press Enter the server will then prompt. 

Enter password: admin$et561 - your view will be (***********)

- If the password is entered correctly the server will then send the user the log in page.
- Else if the password is incorrect you wil be prompted 2 more times to enter the correct password. On the third attempt the server will send the user options:

************ WELCOME TO KATHERINE'S SERVER ************
~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~
         (L)Login
         (C)Create account
         (F)Forgot password
         (E)Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Inputs can be:
L, l, Login, login, C, c, Create, create, F, f, Forgot, forgot E, e, Exit, exit

Forgot password is selected: F, f, Forgot, forgot 
User is prompted by server: (For admin user)
Answers are case sensitive:
    What year did you graduate from High School: 2000                   - your view (****)
    What was your mothers maiden name: Coffee                           - your view (******)
    What was your first cars make and year (Example:HONDA2012): BMW2015 - your view (*******)

- If the security questions are entered correctly. User will be prompted to create a password with the specific conditions:
~~~~~~~~~~~~~~~~ PASSWORD MUST CONTAIN ~~~~~~~~~~~~~~~~
ONE lowercase letter
ONE uppercase letter
ONE number (0123456789)
ONE special character(~!@#$%^&*()_-+=><[{]}|/?)

Enter Password: ***********

- Once the Password is entered it will prompt the user to verify the password.

Verify Password: ***********

- Once it is verified the user is prompted once again, This is also the out come if the user gets the password verification wrong and the password will not be updated for this user.:
************ WELCOME TO KATHERINE'S SERVER ************
~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~
         (L)Login
         (C)Create account
         (E)Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Else if the security questions are incorrect you wil be prompted 2 more times to enter the correct password. On the third attempt the server will send the user options:

************ WELCOME TO KATHERINE'S SERVER ************
~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~
         (L)Login
         (C)Create account
         (E)Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

But now admin is locked and unable to be logged in with. Safety feature for if anyone tries to reset the password.



This is the one and only time you will be given this prompt is on logging in and getting the password wrong. 


Inputs: C, c, Create, create


Create client will allow for a user to create a client to login. 
they will be prompted for a username, which is check to see if it is unique if it is not unique then they will get 2 more attempts to give the server a unique username. If non is given the they will get the prompt:
************ WELCOME TO KATHERINE'S SERVER ************
~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~
         (L)Login
         (C)Create account
         (E)Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


If they give a unique username before the this attempt then the user will be told their username was accepted and prompted for a password creation. This password will be hidden form users view with ***** instead of plain text. 
Server prompt: All these prompts will be (*********) for view
~~~~~~~~~~~~~~~~ PASSWORD MUST CONTAIN ~~~~~~~~~~~~~~~~
ONE lowercase letter
ONE uppercase letter
ONE number (0123456789)
ONE special character(~!@#$%^&*()_-+=><[{]}|/?)
AT LEAST 8 characters in length

- Once password passes the checks the server will prompt the user for: 
    What year did you graduate from High School:
    What was your mothers maiden name:
    What was your first cars make and year (Example:HONDA2012):

- These take any input (not blank) just make sure you remember it. This will also be kept from users view so as to not expose the plaintext. Once the user can successfully log in to an account they will be prompted with: 
  _          _          _          _          _
>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,
  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'
  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs


~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~
           (U)Upload File
           (D)Download File
           (A)Account Settings
           (*)LogOut
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

admin: 

Input: *
 - If a users prompts * in the prompt it will allow them to Log out of the account and then prompt them with: 
************ WELCOME TO KATHERINE'S SERVER ************
~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~
         (L)Login
         (C)Create account
         (E)Exit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

!If a User attempts to enter a option that is not in the correct place such as L while logged in they will be told this is not an option. !

Bugs:
    - Multiple can be accepted by the server but not authenticated so the client will be "connected" but it will cause an error that will not allow it to fully connect to the server due to the servers ca.crt file not being able to be found I think this is due to the change in directories when a user starts moving around the system. 

    - On that same issue If the server has an exception or the user exits incorrectly, or even sometimes correctly  the server will also need to be reset. I believe my threads are the issue there. 

    - Not a bug but (A) leads no not an error or an issue just will tell you not an option. 
    - any blank inputs for password, username, or prompts will lead to never ending loops. so dont do that. 


If te certificates or bash script give any issues I have all the prompts and inputs listed below but also I am giving you the actual certs as well for client and server as long as they are in the same directory as teh codes they should work. 
 

mkdir ~/project
virtualenv -p /usr/bin/python3 ~/project
cd ~/project
source bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install bcrypt -server needs bcrypt to work 
pip install maskpass -user need maskpass to work


Commands I used to create certificate authority: 
openssl ecparam -name prime256v1 -genkey -noout -out ca.key
openssl req -new -x509 -sha256 -key ca.key -out ca.crt

openssl ecparam -name prime256v1 -genkey -noout -out server.key
openssl req -new -sha256 -key server.key -out server.csr
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.pem -days 1000 -sha256 -extfile server-extensions.txt

Client commands: 
openssl req -new -sha256 -key client.key -out client.csr
openssl ecparam -name prime256v1 -genkey -noout -out client.key
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.pem -days 1000 -sha256 -extfile client-extensions.txt

Certificate Information: CA
Country Name: US
State or Province: VA
Locality Name: Harrisonburg
Organization Name: KatherineServerLLC
Organizational Unit: Security
Common Name: CA
Email: your email
challenge Password: cookie
company name: Blank

Certificate Information: Server 
Country Name: US
State or Province: VA
Locality Name: Harrisonburg
Organization Name: KatherineServerLLC
Organizational Unit: Security
Common Name: Server
Email: your email
challenge Password: cookie
company name: Blank 

Certificate Information: Client
Country Name: US
State or Province: VA
Locality Name: Harrisonburg
Organization Name: KatherineServerLLC
Organizational Unit: Security
Common Name: Client
Email: your email
challenge Password: cookie
company name: Blank 

