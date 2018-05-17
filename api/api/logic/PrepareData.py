import os
import pandas as pd
from surprise import NormalPredictor, dump
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
from surprise import SVD
from werkzeug.utils import secure_filename

import api


def prepareColumns(CSVfile, pathDump):
    # CSVfile.save(secure_filename(CSVfile.filename))
    data = pd.read_csv(CSVfile,sep=',')
    data = data[data.actionCategory == "WebNei clicked"]
    topNames = data.groupby("actionName").size().sort_values(ascending=False)[0:20].keys()
    data = data[data.actionName.isin(topNames)]
    actionByUsers = data.groupby(["userName", "actionName"]).size()
    actionByUsers = actionByUsers.apply(lambda x: 1)
    actionByUsers = actionByUsers.unstack()
    actionByUsers = actionByUsers.fillna(0.0)
    actionByUsers = actionByUsers.stack()
    users = list(actionByUsers.index.get_level_values(0))
    items = list(actionByUsers.index.get_level_values(1))
    ratings = list(actionByUsers.values)
    # Creation of the dataframe. Column names are irrelevant.
    ratings_dict = {'itemID': items,
                    'userID': users,
                    'rating': ratings}
    df = pd.DataFrame(ratings_dict)

    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(0, 1))

    # The columns must correspond to user id, item id and ratings (in that order).
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

    algo = SVD()

    # We can now use this dataset as we please, e.g. calling cross_validate
    # cross_validate(SVD(), data, cv=4)
    trainset = data.build_full_trainset()
    trained = algo.fit(trainset)
    dump.dump(pathDump, algo=algo)
    return trained

def getTestsetFromCsv(csvFile):
    data = pd.read_csv(csvFile, sep=',')
    data = data[data.actionCategory == "WebNei clicked"]
    topNames = data.groupby("actionName").size().sort_values(ascending=False)[0:20].keys()
    data = data[data.actionName.isin(topNames)]
    actionByUsers = data.groupby(["userName", "actionName"]).size()
    actionByUsers = actionByUsers.apply(lambda x: 1)
    actionByUsers = actionByUsers.unstack()
    actionByUsers = actionByUsers.fillna(0.0)
    actionByUsers = actionByUsers.stack()
    users = list(actionByUsers.index.get_level_values(0))
    items = list(actionByUsers.index.get_level_values(1))
    ratings = list(actionByUsers.values)
    # Creation of the dataframe. Column names are irrelevant.
    ratings_dict = {'itemID': items,
                    'userID': users,
                    'rating': ratings}
    df = pd.DataFrame(ratings_dict)

    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(0, 1))

    # The columns must correspond to user id, item id and ratings (in that order).
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
    trainset = data.build_full_trainset()
    testset = trainset.build_anti_testset()
    return testset
