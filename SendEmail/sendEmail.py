# -*- coding: utf-8 -*-
import smtplib as smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from config_reader import ConfigReader

class EmailSender:

    def send_email_to_student(self, recepient_email, message):
        try:
            EMAIL_ADDRESS = 'siddiqamin2005@gmail.com'
            EMAIL_PASSWORD = 'siddiq2020'
            #recepient_email = 'affanaminn@gmail.com'

            self.config_reader=ConfigReader()
            self.configuration=self.config_reader.read_config()

            # instance of MIMEMultipart
            self.msg = MIMEMultipart()

            # storing the senders email address
            self.msg['From'] = self.configuration['SENDER_EMAIL']

            # storing the receivers email address
            self.msg['To'] = recepient_email


            # storing the subject
            self.msg['Subject'] = self.configuration['EMAIL_SUBJECT']

            # string to store the body of the mail
            #body = "This will contain attachment"
            body=message

            # attach the body with the msg instance
            self.msg.attach(MIMEText(body, 'html'))


            # instance of MIMEBase and named as p
            self.p = MIMEBase('application', 'octet-stream')
            print("Working till here 1")


            # creates SMTP session
            #self.smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            #self.smtp = smtplib.SMTP_SSL('smtp.gmail.com')
            print("Working till here 2")
            msg = "Hello Everyone, This is our Test email"
            self.text = self.msg.as_string()


            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                #smtp.login(self.msg['SENDER_EMAIL'], self.configuration['PASSWORD'])
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                #smtp.send_message(msg)
                smtp.sendmail(self.msg['From'] , recepient_email, self.text)


            #self.smtp.quit()
        except Exception as e:
            print('the exception is '+str(e))

    def send_email_to_support(self,cust_name,converted_cust_num,body):
            try:
                print("Working till here in Send Email to support ---00")
                EMAIL_ADDRESS = 'siddiqamin2005@gmail.com'
                EMAIL_PASSWORD = 'siddiq2020'
                print("Working till here in Send Email to support ---0.5")
                self.config_reader = ConfigReader()
                self.configuration = self.config_reader.read_config()

                # instance of MIMEMultipart
                self.msg = MIMEMultipart()

                # storing the senders email address
                self.msg['From'] = self.configuration['SENDER_EMAIL']
                print("Working till here in Send Email to support ---1")


                # storing the subject
                self.msg['Subject'] = self.configuration['SALES_TEAM_EMAIL_SUBJECT']
                print("Working till here in Send Email to support ---2")

                # string to store the body of the mail
                # body = "This will contain attachment"
                converted_cust_num = str(converted_cust_num)

                body = body.replace('cust_name',cust_name)
                #cust_contact2 = cust_contact.as_string()
                body = body.replace('cust_contact', converted_cust_num)

                #body = body.replace('cust_contact', cust_contact)
                print("Working till here in Send Email to support ---3")


                # attach the body with the msg instance
                self.msg.attach(MIMEText(body, 'html'))

                # instance of MIMEBase and named as p
                self.p = MIMEBase('application', 'octet-stream')
                print("Working till here in Send Email to support ---4")
                #txt = "Customer Name is {customer-name} and his Contactnumber is {contanct-no}"
                #print(txt.format(customer-name=cust_name))
                #self.support_team_email = self.configuration['SALES_TEAM_EMAIL']
                support_team_email = 'siddiqamin2005@gmail.com'
                self.text = self.msg.as_string()
                self.text2 = "Working in this"

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    # smtp.login(self.msg['SENDER_EMAIL'], self.configuration['PASSWORD'])
                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    # smtp.send_message(msg)
                    smtp.sendmail(self.msg['From'], support_team_email, self.text)




            except Exception as e:
                print('the exception is ' + str(e))
