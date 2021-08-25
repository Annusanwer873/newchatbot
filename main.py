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

    elif (intent == 'Shirts-size'):
        parameters = result.get("parameters")
        cust_shirt_size = parameters.get("Size")
        print(cust_shirt_size)

        if(cust_shirt_size == 'S'):
            str = "You have selected {customer_size} Shirt Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=cust_shirt_size, link="https://api-sendemails.herokuapp.com/ShirtSizeSmall")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}

        elif (cust_shirt_size == 'M'):
            str = "You have selected {customer_size} Shirt Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=cust_shirt_size, link="https://api-sendemails.herokuapp.com/ShirtSizeMedium")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}
        elif (cust_shirt_size == 'L'):
            str = "You have selected {customer_size} Shirt Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=cust_shirt_size, link="https://api-sendemails.herokuapp.com/ShirtSizeLarge")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}
        else:
            fulfillmentText = "We Donot have this Shirt Size, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}


    elif (intent == 'ShalwarKurta-size'):
        parameters = result.get("parameters")
        cust_ShalwarKurta_size = parameters.get("Size")
        #print(cust_shirt_size)


        if (cust_ShalwarKurta_size == 'M'):
            str = "You have selected {customer_size} Shalwar Kurta Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=cust_ShalwarKurta_size,
                              link="https://api-sendemails.herokuapp.com/ShalwarKurtaSizeMedium")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}
        elif (cust_ShalwarKurta_size == 'L'):
            str = "You have selected {customer_size} Shalwar Kurta Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=cust_ShalwarKurta_size, link="https://api-sendemails.herokuapp.com/ShalwarKurtaSizeLarge")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}
        else:
            fulfillmentText = "We Donot have this Size, Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}

    elif (intent == 'Women-kurti'):
        parameters = result.get("parameters")
        Women_Kurti_Size = parameters.get("Size")
        if (Women_Kurti_Size == 'M'):
            str = "You have selected {customer_size} Kurti Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=Women_Kurti_Size,
                              link="https://api-sendemails.herokuapp.com/KurtiSizeMedium")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}

        elif (Women_Kurti_Size == 'L'):
            str = "You have selected {customer_size} Kurti Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=Women_Kurti_Size,
                              link="https://api-sendemails.herokuapp.com/KurtiSizeLarge")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}


    elif (intent == 'Women-Trouser'):
        parameters = result.get("parameters")
        Women_Trouser_Size = parameters.get("Women-Trouser-Size")

        if (Women_Trouser_Size == 'M'):
            str = "You have selected {customer_size} Trouser Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=Women_Trouser_Size,
                              link="https://api-sendemails.herokuapp.com/WoTrouserMedium")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}

        elif (Women_Trouser_Size == 'L'):
            str = "You have selected {customer_size} Trouser Size, Please Proceed to our FMJ Recommendation engine through given link \n {link} \n Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            str2 = str.format(customer_size=Women_Trouser_Size,
                              link="https://api-sendemails.herokuapp.com/WoTrouserLarge")

            fulfillmentText = str2  # "You have selected , Enter 1 for main menu and 0 to exit the chat, Thanks. !!!"
            return {
                "fulfillmentText": fulfillmentText}


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

@app.route('/ShirtSizeLarge', methods=("POST", "GET"))
def ShirtSizeLarge():
    #if request.method == 'POST':
    try:

        intent = 'Shirts-size'
        cust_shirt_size = 'L'
        search_string = 'shirts'
        cat = 'men'
        data_scrapper_FMJ = DataCollection()
        #yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, cust_shirt_size)
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, cust_shirt_size, cat)
        print("HEad ----------------------")
        print(yayvo_Scrapped.head())
        #newdf = yayvo_Scrapped[yayvo_Scrapped['Name'] == "Camo Shirt with Detachable Hoodie [S,L]"]
        newdf = yayvo_Scrapped[(yayvo_Scrapped['Size-Of-Product'] == 'S,L') | (yayvo_Scrapped['Size-Of-Product'] =='S,M,L')]

        download_path = data_scrapper_FMJ.save_as_dataframe(newdf, fileName=search_string.replace("+", "_"))
        #download_path = data_scrapper_FMJ.save_as_dataframe(yayvo_Scrapped, fileName=search_string.replace("+", "_"))

        return render_template('review.html',
                               tables=[newdf.to_html(classes='data')],  # pass the df as html
                               titles=newdf.columns.values,  # pass headers of each cols
                               search_string=search_string,  # pass the search string
                               download_csv=download_path  # pass the download path for csv
                               )

    except Exception as e:
        print(e)
        return render_template("404.html")



