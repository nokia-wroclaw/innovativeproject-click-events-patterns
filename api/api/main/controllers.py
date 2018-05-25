from flask import Blueprint, request, jsonify
import api

from api.logic.modelPredictions import loadDump, getRecommendationForUser

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return api.app.instance_path.casefold();


@main.route('/recommendation/<user>', methods=['GET'])
def dump(user):
    recomendationlist = getRecommendationForUser(user)
    return jsonify(recomendationlist)