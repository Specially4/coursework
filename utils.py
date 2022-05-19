import json
from config_path import *


class LoadJSON:

    def __init__(self, path):
        self.path = path

    def load_data(self):
        """Данная функция загружает список с постами из JSON"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data
        except:
            raise

    def load_to_json(self, data):
        """Данная функция загружает список с постами в JSON"""
        with open(self.path, 'w', encoding='utf-8') as file:
            return json.dump(data, file, indent=2, ensure_ascii=False)


    def occurrence_check_pk(self, data):
        """Данная функция проверяет посты по вхождению 'pk' в списке постов"""
        all_posts = self.load_data()
        bookmarks_pk = []
        for item in all_posts:
            bookmarks_pk.append(item['pk'])
        if data['pk'] not in bookmarks_pk:
            all_posts.append(data)
            self.load_to_json(all_posts)

    def delete_post(self, pk):
        """Данная функция удаляет пост из списка постов"""
        posts_list = []
        for post in self.load_data():
            if pk != post['pk']:
                posts_list.append(post)
        self.load_to_json(posts_list)

    def get_posts(self):
        """Данная функция возвращает список постов так же укарачивает описание поста"""
        data = self.load_data()
        for item in data:
            short_content = (' '.join(item['content'].split('.')[:1]) + '...')
            item['content'] = short_content
        return data

    def get_posts_by_user(self, user_name):
        """Данная функция возвращает пост из списка постов по 'user_name'"""
        posts_by_user = []
        for item in self.load_data():
            if user_name in item['poster_name']:
                short_content = (' '.join(item['content'].split('.')[:1]) + '...')
                item['content'] = short_content
                posts_by_user.append(item)
        return posts_by_user

    def get_comments_by_post_id(self, post_id):
        """Данная функция возвращает список комментариев к определенному посту"""
        comments_by_post_id = []
        for item in self.load_data():
            if post_id == item['post_id']:
                comments_by_post_id.append(item)
        return comments_by_post_id

    def search_for_posts(self, query):
        """Данная функция возвращает пост(ы) из списка постов по запросу поиска"""
        posts_list = []
        for item in self.load_data():
            if query in item['content'].lower():
                posts_list.append(item)
        return posts_list

    def get_post_by_pk(self, pk):
        """Данная функция возвращает пост из списка постов по 'pk'"""
        for item in self.load_data():
            if pk == item['pk']:
                return item


