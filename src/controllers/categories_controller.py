__author__ = 'karl'
from models import Category, Nominee
from flask import render_template


class CategoriesController():

    def __init__(self, db):
        self.db = db

    def get(self):
        categories = self.db.session.query(Category).all()
        return render_template("categoryindex.html", categories=categories)

    def get(self, category_id):
        category = self.db.session.query(Category).filter(Category.id == category_id).all()[0]
        nominees = self.db.session.query(Nominee).filter(Nominee.category_id == category_id).order_by(Nominee.id).all()
        return render_template("categoryshow.html", category=category, nominees=nominees)
