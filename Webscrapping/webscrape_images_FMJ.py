from bs4 import BeautifulSoup as soup
import urllib
import requests
import pandas as pd
import time
import os
from flask import Flask, render_template,  session, redirect, request
from flask_cors import CORS,cross_origin

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
        "Link-For-Product": list()
        #"Size-Of-Product": list()
        }

    def get_final_data(self, commentbox=None, i=None):

        try:
            Row = commentbox.find_all("div", {"class": "astra-shop-summary-wrap"})
            #self.data["Name"].append(Row[i].a.img["alt"])  woocommerce-loop-product__title
            self.data["Name"].append(Row[i].h2)
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
        ### Work On Sizes Later
        # try:
        #     self.data["Size-Of-Product"].append(commentbox.find_all("div", {"class": "cstm_brnd"})[i].get_text().strip())
        #     # self.data["Brand Name"].append("Siddiq")
        # except:
        #     self.data["Size-Of-Product"].append('none')

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

    def FMJ_Scraped(self,intent,cust_shirt_size):

        base_URL = 'http://fmjclothing.jhapto.com/'

        #if (intent == 'Shirts-size'):
            #http: // fmjclothing.jhapto.com / product - category / men / shirts /
        cat = 'men'
        search_string = 'shirts'
        search_string = search_string.replace(" ", "-")
        print('processing, Please wait')
        get_data = DataCollection()
        yayvo_HTML = get_data.get_main_HTML(base_URL,cat, search_string)
        print(yayvo_HTML)
        i=0
        while (i <= len(yayvo_HTML)):
            get_data.get_final_data(yayvo_HTML, i)
            i = i + 1

        yayvo_Scrapped = pd.DataFrame(get_data.get_data_dict())
        yayvo_Scrapped = yayvo_Scrapped.head(5)
        return yayvo_Scrapped
        # print("---------chkinggg -------------")
        # print(yayvo_Scrapped.head())
        # download_path = get_data.save_as_dataframe(yayvo_Scrapped, fileName=search_string.replace("+", "_"))
        # #finish = time.perf_counter()
        # #return yayvo_Scrapped
        # render_template('review.html',
        #                        tables=[yayvo_Scrapped.to_html(classes='data')],  # pass the df as html
        #                        titles=yayvo_Scrapped.columns.values,  # pass headers of each cols
        #                        search_string=search_string,  # pass the search string
        #                        download_csv=download_path  # pass the download path for csv
        #                        )
