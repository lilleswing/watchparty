import hashlib

from sqlalchemy.orm.exc import NoResultFound
from flask import render_template, redirect, url_for

from models import Group


___author__ = 'leswing'


class GroupsController():

    def __init__(self, db):
        self.db = db

    def get(self, warning=None):
        return render_template("groupcreate.html", warning=warning)

    def create(self, params):
        group_name = params['group_name']
        try:
            self.db.session.query(Group).filter(Group.name == group_name).one()
            return self.get(warning="Group name already exists")
        except NoResultFound, e:
            group = Group()
            group.name = group_name
            sha1 = hashlib.sha1()
            sha1.update(group.name)
            group.hash_name = sha1.hexdigest()[0:10]
            self.db.session.add(group)
            self.db.session.commit()
            return redirect(url_for('scoreboard', hash_name=group.hash_name))
