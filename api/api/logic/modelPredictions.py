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
    tmp = prepareData(data)
    userid =  numpy.where(tmp.index.values == user)[0][0]
    predictions = calclatePredicionsForUser(model, userid, userTestItems)
    results = prepareResults(predictions, userTestItems, data)
    print(data.tail(1))
    return results

def prepareDataForUser(user, data):
    data = data[data.actionCategory == "WebNei clicked"]
    topNames = data.groupby("actionName").size().sort_values(ascending=False)[0:50].keys()
    data = data[data.actionName.isin(topNames)]
    userItems = data[data.userName == user].actionName.unique()
    items = data[-data.actionName.isin(userItems)].actionName.unique()
    return numpy.squeeze(numpy.asarray(list(map(lambda x: numpy.where(topNames == x), items))))


def calclatePredicionsForUser(model, user_id, userTestItems_ids = numpy.arange(50)):
    return model.predict(numpy.repeat(user_id, userTestItems_ids.size), userTestItems_ids)

def get_top_n(predictions, n=10):
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

def prepareResults(predictions, userTestItems, df):
    df = df[df.actionCategory == "WebNei clicked"]
    topNames = df.groupby("actionName").size().sort_values(ascending=False)[0:50].keys()
    results = [(topNames[userTestItems[x]], predictions[x]) for x in range(userTestItems.size)]
    results.sort(key=lambda tup: tup[1], reverse = True)
    return results