from flask import Flask, render_template, request, Blueprint, redirect
import logging
from json import JSONDecodeError

from config_path import DATA_PATH, BOOKMARKS_PATH, COMMENTS_PATH
from utils import LoadJSON

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')
logger = logging.getLogger("basic")
logger.setLevel("DEBUG")

stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

file_handler = logging.FileHandler("logger.log", encoding="utf-8")
logger.addHandler(file_handler)


formatter = logging.Formatter("%(levelname)s %(asctime)s : %(message)s  %(pathname)s >> %(funcName)s")
stream_handler.setFormatter(formatter)

@main_blueprint.route('/', methods=["GET"])
def main_page():
    """Данная функция выводит главную страничку"""
    try:
        return render_template('index.html', data=LoadJSON(DATA_PATH).get_posts(), length_bookmark=len(LoadJSON(BOOKMARKS_PATH).get_posts()))
    except FileNotFoundError:
        logger.info("Не удалось найти файл, проверьте правильно ли указан путь.")
        return "Не удалось найти файл, проверьте правильно ли указан путь."
    except JSONDecodeError:
        logger.info("Не удалось открыть файл JSON")
        return "Не удалось открыть файл JSON"
    logger.info("Открытие главной страницы")


@main_blueprint.route('/search/')
def search_page():
    """Данная функция выводит страничку с поиском"""
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
    """Данная функция выводит страничку одного поста"""
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
    """Данная функция выводит страничку с постами определенного пользователя"""
    try:
        return render_template('user-feed.html', data=LoadJSON(DATA_PATH).get_posts_by_user(username))
    except FileNotFoundError:
        logger.info("Не удалось найти файл, проверьте правильно ли указан путь.")
        return "Не удалось найти файл, проверьте правильно ли указан путь."
    except JSONDecodeError:
        logger.info("Не удалось открыть файл JSON")
        return "Не удалось открыть файл JSON"

@main_blueprint.route('/tag/<tag>')
def tag_page(tag):
    """Данная функция выводит страничку с постами по тегу"""
    return render_template('tag.html', data=LoadJSON(DATA_PATH).search_for_posts(tag), tag=tag)