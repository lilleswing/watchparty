import os

from flask import Flask, request
from flask import render_template
from src.models import Selection, Category, Group, Event, Nominee, Pick, db
from src.controllers.selections_controller import SelectionsController


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dev/db/start.db')
db.app = app
db.init_app(app)
selectionsController = SelectionsController(db)


@app.route('/')
def home():
    selections = db.session.query(Selection).order_by(Selection.points).all()[::-1]
    return render_template('scoreboard.html', selections=selections)


@app.route('/selection/create', methods=["GET"])
def selection_create_get():
    return selectionsController.create_get()


@app.route('/selection/create', methods=["POST"])
def selection_create_post():
    return selectionsController.create_post(request.form)


@app.route('/selection/<int:selection_id>', methods=["GET"])
def selection_get(selection_id):
    return selectionsController.get(selection_id)


@app.route('/category', methods=["GET"])
def category_index():
    categories = db.session.query(Category).all()
    return render_template("categoryindex.html", categories=categories)


@app.route('/category/<int:category_id>', methods=["GET"])
def category_show(category_id):
    category = db.session.query(Category).filter(Category.id == category_id).all()[0]
    nominees = db.session.query(Nominee).filter(Nominee.category_id == category_id).order_by(Nominee.id).all()
    return render_template("categoryshow.html", category=category, nominees=nominees)


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res


def update_score():
    selections = db.session.query(Selection).all()
    for selection in selections:
        picks = db.session.query(Pick).filter(Pick.selection_id == selection.id).all()
        points = 0
        for pick in picks:
            category = db.session.query(Category).filter(Category.id == pick.category_id).all()[0]
            if pick.nominee_id == category.winner:
                points += category.point_value
        selection.points = points
        db.session.merge(selection)
        db.session.commit()


def set_winner(category_id, nominee_id):
    category = db.session.query(Category).filter(Category.id == category_id).all()[0]
    category.winner = nominee_id
    db.session.merge(category)
    db.session.commit()
    update_score()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
