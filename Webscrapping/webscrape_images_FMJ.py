from bs4 import BeautifulSoup as soup
import urllib
import requests
import pandas as pd
import time
import os
from flask import Flask, render_template,  session, redirect, request
from flask_cors import CORS,cross_origin
import re

# define global paths for Image and csv folders
#IMG_FOLDER = os.path.join('static', 'images')
#CSV_FOLDER = os.path.join('static', 'CSVs')
#app = Flask(__name__)
#app.config['IMG_FOLDER'] = IMG_FOLDER
#app.config['CSV_FOLDER'] = CSV_FOLDER
IMG_FOLDER = os.path.join('static', 'images')
CSV_FOLDER = os.path.join('static', 'CSVs')

class CleanCache:
    '''
    this class is responsible to clear any residual csv and image files
    present due to the past searches made.
    '''

    def __init__(self, directory=None):
        self.clean_path = directory
        # only proceed if directory is not empty
        if os.listdir(self.clean_path) != list():
            # iterate over the files and remove each file
            files = os.listdir(self.clean_path)
            for fileName in files:
                print(fileName)
                os.remove(os.path.join(self.clean_path, fileName))
        print("cleaned!")



class DataCollection:
    def __init__(self):
        self.data = {
		"Name": list(),
		"Price": list(),
        "Link-For-Product": list(),
        "Size-Of-Product": list()
        }

    def get_final_data(self, commentbox=None, i=None):

        try:
            Row = commentbox.find_all("div", {"class": "astra-shop-summary-wrap"})
            #self.data["Name"].append(Row[i].a.img["alt"])  woocommerce-loop-product__title
            fullnameWithSize = Row[i].h2.get_text().strip()
            #print(fullnameWithSize)
            producttitle, Size = fullnameWithSize.split('[')
            Size_Locked = Size[:-1]
            print("Product Title",producttitle)
            print("Product Size",Size_Locked)


            self.data["Name"].append(fullnameWithSize)


            #self.data["Size-Of-Product"].append(Size_Locked)
        except:
            self.data["Name"].append("No name")

        try:

            self.data["Price"].append(
                commentbox.find_all("span", {"class": "price"})[i].get_text().strip())
            # self.data["Regular Price (PKR)"].append("Fatima")
        except:
            self.data["Price"].append('0')
 ### ------------ Link and Size-Of-Product Tags ---------------------------------
        try:
            Row = commentbox.find_all("div", {"class": "astra-shop-summary-wrap"})

            #Prod_url = Row.find({"class":"ast - loop - product__link"})
            self.data["Link-For-Product"].append(Row[i].a['href'])
            #self.data["Link-For-Product"].append(Prod_url[i])

            #self.data["Link-For-Product"].append(commentbox.find_all("div", {"class": "cstm_brnd"})[i].get_text().strip())
            # self.data["Brand Name"].append("Siddiq")
        except:
            self.data["Link-For-Product"].append('none')

        ### Work On Sizes

        try:
            self.data["Size-Of-Product"].append(Size_Locked)
            # self.data["Brand Name"].append("Siddiq")
        except:
            self.data["Size-Of-Product"].append('none')

    def get_main_HTML(self, base_URL=None, cat = None , search_string=None):
        # construct the search url with base URL and search string
        # http://yayvo.com/search/result/?q=samsung+mobiles
        search_url = f"{base_URL}/product-category/{cat}/{search_string}"
        # usung urllib read the page
        with urllib.request.urlopen(search_url) as url:
            page = url.read()
        # return the html page after parsing with bs4
        return soup(page, "html.parser")

    def get_data_dict(self):
        return self.data



    def save_as_dataframe(self, dataframe, fileName=None):
        csv_path = os.path.join(CSV_FOLDER, fileName)
        fileExtension = '.csv'
        final_path = f"{csv_path}{fileExtension}"
        # clean previous files -
        CleanCache(directory=CSV_FOLDER)
        # save new csv to the csv folder
        dataframe.to_csv(final_path, index=None)
        print("File saved successfully!!")
        return final_path

    def FMJ_Scraped(self,intent,search_string,size,cat):
        #(intent, search_string, cust_ShalwarKurta_size, cat)
        #kurta - shalwar
        base_URL = 'http://fmjclothing.jhapto.com/'

        #if (intent == 'Shirts-size'):
            #http: // fmjclothing.jhapto.com / product - category / men / shirts /
        #cat = 'men'
        #search_string = 'shirts'
        search_string = search_string.replace(" ", "-")
        print('processing, Please wait')
        get_data = DataCollection()
        yayvo_HTML = get_data.get_main_HTML(base_URL,cat, search_string)
        print(yayvo_HTML)
        print("Length")
        print(len(yayvo_HTML))
        i=0
        #while (i <= len(yayvo_HTML)):
        while (i < 12):
            get_data.get_final_data(yayvo_HTML, i)
            i = i + 1

        yayvo_Scrapped = pd.DataFrame(get_data.get_data_dict())
        print(yayvo_Scrapped)

        #yayvo_Scrapped = yayvo_Scrapped.head(15)
        return yayvo_Scrapped
