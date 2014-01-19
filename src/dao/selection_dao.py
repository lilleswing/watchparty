from models import Selection

__author__ = 'karl'


class SelectionDao():
    def __init__(self, db):
        self.db = db

    def get(self, selection_id):
        return self.db.session.query(Selection).filter(Selection.id == selection_id).first()

    def get_by_group(self, group_id):
        return self.db.session.query(Selection).filter(Selection.group_id == group_id)\
                   .order_by(Selection.points).all()[::-1]

    def get_ids(self, ids):
        return self.db.session.query(Selection).filter(Selection.id in ids).all()

    def create(self, selection):
        self.db.session.add(selection)
        self.db.session.commit()
        return selection
