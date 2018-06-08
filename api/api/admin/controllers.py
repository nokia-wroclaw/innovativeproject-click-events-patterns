from flask import Blueprint, request

import api
from api.filehandling.FileManager import handelCSVfile, saveCsvFile, getLatestCsvFile, isCsvFilesDirEmpty, saveTagsFile, \
    getLatestTagsFile

admin = Blueprint('admin', __name__)

@admin.route('/uploadCsv', methods=['POST'])
def uploadCsv():
    f = request.files['data_file']
    if not f:
        return "No file"
    saveCsvFile(f)
    return "csv file uploaded"

@admin.route('/uploadTags', methods=['POST'])
def uploadJson():
    f = request.files['data_file']
    if not f:
        return "No file"
    saveTagsFile(f)
    return "tags file uploaded"


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

@admin.route('/computeModelFromExistingCsvWithTags', methods=['POST'])
def computeModelFromExistingCsvWithTags():
    if not isCsvFilesDirEmpty():
        return "No csv file available"
    f = getLatestCsvFile()
    g = getLatestTagsFile()
    handelCSVfile(f, g)
    return "Sucesfully computed recommender model"


@admin.route('/computeModelFromCsvWithTags', methods=['POST'])
def computeModelFromCsvWithTags():
    g = request.files['tags_file']
    f = request.files['data_file']
    if (f.filename == '') & (g.filename == ''):
        return "No files available"
    f = saveCsvFile(f)
    g = saveTagsFile(g)
    handelCSVfile(f, g)
    return "Sucesfully computed recommender model"
