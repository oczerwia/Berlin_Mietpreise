import pandas as pd
import requests
from time import sleep
from bs4 import BeautifulSoup
import re
from random import seed, randint
from progressbar import ProgressBar
#seed(1)
import datetime
date_object = datetime.date.today()

Path_Old_DF = r'C:\Users\olive\Kaggle\Berlin Analyse\Berlin_Miete_laufend.csv'
Save_Path = r"C:\Users\olive\Kaggle\Berlin Analyse\Berlin_Miete_laufend.csv"

pbar = ProgressBar()
def scrapeWGsite(seitenanzahl):
    #zieht den html text
    seiten_liste = []
    for sitenumber in pbar(range(0,seitenanzahl)):
        link = "https://www.wg-gesucht.de/wg-zimmer-in-Berlin.8.0.1.{}.html?category=0&city_id=8&rent_type=0&noDeact=1&img=1&rent_types%5B0%5D=0".format(seitenanzahl+1)
        response = requests.get(link)
        if(response.status_code == 200):
            soup = BeautifulSoup(response.text, "html.parser")
            kacheln = soup.findAll('div',{"class": "col-sm-8 card_body"})[2:]
            seiten_liste.append(kacheln)
        else: 
            break
        sleep(randint(20,40))
    
    return seiten_liste

def createWGdataframe(liste):
    rows_list = []
    #iteration über jedes Angebot
    pattern_information = re.compile(r'[\S]{1,}')
    pattern_price = re.compile(r'\d')
    pattern_title = re.compile(r'\S{1,}')
    pattern_time_sequence = re.compile(r'\d{2}\.\d{2}.\d{4}')
    for subliste in liste:
        for inserat in subliste:
        #filtert die Zeile unter dem Titel
            precompiled_information = inserat.findAll('span')[1].string
           
            information = pattern_information.findall(precompiled_information)

            price_string = inserat.findAll('b')[0].string
            price = "".join(pattern_price.findall(price_string))

            title_string = inserat.findAll('a')[0].string.replace("\n", "")
            title = " ".join(pattern_title.findall(title_string))

            time_ = inserat.findAll('div')[6].string
            if time_ is None:
                time = None
            else:
                time = " ".join(pattern_time_sequence.findall(time_))
                
            user = inserat.findAll('span')[5].string
            
            #listen zur vereinfachten Verarbeitung der Informationen
            sizetype = []
            cityinfo = []
            #streetname = []

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

            #sucht nach Straßennummer
            if(information[-1].isnumeric()):
                Streetnumber = information.pop(-1)
            else:
                Streetnumber = None
            
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
                              "Streetnumber": Streetnumber, "Price(in €/Month)": price, 
                              "User": user, "Start_date":time_start, "End_date": time_end})
        
    angebote_DF = pd.DataFrame(rows_list)
    return angebote_DF

seiten_daten = scrapeWGsite(10)

WG_Gesucht_df = createWGdataframe(seiten_daten)
WG_Gesucht_df["Pull_Time"] = date_object

WG_Gesucht_alt = pd.read_csv(Path_Old_DF)

WG_Gesucht_df_neu = pd.concat([WG_Gesucht_df, WG_Gesucht_alt])
WG_Gesucht_df_neu.info()

WG_Gesucht_df_neu.to_csv(Save_Path)