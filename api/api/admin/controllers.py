import os
from flask import Blueprint, make_response, request
import datetime
import uuid


import api
from api.logic import PrepareData

admin = Blueprint('admin', __name__)


@admin.route('/uploadData', methods=['POST'])
def uploadData():
    f = request.files['data_file']
    print(type(f))
    if not f:
        return "No file"
    pathToDump = createDumpFileName()
    PrepareData.prepareColumns(f, pathToDump);
    return "file uploded"

def createDumpFileName():
    now = datetime.datetime.now()
    return os.path.join("api","dump","dump" + now.strftime("%y-%m-%d") + "_"+ uuid.uuid4().hex)
