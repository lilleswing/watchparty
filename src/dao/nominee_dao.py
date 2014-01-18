from models import Nominee

__author__ = 'karl'


class NomineeDao():
    def __init__(self, db):
        self.db = db

    def list(self, category_id):
        return self.db.session.query(Nominee).filter(Nominee.category_id == category_id).all()
