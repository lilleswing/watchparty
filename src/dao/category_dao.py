from models import Category

__author__ = 'karl'


class CategoryDao():
    def __init__(self, db):
        self.db = db

    def list(self, event_id):
        return self.db.session.query(Category).filter(Category.event_id == event_id).all()

