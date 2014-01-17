import os

from flask import Flask, request
from flask import render_template
from models import Selection, db
from controllers.selections_controller import SelectionsController
from controllers.categories_controller import CategoriesController


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../dev/db/start.db')
db.app = app
db.init_app(app)
selectionsController = SelectionsController(db)
categoriesController = CategoriesController(db)


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
def category_get():
    return categoriesController.get()


@app.route('/category/<int:category_id>', methods=["GET"])
def category_show(category_id):
    return categoriesController.get(category_id)


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
