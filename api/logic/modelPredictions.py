from collections import defaultdict
import numpy
import pandas as pd


from api.filehandling.FileManager import getLatestCsvFile, loadModel
from api.logic.recommenderSystem import loadDump, prepareData


def getUserIdFromMatrixModel(userName, data):
    tmpdata = prepareData(data)
    users = tmpdata.index.values
    return numpy.where(users == userName)[0][0]

def getRecommendationForUser(user):
    model = loadModel()
    data = pd.read_csv(getLatestCsvFile(), sep=',')
    userTestItems = prepareDataForUser(user, data)
    userNames = data[data.actionCategory == "WebNei clicked"].userName.unique()
    userid =  numpy.where(userNames == user)[0][0]
    predictions = calclatePredicionsForUser(model, userid, userTestItems)
    results = prepareResults(predictions, userTestItems, data)
    return results

def prepareDataForUser(user, data):
    data = data[data.actionCategory == "WebNei clicked"]
    itemNames = data.actionName.unique()
    userItems = data[data.userName == user].actionName.unique()
    items = data[-data.actionName.isin(userItems)].actionName.unique()
    return numpy.squeeze(numpy.asarray(list(map(lambda x: numpy.where(itemNames == x), items))))


def calclatePredicionsForUser(model, user_id, userTestItems_ids = numpy.arange(50)):
    return model.predict(numpy.repeat(user_id, userTestItems_ids.size), userTestItems_ids)

def prepareResults(predictions, userTestItems, df):
    df = df[df.actionCategory == "WebNei clicked"]
    topNames = df.groupby("actionName").size().keys()
    results = [(topNames[userTestItems[x]], predictions[x]) for x in range(userTestItems.size)]
    results.sort(key=lambda tup: tup[1], reverse = True)
    return results