from flask import jsonify
from api.logic.modelPredictions import getRecommendationForUser


def recommendationForUser(user):
    recomendationlist = getRecommendationForUser(user)
    items, weights = resultTuplesToLists(recomendationlist[:20])
    json = buildJson(user, items, weights)
    return json

def resultTuplesToLists(recomendation):
    items = []
    weights = []
    for x in recomendation:
        items.append(x[0])
        weights.append(x[1])
    return items, weights

def buildJson(user, items, weights):
    jsonData = {}
    jsonData['user'] = user
    jsonData['items'] = items
    jsonData['weights'] = weights
    return jsonify(jsonData)
