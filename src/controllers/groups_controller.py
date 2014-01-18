from dao.selection_dao import SelectionDao

__author__ = 'karl'

from flask import render_template
from dao.group_dao import GroupDao
from dao.selection_dao import SelectionDao


class GroupsController():

    def __init__(self, db):
        self.db = db
        self.group_dao = GroupDao(db)
        self.selection_dao = SelectionDao(db)

    def get(self):
        return "lol"

    def get_id(self, group_name):
        group = self.group_dao.get_by_name(group_name)
        selections = self.selection_dao.list(group.id)
        print(self.selection_dao)
        return render_template('scoreboard.html', selections=selections)
