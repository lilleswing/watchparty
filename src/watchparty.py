import os

import json
from flask import Flask, request
from models import db, from_json, Selection
from controllers.selections_controller import SelectionsController
from controllers.categories_controller import CategoriesController
from controllers.groups_controller import GroupsController
from controllers.events_controller import EventsController


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../dev/db/start.db')
db.app = app
db.init_app(app)
groups_controller = GroupsController(db)
selections_controller = SelectionsController(db)
categories_controller = CategoriesController(db)
events_controller = EventsController(db)


@app.route('/api/selection', methods=["POST"])
def selection_post():
    selection = from_json(Selection, request.data)
    selection.points = 0  # No cheating plx
    selection.id = None  # No cheating plx
    return to_json(selections_controller.post(selection))


@app.route('/api/selection/<int:selection_id>/pick', methods=["GET"])
def selection_get_pick(selection_id):
    return to_json(selections_controller.get_pick(selection_id))


@app.route('/api/group/<string:group_name>', methods=["GET"])
def group_get_name(group_name):
    return to_json(groups_controller.get_name(group_name))


@app.route('/api/group/<int:group_id>/selection', methods=["GET"])
def group_get_selection(group_id):
    return to_json(groups_controller.get_selection(group_id))


@app.route('/api/category/<int:category_id>', methods=["GET"])
def category_get_id(category_id):
    return to_json(categories_controller.get_id(category_id))


@app.route('/api/category/<int:category_id>/nominee', methods=["GET"])
def category_get_nominee(category_id):
    return to_json(categories_controller.get_nominee(category_id))


@app.route('/api/event/<int:event_id>')
def event_get_category(event_id):
    return to_json(events_controller.get_id(event_id))


@app.route('/api/event/<int:event_id>/category')
def event_get_category(event_id):
    return to_json(events_controller.get_category(event_id))


@app.route('/')
def home():
    # Home Screen to create a group + video
    return "Will be a create group screen with explanation video"


@app.route('/<string:group_name>')
def show(group_name):
    # Where the real magic happens
    # return groups_controller.get_id(group_name)
    return "home"


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res


def to_json(o):
    if isinstance(o, list):
        return json.dumps([x.as_dict() for x in o])
    return json.dumps(o.as_dict())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
