from models import Pick

__author__ = 'leswing'


class PickDao():
    def __init__(self, db):
        self.db = db

    def get_by_selection(self, selection_id):
        return self.db.session.query(Pick).filter(Pick.selection_id == selection_id).all()
