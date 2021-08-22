import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re

PATTERN = "https:\/\/www\.wg\-gesucht\.de\/[\d]+\.html"

def scrapeWGsite(path : str):
    response = requests.get(path)
    if(response.status_code == 200):
        soup = BeautifulSoup(response.text, "html.parser")
        pageContent = soup.findAll('div', {'class' : 'wgg_card offer_list_item'})[2:]
    else: 
        """LogDaten abspeichern"""
        pageContent = None
        pass
    return pageContent


def extractLinks(path : str):
    linkList : list = []
    with open(path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    linkData = soup.findAll('div', {"style" : "margin-bottom:10px;"})[1::2]
    for i in range(len(linkData)):
        link : str = re.search(PATTERN, linkData[i].text)[i]
        linkList.append(link)
    return linkList


def createWGdataframe(pageContent : str) -> pd.DataFrame():
    rows_list = []
    PATTERN_INFORMATION = re.compile(r'[\S]{1,}')
    PATTERN_PRICE = re.compile(r'\d')
    PATTERN_TITLE = re.compile(r'\S{1,}')
    PATTERNTIMESEQUENCE = re.compile(r'\d{2}\.\d{2}.\d{4}')
    for subliste in pageContent:
        for inserat in subliste:
        #filtert die Zeile unter dem Titel
            precompiled_information = inserat.findAll('span')[1].string
           
            information = PATTERN_INFORMATION.findall(precompiled_information)

            price_string = inserat.findAll('b')[0].string
            price = "".join(PATTERN_PRICE.findall(price_string))

            title_string = inserat.findAll('a')[0].string.replace("\n", "")
            title = " ".join(PATTERN_TITLE.findall(title_string))

            time_ = inserat.findAll('div')[6].string
            if time_ is None:
                time = None
            else:
                time = " ".join(PATTERNTIMESEQUENCE.findall(time_))
                
            user = inserat.findAll('span')[5].string
            
            sizetype = []
            cityinfo = []

            for i in range(len(information)):
                if(information[i] != "|"):
                    sizetype.append(information[i])
                else:
                    del information[0:(i+1)]
                    break

            for j in range(len(information)):
                if(information[j] != "|"):
                    cityinfo.append(information[j])
                else:
                    del information[0:(j+1)]
                    break

            if(information[-1].isnumeric()):
                streetnumber = information.pop(-1)
            else:
                streetnumber = None
            
            if time != None:
                if(len(time)> 11):
                    time_start = time[:10]
                    time_end = time[-10:]
                else:
                    time_start = time
                    time_end = None
                
            if(user == "\n"):
                user = None

            Size = sizetype[0][0]
            Type = sizetype[1]
            City = cityinfo[0]
            Quarter = cityinfo[1]
            Streetname =" ".join(information)
            rows_list.append({"Title" : title, "Size" : Size, "Type": Type,
                              "City": City, "Quarter": Quarter, "Streetname": Streetname,
                              "Streetnumber": streetnumber, "Price(in €/Month)": price, 
                              "User": user, "Start_date":time_start, "End_date": time_end})
        
    angebote_DF = pd.DataFrame(rows_list)
    return angebote_DF
