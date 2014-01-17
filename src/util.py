__author__ = 'karl'
from src.models import Selection, Category, Pick


class Util():

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
