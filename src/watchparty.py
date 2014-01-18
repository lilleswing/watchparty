import os

from flask import Flask, request
from models import db
from controllers.selections_controller import SelectionsController
from controllers.categories_controller import CategoriesController
from controllers.groups_controller import GroupsController


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../dev/db/start.db')
db.app = app
db.init_app(app)
selections_controller = SelectionsController(db)
categories_controller = CategoriesController(db)
groups_controller = GroupsController(db)


@app.route('/')
def group_get():
    return groups_controller.get()

@app.route('/<string:group_name>')
def group_get_id(group_name):
    return groups_controller.get_id(group_name)


@app.route('/<string:group_name>/selection/create', methods=["GET"])
def selection_create_get(group_name):
    return selections_controller.create_get(group_name)


@app.route('/selection/create', methods=["POST"])
def selection_create_post():
    return selections_controller.create_post(request.form)


@app.route('/selection/<int:selection_id>', methods=["GET"])
def selection_get_id(selection_id):
    return selections_controller.get(selection_id)


@app.route('/category', methods=["GET"])
def category_get():
    return categories_controller.get()


@app.route('/category/<int:category_id>', methods=["GET"])
def category_show(category_id):
    return categories_controller.get_id(category_id)


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
