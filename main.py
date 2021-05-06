# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import json
from flask import make_response
from SendEmail.sendEmail import EmailSender
from email_templates import template_reader
import os



app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def webhook():
    #print("Affan here ........")
    #print("Request:")
    req = request.get_json(silent=True, force=True)
    #print(json.dumps(req, indent=4))
    res = processRequest(req)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

# processing the request from dialogflow
def processRequest(req):
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')

    if (intent == 'Get Promotional Emails'):
        parameters = result.get("parameters")
        cust_name = parameters.get("name")
        cust_email = parameters.get("email")
        course_no = "1"
        course_name = 'DataScienceMasters'
        email_sender = EmailSender()
        template = template_reader.TemplateReader()
        email_message = template.read_course_template(course_name)
        email_sender.send_email_to_student(cust_email, email_message)

        fulfillmentText = "I have sent the brochure and a promocode valid for 10th June 2021. You can get 20% flat discount through this promocode. Enter 1 for main menu and 0 to exit the chat"

        return {
            "fulfillmentText": fulfillmentText
        }
    elif (intent == 'Contact Customer Support'):
        parameters = result.get("parameters")
        cust_name = parameters.get("name")
        cust_contactnumber = parameters.get("number")
        converted_cust_num = str(cust_contactnumber)

        cust_email = 'affanaminn@gmail.com'

        email_sender = EmailSender()
        template = template_reader.TemplateReader()
        course_name = 'DS'
        email_message = template.read_course_template(course_name)
        #        email_sender.send_email_to_student(cust_email, email_message)
        email_sender.send_email_to_support(cust_name,converted_cust_num,email_message )

        fulfillmentText = "Number has sent to the support team via email, you will be contacted shortly, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"

        return {
            "fulfillmentText": fulfillmentText
        }

    elif (intent == 'Shirts-size'):
        parameters = result.get("parameters")
        cust_shirt_size = parameters.get("Size")
        #print(cust_shirt_size)

        str = "You have selected {customer_size} Shirt Size, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
        str2 = str.format(customer_size = cust_shirt_size)


        fulfillmentText = str2#"You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"

        return {
            "fulfillmentText": fulfillmentText
        }

    elif (intent == 'Pants-weist'):
        parameters = result.get("parameters")
        cust_pant_weist = parameters.get("Weist")
        #cust_pant_weist2 = str(cust_pant_weist)
        #print(cust_shirt_size)
        str = "You have selected {customer_Weist_size} Pant Waist, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
        str2 = str.format(customer_Weist_size = cust_pant_weist)


        fulfillmentText = str2#"You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"

        return {
            "fulfillmentText": fulfillmentText
        }

    elif (intent == 'ShalwarKurta-size'):
        parameters = result.get("parameters")
        cust_ShalwarKurta_size = parameters.get("Size")
        #print(cust_shirt_size)
        str = "You have selected {customer_size} Shalwar Kurta Size, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
        str2 = str.format(customer_size = cust_ShalwarKurta_size)


        fulfillmentText = str2#"You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"

        return {
            "fulfillmentText": fulfillmentText
        }

    elif (intent == 'Shoe-Size'):
        parameters = result.get("parameters")
        cust_Shoe_size = parameters.get("Size")
        #cust_Shoe_size = str(cust_Shoe_size)
        # print(cust_shirt_size)
        str = "You have selected {customer_shoe_size} shoes Size, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
        str2 = str.format(customer_shoe_size=cust_Shoe_size)

        fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"

        return {
            "fulfillmentText": fulfillmentText
        }


    else:
        return "nothing found"







    #log = logger.Log()

    sessionID=req.get('responseId')
    result = req.get("queryResult")
    user_says=result.get("queryText")
    #log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")

    #cust_contact = parameters.get("phn_no")
    #course_no = parameters.get("number")
    cust_contact = "12345"
    course_no = "1"
    cust_name = parameters.get("name")
    cust_email = parameters.get("email")
    #cust_contact = parameters.get("number")

    print(cust_name)
    print(cust_contact)
    print(cust_email)
    #print(course_no)
    course_name = 'DataScienceMasters'

    # if(course_no == 1):
    #     course_name = 'DataScienceMasters'
    # elif(course_no == 2):
    #     course_name = 'MachineLearningMasters'
    # elif(course_no == 3):
    #     course_name ='DeepLearningMasters'
    # else:
    #     course_name ='NLPMasters'

    intent = result.get("intent").get('displayName')
    print(course_name)
    if (intent=='Get Promotional Emails'):
        email_sender=EmailSender()
        template= template_reader.TemplateReader()
        email_message=template.read_course_template(course_name)
        email_sender.send_email_to_student(cust_email,email_message)

        fulfillmentText="I have sent the brochure and a promocode valid for 10th June 2021. You can get 20% flat discount through this promocode. Enter 1 for main menu and 0 to exit the chat"

        return {
            "fulfillmentText": fulfillmentText
        }

    elif (intent == 'Contact Customer Support'):
        email_sender = EmailSender()
        template = template_reader.TemplateReader()
        email_message = template.read_course_template(course_name)
#        email_sender.send_email_to_student(cust_email, email_message)
        email_sender.send_email_to_support(cust_email, email_message)

        fulfillmentText = "Number has sent to the support team via email, you will be contacted shortly, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"

        return {
            "fulfillmentText": fulfillmentText
        }


    else:
        return "nothing found"




if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    #app.run()
