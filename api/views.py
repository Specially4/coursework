from flask import jsonify, Blueprint
from config_path import *
from utils import LoadJSON

api_blueprint = Blueprint('api_blueprint', __name__, template_folder='templates')



@api_blueprint.route('/api/posts')
def api_post():
    """Данная функция возвращает страничку с JSON постов"""
    return jsonify(LoadJSON(DATA_PATH).get_posts())


@api_blueprint.route('/api/post/<int:pk>')
def api_post_pk(pk):
    """Данная функция возвращает страничку с JSON одного поста"""
    return jsonify(LoadJSON(DATA_PATH).get_post_by_pk(pk))