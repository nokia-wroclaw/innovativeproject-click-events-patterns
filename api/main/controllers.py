from flask import Blueprint

from api.userhandling.UserManager import recommendationForUser

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Api Recommender System'


@main.route('/recommendation/<user>', methods=['GET'])
def recommendation(user):
    return recommendationForUser(user)

