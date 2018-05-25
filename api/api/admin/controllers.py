import os
from flask import Blueprint, make_response, request
import datetime
import uuid


import api
from api.filehandling.FileManager import handelCSVfile, saveCsvFile, getLatestCsvFile, isCsvFilesDirEmpty
from api.logic.csvManipulation import createUnificatePresentationNameColmun

admin = Blueprint('admin', __name__)


@admin.route('/uploadCsv', methods=['POST'])
def uploadCsv():
    f = request.files['data_file']
    if not f:
        return "No file"
    saveCsvFile(f)
    return "csv file uploaded"


@admin.route('/computeModelFromCsv', methods=['POST'])
def computeModelFromCsv():
    f = request.files['data_file']
    if not f:
        return "No csv file available"
    f = saveCsvFile(f)
    handelCSVfile(f)
    return "Sucesfully computed recommender model"


@admin.route('/computeModelFromExistingCsv', methods=['POST'])
def computeModelFromExistingCsv():
    if not isCsvFilesDirEmpty():
        return "No csv file available"
    f = getLatestCsvFile()
    handelCSVfile(f)
    return "Sucesfully computed recommender model"