__author__ = 'karl'
import json
from models import Category, Nominee


class CategoriesController():

    def __init__(self, db):
        self.db = db

    def get(self):
        categories = self.db.session.query(Category).all()
        return json.dumps([x.to_json for x in categories])

    def get(self, category_id):
        category = self.db.session.query(Category).filter(Category.id == category_id).first()
        return category.to_json()
