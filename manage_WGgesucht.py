"""
Managen der verschiedenen ETL Stages für WG Gesucht
"""
from .Extract_WGgesucht import *
from .Transform_WGgesucht import *
#from .Loading_WGgesucht import *

if __name__ == '__main__':
    for pageNumber in range(1,6):
        cityLink = getCityLink("Berlin", pageNumber)
        content = scrapeWGsiteFull(cityLink)
        saveFullInsertLocally("Berlin", pageNumber, str(content))


"""
5 Mal täglich extracten
1 Mal täglich transformen und dann direkt loaden
1 Mal pro Woche aus der Datenbank holen
"""