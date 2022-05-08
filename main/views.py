from flask import Flask, render_template, request, Blueprint
import logging
from config import *
from utils import LoadJSON
from json import JSONDecodeError

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')

logger = logging.getLogger("basic")
logger.setLevel("DEBUG")

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

file_handler = logging.FileHandler("../logger.log", encoding="utf-8")
logger.addHandler(file_handler)


formatter = logging.Formatter("%(levelname)s %(asctime)s : %(message)s  %(pathname)s >> %(funcName)s")
stream_handler.setFormatter(formatter)


@main_blueprint.route('/')
def main_page():
    logger.info("Открытие главной страницы")
    try:
        return render_template('index.html', data=LoadJSON(DATA_PATH).get_posts())
    except FileNotFoundError:
        logger.info("Не удалось найти файл, проверьте правильно ли указан путь.")
        return "Не удалось найти файл, проверьте правильно ли указан путь."
    except JSONDecodeError:
        logger.info("Не удалось открыть файл JSON")
        return "Не удалось открыть файл JSON"


@main_blueprint.route('/search/')
def search_page():
    try:
        s = request.args.get("s", "").lower()
        data = LoadJSON(DATA_PATH).search_for_posts(s)
        logger.info(f'Выполнен поиск по запросу: {s}')
    except FileNotFoundError:
        logger.info("Не удалось найти файл, проверьте правильно ли указан путь.")
        return "Не удалось найти файл, проверьте правильно ли указан путь."
    except JSONDecodeError:
        logger.info("Не удалось открыть файл JSON")
        return "Не удалось открыть файл JSON"
    else:
        return render_template('search.html', data=data)


@main_blueprint.route('/post/<int:pk>')
def post_page(pk):
    try:
        logger.info(f'Открыт пост с id: {pk}')
        return render_template('post.html', data=LoadJSON(DATA_PATH).get_post_by_pk(pk),
                               data_comments=LoadJSON(COMMENTS_PATH).get_comments_by_post_id(pk))
    except FileNotFoundError:
        logger.info("Не удалось найти файл, проверьте правильно ли указан путь.")
        return "Не удалось найти файл, проверьте правильно ли указан путь."
    except JSONDecodeError:
        logger.info("Не удалось открыть файл JSON")
        return "Не удалось открыть файл JSON"


@main_blueprint.route('/users/<username>')
def user_page(username):
    try:
        return render_template('user-feed.html', data=LoadJSON(DATA_PATH).get_posts_by_user(username))
    except FileNotFoundError:
        logger.info("Не удалось найти файл, проверьте правильно ли указан путь.")
        return "Не удалось найти файл, проверьте правильно ли указан путь."
    except JSONDecodeError:
        logger.info("Не удалось открыть файл JSON")
        return "Не удалось открыть файл JSON"