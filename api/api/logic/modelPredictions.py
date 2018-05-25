from collections import defaultdict
import pandas as pd
from surprise import dump, Reader, Dataset
import glob
import os

from api.filehandling.FileManager import getLatestCsvFile, loadModel
from api.logic.recommenderSystem import loadDump


def getRecommendationForUser(user):
    algo = loadModel()
    data = pd.read_csv(getLatestCsvFile(), sep=',')
    userTestItems = prepareDataForUser(user, data)
    predictions = calclatePredicionsForUser(algo, user, userTestItems)
    return predictions;

def prepareDataForUser(user, data):
    data = data[data.actionCategory == "WebNei clicked"]
    userItems = data[data.userName == user].actionName.unique()
    return data[-data.actionName.isin(userItems)].actionName.unique()

def calclatePredicionsForUser(algo, user, userTestItems):
    l = list(map(lambda x: algo.predict(user, x), userTestItems))
    l = [(x.iid, x.est) for x in l]
    k = sorted(l, key=lambda tup: tup[1], reverse=True)
    return k;

def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n