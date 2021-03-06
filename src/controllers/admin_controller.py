from flask import render_template, url_for, redirect
from models import Selection, Pick, Category, Nominee

__author__ = 'leswing'


class AdminController():
    def __init__(self, db):
        self.db = db

    def update_score(self):
        selections = self.db.session.query(Selection).all()
        for selection in selections:
            picks = self.db.session.query(Pick).filter(Pick.selection_id == selection.id).all()
            points = 0
            for pick in picks:
                category = self.db.session.query(Category).filter(Category.id == pick.category_id).all()[0]
                if pick.nominee_id == category.winner:
                    points += category.point_value
            selection.points = points
            self.db.session.merge(selection)
            self.db.session.commit()

    def set_winner(self, category_id, nominee_id):
        category = self.db.session.query(Category).filter(Category.id == category_id).all()[0]
        category.winner = nominee_id
        self.db.session.merge(category)
        self.db.session.commit()
        self.update_score()

    def list(self):
        categories = self.db.session.query(Category).order_by(Category.id).all()
        return render_template("adminlist.html", categories=categories)

    def get_category(self, category_id):
        category = self.db.session.query(Category).filter(Category.id == category_id).all()[0]
        nominees = self.db.session.query(Nominee).filter(Nominee.category_id == category_id).all()
        return render_template("adminpick.html", nominees=nominees, category=category)

    def pick_winner(self, category_id, form):
        nominee_id = int(form['winner'])
        nominee = self.db.session.query(Nominee).filter(Nominee.id == nominee_id).all()[0]
        self.set_winner(category_id, nominee_id)
        return redirect(url_for('admin_get'))

