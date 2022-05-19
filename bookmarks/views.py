from flask import Blueprint, redirect, render_template
from config_path import *
from utils import LoadJSON

bookmarks_blueprint = Blueprint('bookmarks_blueprint', __name__, template_folder='templates')


@bookmarks_blueprint.route('/bookmarks/add/<int:pk>')
def add_post(pk):
    data = LoadJSON(DATA_PATH).get_post_by_pk(pk)
    LoadJSON(BOOKMARKS_PATH).occurrence_check_pk(data)
    # logger.info(f"Запись поста {pk} в закладки")
    return redirect("/", code = 302)


@bookmarks_blueprint.route('/bookmarks/')
def bookmarks_page():
    return render_template('bookmarks.html', data=LoadJSON(BOOKMARKS_PATH).get_posts())


@bookmarks_blueprint.route('/bookmark/delete/<int:pk>')
def delete_post(pk):
    LoadJSON(BOOKMARKS_PATH).delete_post(pk)
    # logger.info(f"Удаление поста {pk} из закладок")
    return redirect("/bookmarks/", code = 302)