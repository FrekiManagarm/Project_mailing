import imaplib, serial, struct, time
import json

with open('config.json') as config_data:
    print(type(config_data))
email = Mail()
# Check d'un nouveau mail toutes les minutes 

def main():


class Mail():
    def __init__(self):
        self.user= config_data.senderMail
        self.password= config_data.Password
        self.ser = serial.Serial('/dev/tty.usbmodem621', 9600)
        self.M = imaplib.IMAP4_SSL(config_data.domaineServer, '993')
        self.M.login(self.user, self.password)      
    def checkMail(self):
        self.M.select()
        self.unRead = self.M.search(None, 'UnSeen')
        return len(self.unRead[1][0].split())  
    def sendData(self):
        self.numMessages= self.checkMail()
        #turn the string into packed binary data to send int
        self.ser.write(struct.pack('B', self.numMessages))
while 1:
        print('Sending')
        email.sendData()
        time.sleep(60)

class Translation():
    def __init__(self):
        with open("new_mail", "r") as Mail_data:
            print(type(Mail_data))
        Mail_data = {email.content}
        fichier = open(".json","wt")
        fichier.write(json.dumps(Mail_data))
        fichier.close()


 
if __name__ == "__main__":
    main()

    