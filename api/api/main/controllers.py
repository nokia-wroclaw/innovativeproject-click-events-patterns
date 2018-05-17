from flask import Blueprint, request
import api
from api.logic.Recommendation import loadDump, getRecommendationForUser

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return api.app.instance_path.casefold();

@main.route('/recommendation/<user>', methods=['POST'])
def dump(user):
    f = request.files['data_file']
    if not f:
        return "No file"
    getRecommendationForUser(f, user)
    return user;