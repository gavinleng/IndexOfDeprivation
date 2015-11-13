__author__ = 'G'

import sys
sys.path.append('../harvesterlib')

import pandas as pd
import argparse
import json

import now
import openurl
import datasave as dsave


# url = "https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/6884/1871689.xls"
# output_path = "tempLASum.csv"
# sheet = "LA Summaries ID 2010"
# required_indicators = ['LA CODE', 'LA NAME', 'Rank of Local Concentration']


def download(url, sheet, reqFields, outPath, keyCol, digitCheckCol, noDigitRemoveFields):
    col = reqFields
    dName = outPath

    # open url
    socket = openurl.openurl(url, logfile, errfile)

    # operate this excel file
    logfile.write(str(now.now()) + ' excel file loading\n')
    print('excel file loading------')
    xd = pd.ExcelFile(socket)
    df = xd.parse(sheet)
    
    # data reading
    logfile.write(str(now.now()) + ' data reading\n')
    print('data reading------')
    raw_data = df.loc[:, col]

    # save csv file
    dsave.save(raw_data, col, keyCol, digitCheckCol, noDigitRemoveFields, dName, logfile)


parser = argparse.ArgumentParser(description='Extract online Index of Deprivation Excel file LA Summaries ID 2010 to .csv file.')
parser.add_argument("--generateConfig", "-g", help="generate a config file called config_LASum.json", action="store_true")
parser.add_argument("--configFile", "-c", help="path for config file")
args = parser.parse_args()

if args.generateConfig:
    obj = {"url": "https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/6884/1871689.xls",
           "outPath": "tempLASum.csv",
           "sheet": "LA Summaries ID 2010",
           "reqFields": ['LA CODE', 'LA NAME', 'Rank of Local Concentration'],
           "primaryKeyCol": ['LA CODE'],#[0],
           "digitCheckCol": ['Rank of Local Concentration'],#[2],
           "noDigitRemoveFields": []
           }

    logfile = open("log_tempLASum.log", "w")
    logfile.write(str(now.now()) + ' start\n')

    errfile = open("err_tempLASum.err", "w")

    with open("config_tempLASum.json", "w") as outfile:
        json.dump(obj, outfile, indent=4)
        logfile.write(str(now.now()) + ' config file generated and end\n')
        sys.exit("config file generated")

if args.configFile == None:
    args.configFile = "config_tempLASum.json"

with open(args.configFile) as json_file:
    oConfig = json.load(json_file)

    logfile = open('log_' + oConfig["outPath"].split('.')[0] + '.log', "w")
    logfile.write(str(now.now()) + ' start\n')

    errfile = open('err_' + oConfig["outPath"].split('.')[0] + '.err', "w")

    logfile.write(str(now.now()) + ' read config file\n')
    print("read config file")

download(oConfig["url"], oConfig["sheet"], oConfig["reqFields"], oConfig["outPath"], oConfig["primaryKeyCol"], oConfig["digitCheckCol"], oConfig["noDigitRemoveFields"])
