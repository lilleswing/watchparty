from dao.category_dao import CategoryDao
from dao.nominee_dao import NomineeDao

__author__ = 'karl'


class CategoriesController():

    def __init__(self, db):
        self.category_dao = CategoryDao(db)
        self.nominee_dao = NomineeDao(db)
        self.db = db

    def get_id(self, category_id):
        return self.category_dao.get(category_id)

    def get_nominee(self, category_id):
        return self.nominee_dao.get_by_category(category_id)

