"""
Managen der verschiedenen ETL Stages für WG Gesucht
"""
from .Extract_WGgesucht import *
from .Transform_WGgesucht import *

if __name__ == '__main__':
    for pageNumber in range(1,6):
        cityLink = getCityLink("Berlin", pageNumber)
        content = scrapeWGsiteFull(cityLink)
        saveLocally("Berlin", pageNumber, str(content))
