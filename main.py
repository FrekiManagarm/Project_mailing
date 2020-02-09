import imaplib, serial, struct, time
import json

with open('config.json') as config_data:
    print(type(config_data))

# Check d'un nouveau mail toutes les minutes 

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

def main():
        
    email = Mail()
    
    while 1:
        print('Sending')
        email.sendData()
        time.sleep(60)
 
if __name__ == "__main__":
    main()

    