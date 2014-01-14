import os

from flask import Flask, request, redirect, url_for
from flask import render_template
from src.models import Selection, Category, Group, Event, Nominee, Pick, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dev/db/start.db')
db.app = app
db.init_app(app)


@app.route('/')
def home():
    selections = db.session.query(Selection).order_by(Selection.points).all()[::-1]
    return render_template('scoreboard.html', selections=selections)


@app.route('/selection/create', methods=["GET"])
def create_selection_view():
    return create_selection_view(None)


@app.route('/category', methods=["GET"])
def category_index():
    categories = db.session.query(Category).all()
    return render_template("categoryindex.html", categories=categories)


@app.route('/category/<int:category_id>', methods=["GET"])
def category_show(category_id):
    category = db.session.query(Category).filter(Category.id == category_id).all()[0]
    nominees = db.session.query(Nominee).filter(Nominee.category_id == category_id).order_by(Nominee.id).all()
    return render_template("categoryshow.html", category=category, nominees=nominees)


def create_selection_view(warning):
    params = []
    categories = db.session.query(Category).all()
    for category in categories:
        param = {}
        nominees = db.session.query(Nominee).filter(Nominee.category_id == category.id).all()
        param["category"] = category
        param["nominees"] = nominees
        params.append(param)
    return render_template("selectioncreate.html", warning=warning, params=params)


@app.route('/selection/create', methods=["POST"])
def create_selection():
    category_ids = set([str(x[0]) for x in db.session.query(Category.id).order_by(Category.id).all()])
    if not category_ids.issubset(request.form.keys()):
        return create_selection_view("Please select a winner for every category")
    if request.form["selection_name"] == "":
        return create_selection_view("Please select a name for your selections")
    selection = Selection(request.form["selection_name"])
    db.session.add(selection)
    db.session.commit()
    for category_id in category_ids:
        nominee_id = int(request.form[category_id])
        pick = Pick(selection.id, category_id, nominee_id)
        db.session.add(pick)
        db.session.commit()
    return redirect(url_for('view_selection', selection_id=selection.id))


@app.route('/selection/<int:selection_id>', methods=["GET"])
def view_selection(selection_id):
    selection = db.session.query(Selection).filter(Selection.id == selection_id).all()[0]
    picks = db.session.query(Pick).filter(Pick.selection_id == selection_id).order_by(Pick.category_id).all()
    params = []
    for pick in picks:
        category_name = db.session.query(Category).filter(Category.id == pick.category_id).all()[0].name
        nominee_name = db.session.query(Nominee).filter(Nominee.id == pick.nominee_id).all()[0].name
        param = {"category_name": category_name, "nominee_name": nominee_name}
        params.append(param)
    return render_template("selectionview.html", params=params, name=selection.name)


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
