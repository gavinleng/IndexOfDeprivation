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
import hashlib

# url = "https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/6884/1871689.xls"
# output_path = "tempLASum.csv"
# sheet = "LA Summaries ID 2010"
# required_indicators = ['LA CODE', 'LA NAME', 'Rank of Local Concentration']


def download(url, sheet, reqFields, outPath):
    col = reqFields
    dName = outPath

    # open url
    socket = openurl(url)

    # operate this excel file
    logfile.write(str(now()) + ' excel file loading\n')
    print('excel file loading------')
    xd = pd.ExcelFile(socket)
    df = xd.parse(sheet)
	
	# data reading
    logfile.write(str(now()) + ' data reading\n')
    print('data reading------')
    raw_data = df.loc[:, col]

    # check the no digit data
    check_field = 'Rank of Local Concentration'
    inrow = checkRaw(raw_data, check_field)

    # drop the no digit data
    raw_data = raw_data.drop(raw_data.index[inrow])
    logfile.write(str(now()) + ' data reading end\n')
    print('data reading end------')

    # create primary key by md5 for each row
    logfile.write(str(now()) + ' create primary key\n')
    print('create primary key------')
    keyCol = [0]
    raw_data['pkey'] = fpkey(raw_data, col, keyCol)
    logfile.write(str(now()) + ' create primary key end\n')
    print('create primary key end------')

    #save csv file
    logfile.write(str(now()) + ' writing to file\n')
    print('writing to file ' + dName)
    dfw = pd.DataFrame(raw_data, columns=col + ['pkey'])
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

def openurl(url):
    try:
        socket = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        errfile.write(str(now()) + ' file download HTTPError is ' + str(e.code) + ' . End progress\n')
        logfile.write(str(now()) + ' error and end progress\n')
        sys.exit('file download HTTPError = ' + str(e.code))
    except urllib.error.URLError as e:
        errfile.write(str(now()) + ' file download URLError is ' + str(e.args) + ' . End progress\n')
        logfile.write(str(now()) + ' error and end progress\n')
        sys.exit('file download URLError = ' + str(e.args))
    except Exception:
        print('file download error')
        import traceback
        errfile.write(str(now()) + ' generic exception: ' + str(traceback.format_exc()) + ' . End progress\n')
        logfile.write(str(now()) + ' error and end progress\n')
        sys.exit('generic exception: ' + traceback.format_exc())

    return socket

def fpkey(data, col, keyCol):
    mystring = ''
    pkey = []
    for i in range(len(data[col[0]])):
        for j in keyCol:
            mystring += str(data[col[j]][i])
        mymd5 = hashlib.md5(mystring.encode()).hexdigest()
        pkey.append(mymd5)

    return pkey

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
