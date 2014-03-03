__author__ = 'leswing'

from flask import render_template, redirect, url_for
from models import Nominee, Category, Pick, Selection

def sort_categories(categories, id_func):
    category_order = [7, 18, 9, 10, 20, 2, 21, 11, 22, 23, 5, 4,13, 8, 6,
                     1, 17, 16, 12, 14, 3, 15, 19, 24]
    cat_dict = {id_func(x): x for x in categories}
    ordered = list()
    print cat_dict
    for elem in category_order:
        ordered.append(cat_dict[elem])
    return ordered

class SelectionsController():

    def __init__(self, db):
        self.db = db

    def create_get(self, group, warning=None):
        params = []
        categories = self.db.session.query(Category).all()
        categories = sort_categories(categories, lambda x: x.id)
        for category in categories:
            param = {}
            nominees = self.db.session.query(Nominee).filter(Nominee.category_id == category.id).all()
            param["category"] = category
            param["nominees"] = nominees
            params.append(param)
        return render_template("selectioncreate.html", warning=warning, params=params, group=group)

    def create_post(self, group, params):
        if True:
            return None
        category_ids = set([str(x[0]) for x in self.db.session.query(Category.id).order_by(Category.id).all()])
        if not category_ids.issubset(params.keys()):
            return self.create_get("Please select a winner for every category")
        if params["selection_name"] == "":
            return self.create_get("Please select a name for your selections")
        selection = Selection(params["selection_name"])
        selection.group_id = group.id
        self.db.session.add(selection)
        self.db.session.commit()
        picks = list()
        for category_id in category_ids:
            nominee_id = int(params[category_id])
            pick = Pick(selection.id, category_id, nominee_id)
            picks.append(pick)
        self.db.session.add_all(picks)
        self.db.session.commit()
        return self.get(group=group, selection_id=selection.id)

    def get(self, group, selection_id):
        selection = self.db.session.query(Selection).filter(Selection.id == selection_id).first()
        picks = self.db.session.query(Pick).filter(Pick.selection_id == selection_id).order_by(Pick.category_id).all()
        picks = sort_categories(picks, lambda x: x.category_id)
        params = []
        for pick in picks:
            category_name = self.db.session.query(Category).filter(Category.id == pick.category_id).first().name
            nominee_name = self.db.session.query(Nominee).filter(Nominee.id == pick.nominee_id).first().name
            param = {"category_name": category_name, "nominee_name": nominee_name}
            params.append(param)
        return render_template("selectionview.html", group=group, params=params, name=selection.name)
