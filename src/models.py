import json

__author__ = 'karl'

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Nominee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    name = db.Column(db.String(256))

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

    def __repr__(self):
        return '<Name %r>' % self.name


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    hash_name = db.Column(db.String(64))


class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    group_id = db.Column(db.Integer)
    points = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.points = 0

    def __repr__(self):
        return '<Name %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    winner = db.Column(db.Integer)
    point_value = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.winner = -1
        self.point_value = 1

    def __repr__(self):
        return '<Name %r>' % self.name


class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selection_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    nominee_id = db.Column(db.Integer)

    def __init__(self, selection_id, category_id, nominee_id):
        self.selection_id = selection_id
        self.category_id = category_id
        self.nominee_id = nominee_id

    def __repr__(self):
        return '<selection_id %d, category_id %d, nominee_id %d>' % (
            self.selection_id, self.category_id, self.nominee_id)


def seed():
    db.drop_all()
    db.create_all()

    data = json.loads(open('../dev/db/oscars.json').read())
    categories = data.keys()
    for cat_name in categories:
        cat_model = Category(cat_name)
        db.session.add(cat_model)
        db.session.commit()
        cat_values = data[cat_name]
        for value in cat_values:
            print value
            nom = Nominee(value, cat_model.id)
            db.session.add(nom)
            db.session.commit()
