import os

from flask import Flask, request
from flask import render_template
from models import Selection, db, Group
from controllers.selections_controller import SelectionsController
from controllers.categories_controller import CategoriesController
from controllers. admin_controller import AdminController
from controllers.groups_controller import GroupsController


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///../dev/db/start.db')
db.app = app
db.init_app(app)
selectionsController = SelectionsController(db)
categoriesController = CategoriesController(db)
groupsController = GroupsController(db)
adminController = AdminController(db)


@app.route('/')
def home():
    return groupsController.get()

@app.route('/group', methods=["POST"])
def group_create():
    return groupsController.create(request.form)

@app.route('/admin/<int:category_id>', methods=["GET"])
def admin_category(category_id):
    return adminController.get_category(category_id)

@app.route('/admin/<int:category_id>', methods=["POST"])
def admin_pick_winner(category_id):
    return adminController.pick_winner(category_id, request.form)

@app.route('/admin', methods=["GET"])
def admin_get():
    return adminController.list()




@app.route('/<string:hash_name>/selection/create', methods=["GET"])
def selection_create_get(hash_name):
    group = db.session.query(Group).filter(Group.hash_name == hash_name).one()
    return selectionsController.create_get(group)


@app.route('/<string:hash_name>/selection/create', methods=["POST"])
def selection_create_post(hash_name):
    group = db.session.query(Group).filter(Group.hash_name == hash_name).one()
    return selectionsController.create_post(group, request.form)


@app.route('/<string:hash_name>/selection/<int:selection_id>', methods=["GET"])
def selection_get(hash_name, selection_id):
    group = db.session.query(Group).filter(Group.hash_name == hash_name).one()
    return selectionsController.get(group, selection_id)


@app.route('/category', methods=["GET"])
def category_get():
    return categoriesController.get()


@app.route('/category/<int:category_id>', methods=["GET"])
def category_show(category_id):
    return categoriesController.get(category_id)

@app.route('/<string:hash_name>', methods=["GET"])
def scoreboard(hash_name):
    if hash_name == 'favicon.ico':
        return ""
    group = db.session.query(Group).filter(Group.hash_name == hash_name).one()
    selections = db.session.query(Selection).filter(Selection.group_id == group.id)\
        .order_by(Selection.points).all()[::-1]
    return render_template('scoreboard.html', group=group, selections=selections)


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
