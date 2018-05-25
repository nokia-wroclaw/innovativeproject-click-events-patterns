import glob
import os
import shutil

from flask import Blueprint, make_response, request
import datetime
import uuid
import os
import pandas as pd

from api.logic.recommenderSystem import createRecommenderModel, saveDump, loadDump

csvfilesPath = os.path.join("api", "csvfiles")

def isCsvFilesDirEmpty():
    return len(os.listdir(csvfilesPath)) > 0

def handelCSVfile(CSVfile):
    data = pd.read_csv(CSVfile, sep=',')
    algo = createRecommenderModel(data)
    saveModel(algo)


def createDumpPath():
    now = datetime.datetime.now()
    return os.path.join("api", "dump", "dump" + now.strftime("%y-%m-%d") + "_" + uuid.uuid4().hex)

def createCsvPath():
    now = datetime.datetime.now()
    return os.path.join("api", "csvfiles", "csv" + now.strftime("%y-%m-%d") + "_" + uuid.uuid4().hex + ".csv")

def saveCsvFile(csv):
    pathName = createCsvPath()
    print(pathName)
    csv.save(pathName)
    return getLatestCsvFile()

def saveModel(algo):
    pathDump = createDumpPath()
    saveDump(algo, pathDump)

def getLatestCsvFile():
    list_of_files = glob.glob(os.path.join("api", "csvfiles", "*"))
    return max(list_of_files, key=os.path.getctime)

def loadModel():
    fileName = getLatestDumpPath()
    return loadDump(fileName)[1]

def getLatestDumpPath():
    list_of_files = glob.glob(os.path.join("api","dump","*"))
    return max(list_of_files, key=os.path.getctime)