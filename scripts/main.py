import imaplib, serial, struct, time, os
import json

with open('/config.json') as config:
    print(type(config))

email = Mail()
# Check d'un nouveau mail toutes les minutes 



class Mail():
    def __init__(self):
        self.user= config.senderMail
        self.password= config.Password
        self.ser = serial.Serial('/dev/tty.usbmodem621', 9600)
        self.M = imaplib.IMAP4_SSL(config.domaineServer, '993')
        self.M.login(self.user, self.password)      
    def checkMail(self):
        self.M.select()
        self.unRead = self.M.search(None, 'UnSeen')
        return len(self.unRead[1][0].split())  
    def sendData(self):
        self.numMessages= self.checkMail()
        #turn the string into packed binary data to send int
        self.ser.write(struct.pack('B', self.numMessages))  
    


# Ci dessous un essai de conversion du Mail en JSON
class Translation():
    def __init__(self):
        with open("new_mail", "x") as Mail_data:
            print(type(Mail_data))
        Mail_data = {email.content}
        fichier = open("new_mail.json","wt")
        fichier.write(json.dumps(Mail_data))
        fichier.close()

# Ci dessous 
class Stock():
    with open('/config.json') as Mail_data:
        fichier = Mail_data.os.path.join(Mail_data.repertoire)
    
while 1:
    print('Sending')
    email.sendData()
    time.sleep(60)
 
if __name__ == "__main__":
    main()


