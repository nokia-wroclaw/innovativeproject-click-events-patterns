from lightfm import LightFM, cross_validation
from lightfm.data import Dataset
from scipy.sparse import coo_matrix
from sklearn.externals import joblib
from lightfm.evaluation import auc_score

import pandas as pd


def createRecommenderModel(data, tags):
    interactions, item_features,user_features = prepareData(data, tags)
    model = createModel()
    model = trainModel(model, interactions, item_features, user_features)
    return model


def createModel(components=30, item_alpha=1e-6):
    # Let's fit a WARP model: these generally have the best performance.
    model = LightFM(loss='warp',
                    item_alpha=item_alpha,
                    no_components=components)
    return model


def prepareData(df, tags):
    df = df[df.actionCategory == "WebNei clicked"]
    actionByUsers = df.groupby(["userName", "actionName"]).size()
    uniqueUsers = df[df.userName.isin(actionByUsers.index.get_level_values(0).unique().values)].drop_duplicates(
        'userName')
    uniqueUsers['user_features'] = uniqueUsers[['title', 'team', 'organization', 'department']].values.tolist()
    dataset = Dataset()
    dataset.fit((list(actionByUsers.index.get_level_values(0))),
                (list(actionByUsers.index.get_level_values(1))))

    rowM, colM = prepareJson(tags)
    rowU, colU = prepareUserFeatures(uniqueUsers)

    dataset.fit_partial(items=rowM,
                        item_features=colM,
                        users=rowU,
                        user_features=colU)

    (interactions, weights) = dataset.build_interactions(
        zip(list(actionByUsers.index.get_level_values(0)), list(actionByUsers.index.get_level_values(1))))
    item_features = dataset.build_item_features(zip(rowM, [colM]))
    user_features = dataset.build_user_features(zip(rowU, [colU]))
    return interactions, item_features, user_features

def prepareUserFeatures(users):
    rowU = []
    colU = []
    for index, row in users.iterrows():
        for rowA in row[12]:
            colU.append(row[5])
            rowU.append(rowA)
    return rowU, colU



def prepareJson(json):
    print(json)
    tags = pd.read_json(path_or_buf=json, orient='records', dtype={"A": str, "B": list})
    rowM = []
    colM = []
    for index, row in tags.iterrows():
        for rowA in row[1]:
            if (row[0] == ""):
                rowM.append(row[0])
            else:
                rowM.append(row[2])
            colM.append(rowA)
    return rowM, colM


def createMatrix(data):
    return coo_matrix(data.values)


def trainModel(model, train, item_features, user_features, epochs=20, threads=2):
    model = model.fit(train,epochs=epochs, item_features = item_features, user_features=user_features, num_threads=threads)
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
