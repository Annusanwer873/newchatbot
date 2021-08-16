# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
import json
from flask import make_response
from SendEmail.sendEmail import EmailSender
from email_templates import template_reader
from Webscrapping.webscrape_images_FMJ import DataCollection
import os

IMG_FOLDER = os.path.join('static', 'images')
CSV_FOLDER = os.path.join('static', 'CSVs')
app = Flask(__name__)
app.config['IMG_FOLDER'] = IMG_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER


@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    intent = result.get("intent").get('displayName')

    if (intent == 'CourseSelection'):
        parameters = result.get("parameters")
        course_name = parameters.get("name")
        cust_name = parameters.get("stuname")
        cust_email = parameters.get("email")

        #course_name = 'DataScienceMasters'
        email_sender = EmailSender()
        template = template_reader.TemplateReader()
        email_message = template.read_course_template(course_name)
        email_sender.send_email_to_student(cust_email, email_message)

        fulfillmentText = "I have sent the brochure and a promocode valid for 10th June 2021. You can get 20% flat discount through this promocode. Enter 1 for main menu and 0 to exit the chat"

        return {
            "fulfillmentText": fulfillmentText
        }
    elif (intent == 'Help Desk'):

        parameters = result.get("parameters")
        cust_name = parameters.get("name")
        cust_contactnumber = parameters.get("number")
        #converted_cust_num = str(cust_contactnumber)

        cust_email = 'affanaminn@gmail.com'

        email_sender = EmailSender()
        template = template_reader.TemplateReader()
        course_name = 'DS'
        email_message = template.read_course_template(course_name)
        #        email_sender.send_email_to_student(cust_email, email_message)
        email_sender.send_email_to_support(cust_name,cust_contactnumber,email_message )

        fulfillmentText = "Your Number and Name has been sent to the support team via email, you will be contacted shortly, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"

        return {
            "fulfillmentText": fulfillmentText
        }
    else:
        return "nothing found"

@app.route('/',methods=['GET'])
def homePage():
	return render_template("index.html")


@app.route('/ShirtSizeMedium', methods=("POST", "GET"))
def ShirtSizeMedium():
    #if request.method == 'POST':
    try:
        intent = 'Shirts-size'
        cust_shirt_size = 'M'
        search_string = 'shirts'
        cat = 'men'


        data_scrapper_FMJ = DataCollection()
        #yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, cust_shirt_size)
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, cust_shirt_size, cat)
        newdf = yayvo_Scrapped[
            (yayvo_Scrapped['Size-Of-Product'] == 'S,M') | (yayvo_Scrapped['Size-Of-Product'] == 'S,M,L')]

        download_path = data_scrapper_FMJ.save_as_dataframe(newdf, fileName=search_string.replace("+", "_"))

        return render_template('review.html',
                               tables=[newdf.to_html(classes='data')],  # pass the df as html
                               titles=newdf.columns.values,  # pass headers of each cols
                               search_string=search_string,  # pass the search string
                               download_csv=download_path  # pass the download path for csv
                               )

    except Exception as e:
        print(e)
        return render_template("404.html")

@app.route('/ShirtSizeSmall', methods=("POST", "GET"))
def ShirtSizeSmall():
    #if request.method == 'POST':
    try:
        intent = 'Shirts-size'
        cust_shirt_size = 'S'
        search_string = 'shirts'
        cat = 'men'
        data_scrapper_FMJ = DataCollection()
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, cust_shirt_size, cat)

        newdf = yayvo_Scrapped[yayvo_Scrapped['Size-Of-Product'] == 'S,M,L']

        download_path = data_scrapper_FMJ.save_as_dataframe(newdf, fileName=search_string.replace("+", "_"))

        return render_template('review.html',
                               tables=[newdf.to_html(classes='data')],  # pass the df as html
                               titles=newdf.columns.values,  # pass headers of each cols
                               search_string=search_string,  # pass the search string
                               download_csv=download_path  # pass the download path for csv
                               )

    except Exception as e:
        print(e)
        return render_template("404.html")


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    #app.run()
