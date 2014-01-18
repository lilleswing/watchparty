from dao.category_dao import CategoryDao
from dao.group_dao import GroupDao
from dao.nominee_dao import NomineeDao
from dao.selection_dao import SelectionDao
from flask import render_template, redirect, url_for
from models import Nominee, Category, Pick, Selection

__author__ = 'leswing'


class SelectionsController():

    def __init__(self, db):
        self.db = db
        self.group_dao = GroupDao(db)
        self.category_dao = CategoryDao(db)
        self.nominee_dao = NomineeDao(db)
        self.selection_dao = SelectionDao(db)

    def create_get(self, group_name, warning=None):
        params = []
        group = self.group_dao.get_by_name(group_name)
        categories = self.category_dao.list(group.event_id)
        for category in categories:
            param = {}
            nominees = self.nominee_dao.list(category.id)
            param["category"] = category
            param["nominees"] = nominees
            params.append(param)
        return render_template("selectioncreate.html", warning=warning, params=params)

    # TODO(Leswing) Change to reading in from JSON
    def create_post(self, group_name, params):
        group = self.group_dao.get_by_name(group_name)
        category_ids = set([str(x[0]) for x in self.db.session.query(Category.id).order_by(Category.id).all()])
        if not category_ids.issubset(params.keys()):
            return self.create_get("Please select a winner for every category")
        if params["selection_name"] == "":
            return self.create_get("Please select a name for your selections")
        selection = Selection(params["selection_name"])
        selection.group_id = group.id
        self.db.session.add(selection)
        self.db.session.commit()
        for category_id in category_ids:
            nominee_id = int(params[category_id])
            pick = Pick(selection.id, category_id, nominee_id)
            self.db.session.add(pick)
            self.db.session.commit()
        return redirect(url_for('selection_get', selection_id=selection.id))

    def get(self, selection_id):
        selection = self.selection_dao.get(selection_id)
        picks = self.db.session.query(Pick).filter(Pick.selection_id == selection_id).order_by(Pick.category_id).all()
        params = []
        for pick in picks:
            category_name = self.db.session.query(Category).filter(Category.id == pick.category_id).all()[0].name
            nominee_name = self.db.session.query(Nominee).filter(Nominee.id == pick.nominee_id).all()[0].name
            param = {"category_name": category_name, "nominee_name": nominee_name}
            params.append(param)
        return render_template("selectionview.html", params=params, name=selection.name)