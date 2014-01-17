__author__ = 'leswing'

from flask import render_template, redirect, url_for
from src.models import Nominee, Category, Pick, Selection


class SelectionsController():

    def __init__(self, db):
        self.db = db

    def create_get(self, warning=None):
        params = []
        categories = self.db.session.query(Category).all()
        for category in categories:
            param = {}
            nominees = self.db.session.query(Nominee).filter(Nominee.category_id == category.id).all()
            param["category"] = category
            param["nominees"] = nominees
            params.append(param)
        return render_template("selectioncreate.html", warning=warning, params=params)

    def create_post(self, params):
        category_ids = set([str(x[0]) for x in self.db.session.query(Category.id).order_by(Category.id).all()])
        if not category_ids.issubset(params.keys()):
            return self.create_get("Please select a winner for every category")
        if params["selection_name"] == "":
            return self.create_get("Please select a name for your selections")
        selection = Selection(params["selection_name"])
        self.db.session.add(selection)
        self.db.session.commit()
        for category_id in category_ids:
            nominee_id = int(params[category_id])
            pick = Pick(selection.id, category_id, nominee_id)
            self.db.session.add(pick)
            self.db.session.commit()
        return redirect(url_for('selection_get', selection_id=selection.id))

    def get(self, selection_id):
        selection = self.db.session.query(Selection).filter(Selection.id == selection_id).all()[0]
        picks = self.db.session.query(Pick).filter(Pick.selection_id == selection_id).order_by(Pick.category_id).all()
        params = []
        for pick in picks:
            category_name = self.db.session.query(Category).filter(Category.id == pick.category_id).all()[0].name
            nominee_name = self.db.session.query(Nominee).filter(Nominee.id == pick.nominee_id).all()[0].name
            param = {"category_name": category_name, "nominee_name": nominee_name}
            params.append(param)
        return render_template("selectionview.html", params=params, name=selection.name)