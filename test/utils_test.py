import pytest
from utils import LoadJSON
from run import app

DATA_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"
BOOKMARKS_PATH = "data/bookmarks.json"

load_json_data = LoadJSON(DATA_PATH)
load_json_comments = LoadJSON(COMMENTS_PATH)

key_data = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]
key_comments = ["post_id", "commenter_name", "comment", "pk"]
poster_name = ["leo", "johnny", "hank", "larry"]
posts_id = [1, 2, 3, 4, 5, 6, 7]
posts_pk = [1, 2, 3, 4, 5, 6, 7, 8]
search_words = ["утро", "свалка", "днем"]


def test_load_data():
    assert type(load_json_data.load_data()) == list


def test_load_comments():
    assert type(load_json_comments.load_data()) == list


def test_get_post():
    for i in load_json_data.get_posts():
        for t in key_data:
            assert t in i


def test_get_posts_by_user():
    for name in poster_name:
        for post in load_json_data.get_posts_by_user(name):
            assert name in post['poster_name']


def test_get_comments_by_post_id():
    for post_id in posts_id:
        for post in load_json_comments.get_comments_by_post_id(post_id):
            assert post_id == post['post_id']


def test_search_for_posts():
    for word in search_words:
        for post in load_json_data.search_for_posts(word):
            assert word in post['content'].lower()


def test_get_post_by_pk():
    for post_pk in posts_pk:
        assert post_pk == load_json_data.get_post_by_pk(post_pk)['pk']


def test_type_json():
    response = app.test_client().get('/api/posts', follow_redirects=True)
    assert type(response.json) == list


def test_key_json():
    response = app.test_client().get('/api/posts', follow_redirects=True)
    for item in response.json:
        for key in key_data:
            assert key in item


def test_type_json_pk():
    response = app.test_client().get('/api/post/7', follow_redirects=True)
    assert type(response.json) == dict


def test_key_json_pk():
    response = app.test_client().get('/api/post/7', follow_redirects=True)
    for item in response.json.keys():
        assert item in key_data