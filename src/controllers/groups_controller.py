__author__ = 'karl'

from flask import render_template
from src.models import Selection, Group


class GroupsController():

    def __init__(self, db):
        self.db = db

    def get(self):
        return "lol"

    def get_id(self, group_name):
        group = self.db.session.query(Group).filter(Group.name == group_name).all()[0]
        selections = self.db.session.query(Selection).filter(Selection.group_id == group.id).order_by(
            Selection.points).all()[::-1]
        return render_template('scoreboard.html', selections=selections)