### ---------------------------------------------------------------------------------------####


@app.route('/ShalwarKurtaSizeMedium', methods=("POST", "GET"))
def ShalwarKurtaSizeMedium():
    #if request.method == 'POST':
    try:


        intent = 'ShalwarKurta-size'
        cust_ShalwarKurta_size = 'M'
        search_string = 'Kurta Shalwar'
        cat = 'men'


        data_scrapper_FMJ = DataCollection()
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, cust_ShalwarKurta_size,cat)
        newdf = yayvo_Scrapped[(yayvo_Scrapped['Size-Of-Product'] == 'S,M') | (yayvo_Scrapped['Size-Of-Product'] == 'S,M,L')]

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


@app.route('/ShalwarKurtaSizeLarge', methods=("POST", "GET"))
def ShalwarKurtaSizeLarge():
    #if request.method == 'POST':
    try:
        intent = 'ShalwarKurta-size'
        cust_ShalwarKurta_size = 'L'
        search_string = 'Kurta Shalwar'
        cat = 'men'


        data_scrapper_FMJ = DataCollection()
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, cust_ShalwarKurta_size, cat)
        newdf = yayvo_Scrapped[
            (yayvo_Scrapped['Size-Of-Product'] == 'S,L') | (yayvo_Scrapped['Size-Of-Product'] == 'S,M,L')]

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



### ---------------------------------------------------------------------------------------####
### ---------------------------------!!!  -- -   Women Fashion Starts ..... !!!! ------------------------------------------------------####


@app.route('/KurtiSizeMedium', methods=("POST", "GET"))
def KurtiSizeMedium():
    #if request.method == 'POST':
    try:
        intent = 'Women-kurti'
        size = 'M'
        search_string = 'kurti'
        cat = 'women'


        data_scrapper_FMJ = DataCollection()
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, size, cat)


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


@app.route('/KurtiSizeLarge', methods=("POST", "GET"))
def KurtiSizeLarge():
    #if request.method == 'POST':
    try:
        intent = 'Women-kurti'
        size = 'L'
        search_string = 'kurti'
        cat = 'women'


        data_scrapper_FMJ = DataCollection()
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, size, cat)
        newdf = yayvo_Scrapped[
            (yayvo_Scrapped['Size-Of-Product'] == 'S,L') | (yayvo_Scrapped['Size-Of-Product'] == 'S,M,L')]

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


### -----------------------------------------------------------------------------------------------------------------##

@app.route('/WoTrouserLarge', methods=("POST", "GET"))
def WoTrouserLarge():
    #if request.method == 'POST':
    try:
        intent = 'Women-Trouser' #change
        size = 'L'
        search_string = 'trousers-women'
        cat = 'women'


        data_scrapper_FMJ = DataCollection()
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, size, cat)
        newdf = yayvo_Scrapped[
            (yayvo_Scrapped['Size-Of-Product'] == 'S,L') | (yayvo_Scrapped['Size-Of-Product'] == 'S,M,L')]

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


@app.route('/WoTrouserMedium', methods=("POST", "GET"))
def WoTrouserMedium():
    #if request.method == 'POST':
    try:
        intent = 'Women-Trouser'
        size = 'M'
        search_string = 'trousers-women'
        cat = 'women'


        data_scrapper_FMJ = DataCollection()
        yayvo_Scrapped = data_scrapper_FMJ.FMJ_Scraped(intent, search_string, size, cat)

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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    #app.run()
