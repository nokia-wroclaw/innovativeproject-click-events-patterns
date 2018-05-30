from lightfm import LightFM, cross_validation
from scipy.sparse import coo_matrix
from sklearn.externals import joblib
from lightfm.evaluation import auc_score

import pandas as pd

def createRecommenderModel(data):
    preparedData = prepareData(data)
    matrix = createMatrix(preparedData)
    model = createModel()
    model = trainModel(model, matrix)
    return model

def createModel(components = 30, item_alpha = 1e-6):
    # Let's fit a WARP model: these generally have the best performance.
    model = LightFM(loss='warp',
                    item_alpha=item_alpha,
                    no_components=components)
    return model

def prepareData(df, max_items = 50):
    df = df[df.actionCategory == "WebNei clicked"]
    topNames = df.groupby("actionName").size().sort_values(ascending=False)[0:max_items].keys()
    df = df[df.actionName.isin(topNames)]
    actionByUsers = df.groupby(["userName", "actionName"]).size()
    actionByUsers = actionByUsers.apply(lambda x: 1)
    actionByUsers = actionByUsers.unstack()
    actionByUsers = actionByUsers.fillna(0.0)
    return actionByUsers


def createMatrix(data):
    return coo_matrix(data.values)


def trainModel(model, train, epochs = 20, threads = 2):
    model = model.fit(train, epochs=epochs, num_threads=threads)
    return model;

def computeAUCscore(model, matrix):
    train, test = cross_validation.random_train_test_split(matrix)
    test_auc = auc_score(model,
                                 test,
                                 train_interactions=train,
                                 num_threads=2).mean()
    print('AUC: %s' % test_auc)
    return test_auc

def saveDump(model, pathDump):
    joblib.dump(model, pathDump)

def loadDump(pathDump):
    return joblib.load(pathDump)

