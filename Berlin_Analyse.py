import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

WG_Gesucht_alt = pd.read_csv(r'C:\Users\SESA612698\Jupyter_Scripte\Berlin_Miete_laufend.csv')

WG_Gesucht_df_neu = WG_Gesucht_alt[["Title", "Size", "Type",
                                 "City", "Quarter", "Streetname",
                                 "Streetnumber", "Price(in €/Month)", 
                                 "User", "Start_date", "End_date", 
                                 "Pull_Time"]]


WG_Gesucht_df_neu = WG_Gesucht_df_neu.drop_duplicates(subset = ["Title", "Size", 
                                                                "Type", "City",
                                                                "Quarter","Streetname",
                                                                "Streetnumber", "Price(in €/Month)",
                                                                "User", "Start_date", 
                                                                "End_date"] , keep ="first", inplace = False)

WG_Gesucht_df_neu["Quarter"] = ["Charlottenburg" if x.find("Charlottenburg")!= -1 else x for x in WG_Gesucht_df_neu["Quarter"]]
WG_Gesucht_df_neu["Quarter"] = ["Kreuzberg" if x.find("Kreuzberg")!= -1 else x for x in WG_Gesucht_df_neu["Quarter"]]
Quarter = WG_Gesucht_df_neu["Quarter"].value_counts().reset_index()

Quarter_set = set(WG_Gesucht_df_neu["Quarter"])
for quarter in Quarter_set:
    if WG_Gesucht_df_neu[WG_Gesucht_df_neu["Quarter"] == quarter].count()[0] < 10:
        WG_Gesucht_df_neu = WG_Gesucht_df_neu[~(WG_Gesucht_df_neu["Quarter"] == quarter)]

WG_Gesucht_df_neu = WG_Gesucht_df_neu[WG_Gesucht_df_neu["Price(in €/Month)"] > 200]

Quarter_count = pd.DataFrame(WG_Gesucht_df_neu["Quarter"].value_counts()).reset_index()
g = sns.barplot(data = Quarter_count[:15], x = "index", y = "Quarter")
g.set_xticklabels(g.get_xticklabels(), rotation = 90)
plt.show()

plt.subplots(figsize = (15,10))
ax = sns.boxplot(x = WG_Gesucht_df_neu["Quarter"], y = WG_Gesucht_df_neu["Price(in €/Month)"], data = WG_Gesucht_df_neu)
ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)

plt.show()

WG_Gesucht_df_neu["Time_delta"] = 0
for num,delta in enumerate(WG_Gesucht_df_neu):
    try:
        WG_Gesucht_df_neu["Time_delta"][num] = WG_Gesucht_df_neu["End_date"][num] - WG_Gesucht_df_neu["Start_date"][num]
    except:
        WG_Gesucht_df_neu["Time_delta"][num] = 100000000
        
        
WG_Gesucht_df_neu["Start_date"] = [datetime.strptime(x, "%d.%m.%Y") for x in WG_Gesucht_df_neu["Start_date"]]
WG_Gesucht_df_neu["End_date"] = WG_Gesucht_df_neu["End_date"].fillna(0).astype(str)
WG_Gesucht_df_neu["End_date"] = [datetime.strptime(x, "%d.%m.%Y") if x != "0" else x for x in WG_Gesucht_df_neu["End_date"]]


WG_Gesucht_df_neu["Time_delta"] = 0
for num,delta in enumerate(WG_Gesucht_df_neu):
    if WG_Gesucht_df_neu["End_date"][num] != "0":
        WG_Gesucht_df_neu["Time_delta"][num] = (WG_Gesucht_df_neu["End_date"][num] - WG_Gesucht_df_neu["Start_date"][num]).days