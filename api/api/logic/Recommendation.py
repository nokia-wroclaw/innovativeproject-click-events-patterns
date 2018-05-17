from collections import defaultdict
import pandas as pd
from surprise import dump
import glob
import os

from api.logic.PrepareData import getTestsetFromCsv


def loadDump():
    file_name = getLatestDumpPath()
    return dump.load(file_name)


def getLatestDumpPath():
    list_of_files = glob.glob(os.path.join("api","dump","*"))
    return max(list_of_files, key=os.path.getctime)

def getRecommendationForUser(CSVfile, user):
    algo = loadDump()[1]
    data = pd.read_csv(CSVfile, sep=',')
    data = data[data.actionCategory == "WebNei clicked"].actionName.unique()
    l = list(map(lambda x: algo.predict(user, x), data))
    l = [(x.iid, x.est) for x in l]
    k = sorted(l, key=lambda tup: tup[1], reverse=True)
    p = algo.predict(user, "Introduction to Virtualization and Telco Cloud ")
    print(k)

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