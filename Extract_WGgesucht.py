"""This file downloads and saves the whole HTML code of the website"""

import requests
from bs4 import BeautifulSoup
import datetime
from datetime import datetime as dt

now = dt.now()
CURRENTDATE = datetime.date.today()
CURRENTDATEHOUR = now.strftime("%d-%m-%Y~%H-%M")
CITIES = ["Berlin", "Münster", "Frankfurt", "Hamburg", "Münster"]


def getCityLink(city : str, pageNumber : int) -> str: 
    CITYLINK = {"Münster" : f"https://www.wg-gesucht.de/wg-zimmer-in-Munster.91.0.1.{pageNumber}.html?category=0&city_id=91&rent_type=0&sort_column=0&noDeact=1&img=1&rent_types%5B0%5D=0",
                "Frankfurt" : f"https://www.wg-gesucht.de/wg-zimmer-in-Frankfurt-am-Main.41.0.1.{pageNumber}.html?category=0&city_id=41&rent_type=0&sort_column=0&noDeact=1&img=1&rent_types%5B0%5D=0",
                "Hamburg" : f"https://www.wg-gesucht.de/wg-zimmer-in-Hamburg.55.0.1.{pageNumber}.html?category=0&city_id=55&rent_type=0&sort_column=0&noDeact=1&img=1&rent_types%5B0%5D=0",
                "Berlin" : f"https://www.wg-gesucht.de/wg-zimmer-in-Berlin.8.0.1.{pageNumber}.html?category=0&city_id=8&rent_type=0&noDeact=1&img=1&rent_types%5B0%5D=0",
                "Köln" : f"https://www.wg-gesucht.de/wg-zimmer-in-Koeln.73.0.1.{pageNumber}.html?category=0&city_id=73&rent_type=0&sort_column=0&noDeact=1&img=1&rent_types%5B0%5D=0"
                }
    return CITYLINK[city]


def scrapeWGsiteFull(path : str):
    response = requests.get(path)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
    else: 
        soup = None
    return soup


def extractSingleInsert(path : str):
    """takes single Inserts from extract Links Function and extracts them"""
    response = requests.get(path)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        soup = None
    return soup

def saveSingleInsert(city : str, insertID : int, pageContent : str):
    LOCALPATH = f"C:\\Users\\olive\\Desktop\\SINGLE_INSERT_WG_GESUCHT_{city}_{str(insertID)}.html"
    with open(LOCALPATH, "w", encoding = 'utf-8') as file:
        file.write(pageContent)
    

def saveFullInsertLocally(city : str, pagenumber : int, pageContent : str):
    LOCALPATH = f"C:\\Users\\olive\\Desktop\\HTML__WG_GESUCHT_{city}_{pagenumber}_{CURRENTDATEHOUR}.html"
    with open(LOCALPATH, "w", encoding='utf-8') as file:
        file.write(pageContent)


