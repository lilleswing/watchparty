__author__ = 'karl'

from models import Group


class GroupDao():
    def __init__(self, db):
        self.db = db

    def get_by_name(self, group_name):
        return self.db.session.query(Group).filter(Group.name == group_name).first()
