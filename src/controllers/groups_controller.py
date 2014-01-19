
__author__ = 'karl'

from dao.group_dao import GroupDao
from dao.selection_dao import SelectionDao


class GroupsController():

    def __init__(self, db):
        self.db = db
        self.group_dao = GroupDao(db)
        self.selection_dao = SelectionDao(db)

    def get_name(self, group_name):
        return self.group_dao.get_by_name(group_name)

    def get_selection(self, group_id):
        return self.selection_dao.get_by_group(group_id)
