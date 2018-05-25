from surprise import NormalPredictor, dump
from surprise import Dataset
from surprise import Reader
from surprise.prediction_algorithms.matrix_factorization import SVD

import pandas as pd

def createRecommenderModel(data):
    preparedData = prepareData(data)
    matrix = createMatrix(preparedData)

    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(0, 1))
    # The columns must correspond to user id, item id and ratings (in that order).
    data = Dataset.load_from_df(matrix[['userID', 'itemID', 'rating']], reader)
    algo = trainModel(data)
    return algo


def prepareData(data):
    data = data[data.actionCategory == "WebNei clicked"]
    topNames = data.groupby("actionName").size().sort_values(ascending=False)[0:20].keys()
    data = data[data.actionName.isin(topNames)]
    actionByUsers = data.groupby(["userName", "actionName"]).size()
    actionByUsers = actionByUsers.apply(lambda x: 1)
    return actionByUsers


def createMatrix(data):
    users = list(data.index.get_level_values(0))
    items = list(data.index.get_level_values(1))
    ratings = list(data.values)
    # Creation of the dataframe. Column names are irrelevant.
    ratings_dict = {'itemID': items,
                    'userID': users,
                    'rating': ratings}
    df = pd.DataFrame(ratings_dict)
    return df


def trainModel(dataset):
    algo = SVD()

    # We can now use this dataset as we please, e.g. calling cross_validate
    # cross_validate(SVD(), data, cv=4)
    trainset = dataset.build_full_trainset()
    trained = algo.fit(trainset)
    return algo;

def saveDump(algo, pathDump):
    dump.dump(pathDump, algo=algo)

def loadDump(file_name):
    return dump.load(file_name)

