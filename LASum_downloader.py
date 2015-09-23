# -*- coding: utf-8 -*-

__author__ = 'my'

"""
LASum_downloader.py
Created on Fri Sep 22 14:38:54 2015

@author: G
"""

import sys
import urllib
import pandas as pd
import argparse
import json


# url = "https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/6884/1871689.xls"
# output_path = ""
# sheet = "LA Summaries ID 2010"
# required_indicators = ["2011", "2012", "2013", "2014"]


def download(url, sheet, reqFields, outPath):
    col = reqFields
    dName = outPath

    try:
        socket = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        sys.exit('excel download HTTPError = ' + str(e.code))
    except urllib.error.URLError as e:
        sys.exit('excel download URLError = ' + str(e.args))
    except Exception:
        print('excel file download error')
        import traceback
        sys.exit('generic exception: ' + traceback.format_exc())

    #operate this excel file
    xd = pd.ExcelFile(socket)
    df = xd.parse(sheet)

    print('data reading------')
    raw_data = df.loc[:, col]

    #save csv file
    print('writing to file ' + dName)
    dfw = pd.DataFrame(raw_data, columns=col)
    dfw.to_csv(dName, index=False)
    print('Requested data has been extracted and saved as ' + dName)
    print("finished")

parser = argparse.ArgumentParser(description='Extract online Index of Deprivation Excel file LA Summaries ID 2010 to .csv file.')
parser.add_argument("--generateConfig", "-g", help="generate a config file called config_LASum.json", action="store_true")
parser.add_argument("--configFile", "-c", help="path for config file")
args = parser.parse_args()

if args.generateConfig:
    obj = {"url": "https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/6884/1871689.xls",
           "outPath": "tempLASum.csv",
           "sheet": "LA Summaries ID 2010",
           "reqFields": ['LA CODE', 'LA NAME', 'Rank of Local Concentration']
           }

    with open("config_LASum.json", "w") as outfile:
        json.dump(obj, outfile, indent=4)
        sys.exit("config file generated")

if args.configFile == None:
    args.configFile = "config_LASum.json"

with open(args.configFile) as json_file:
    oConfig = json.load(json_file)
    print("read config file")

download(oConfig["url"], oConfig["sheet"], oConfig["reqFields"], oConfig["outPath"])
