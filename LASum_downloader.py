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
import datetime


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
        errfile.write(str(now()) + ' excel download HTTPError is ' + str(e.code) + ' . End progress\n')
        logfile.write(str(now()) + ' error and end progress\n')
        sys.exit('excel download HTTPError = ' + str(e.code))
    except urllib.error.URLError as e:
        errfile.write(str(now()) + ' excel download URLError is ' + str(e.args) + ' . End progress\n')
        logfile.write(str(now()) + ' error and end progress\n')
        sys.exit('excel download URLError = ' + str(e.args))
    except Exception:
        print('excel file download error')
        import traceback
        errfile.write(str(now()) + ' generic exception: ' + str(traceback.format_exc()) + ' . End progress\n')
        logfile.write(str(now()) + ' error and end progress\n')
        sys.exit('generic exception: ' + traceback.format_exc())

    #operate this excel file
    logfile.write(str(now()) + ' excel file loading\n')
    xd = pd.ExcelFile(socket)
    df = xd.parse(sheet)

    logfile.write(str(now()) + ' data reading\n')
    print('data reading------')
    raw_data = df.loc[:, col]

    #check the no digit data
    check_field = 'Rank of Local Concentration'
    inrow = checkRaw(raw_data, check_field)

    raw_data_w = raw_data.drop(raw_data.index[inrow])

    #save csv file
    print('writing to file ' + dName)
    dfw = pd.DataFrame(raw_data_w, columns=col)
    dfw.to_csv(dName, index=False)
    logfile.write(str(now()) + ' has been extracted and saved as ' + str(dName) + '\n')
    print('Requested data has been extracted and saved as ' + dName)
    logfile.write(str(now()) + ' finished\n')
    print("finished")

def checkRaw(data, field):
    inrow = []
    for i in range(len(data)):
        if str(data.loc[i, field]).isdigit() != True:
            inrow.append(i)
            print('------------------------------------')
            print('the value is not a digit number at:')
            print(data.loc[i, :])

    return inrow

def now():
    return datetime.datetime.now()


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

    logfile = open("log_tempLASum.log", "w")
    logfile.write(str(now()) + ' start\n')

    errfile = open("err_tempLASum.err", "w")

    with open("config_tempLASum.json", "w") as outfile:
        json.dump(obj, outfile, indent=4)
        logfile.write(str(now()) + ' config file generated and end\n')
        sys.exit("config file generated")

if args.configFile == None:
    args.configFile = "config_tempLASum.json"

with open(args.configFile) as json_file:
    oConfig = json.load(json_file)

    logfile = open('log_' + oConfig["outPath"].split('.')[0] + '.log', "w")
    logfile.write(str(now()) + ' start\n')

    errfile = open('err_' + oConfig["outPath"].split('.')[0] + '.err', "w")

    logfile.write(str(now()) + ' read config file\n')
    print("read config file")

download(oConfig["url"], oConfig["sheet"], oConfig["reqFields"], oConfig["outPath"])
