# import imaplib, serial, struct, time
# import json

# with open("config.json") as config:
#     print(type(config))

# # Check d'un nouveau mail toutes les minutes 

# class Mail():
#     def __init__(self):
#         self.user= config.senderMail
#         self.password= config.Password
#         self.ser = serial.Serial('/dev/tty.usbmodem621', 9600)
#         self.M = imaplib.IMAP4_SSL(config.domaineServer, '993')
#         self.M.login(self.user, self.password)      
#     def checkMail(self):
#         self.M.select()
#         self.unRead = self.M.search(None, 'UnSeen')
#         return len(self.unRead[1][0].split())  
#     def sendData(self):
#         self.numMessages= self.checkMail()
#         #turn the string into packed binary data to send int
#         self.ser.write(struct.pack('B', self.numMessages))       

# def main():
    
#     email = Mail()
    
#     while 1:
#         print('Sending')
#         email.sendData()
#         time.sleep(60)
 
# if __name__ == "__main__":
#     main()

import imaplib
import email
import json 

with open("/conf.json") as conf:
    print(type(conf))

email_address = conf.senderMail 
email_pass = conf.Password 

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_address, email_pass)

num_of_mail = 0

while True:

    mail.select('inbox')

    type, data = mail.search(None, '(UNSEEN)')
    mail_ids = data[0]
    id_list = mail_ids.split()

    if len(id_list) > num_of_mail:
        print('New Mail Found...\n')

        for i in range(int(id_list[-1]), int(id_list[0]) -1, -1):
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    email_body = msg.get_payload()[0].get_payload()
                    file = open('EMAIL.txt','w')
                    file.write(email_from)
                    file.write(email_subject)
                    file.write(email_body)
                    file.close()
        num_of_mail = len(id_list)