from dao.pick_dao import PickDao
from dao.selection_dao import SelectionDao

__author__ = 'leswing'


class SelectionsController():

    def __init__(self, db):
        self.db = db
        self.selection_dao = SelectionDao(db)
        self.pick_dao = PickDao(db)

    def get_pick(self, selection_id):
        return self.pick_dao.get_by_selection(selection_id)

    def post(self, selection):
        return self.selection_dao.create(selection)
