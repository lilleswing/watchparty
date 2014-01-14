import os

from flask import Flask, request, redirect, url_for
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///dev/db/start.db')
db = SQLAlchemy(app)


class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    points = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.points = 0

    def __repr__(self):
        return '<Name %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    winner = db.Column(db.Integer)
    point_value = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.winner = -1
        self.point_value = 1

    def __repr__(self):
        return '<Name %r>' % self.name


class Nominee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    name = db.Column(db.String(256))

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

    def __repr__(self):
        return '<Name %r>' % self.name


class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selection_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    nominee_id = db.Column(db.Integer)

    def __init__(self, selection_id, category_id, nominee_id):
        self.selection_id = selection_id
        self.category_id = category_id
        self.nominee_id = nominee_id

    def __repr__(self):
        return '<selection_id %d, category_id %d, nominee_id %d>' % (
            self.selection_id, self.category_id, self.nominee_id)


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


def seed():
    db.create_all()
    categories = [
        {"Best Motion Picture, Drama": ["12 Years a Slave", "Captain Phillips", "Gravity", "Philomena", "Rush"]}, {
            "Best Actor in a Motion Picture, Drama": ["Chiwetel Ejiofor, 12 Years A Slave",
                                                      "Idris Elba, Mandela: Long Walk To Freedom",
                                                      "Tom Hanks, Captain Phillips",
                                                      "Matthew McConaughey, Dallas Buyers Club",
                                                      "Robert Redford, All Is Lost"]}, {
            "Best Actress in a Motion Picture, Drama": ["Cate Blanchett, Blue Jasmine", "Sandra Bullock, Gravity",
                                                        "Judi Dench, Philomena", "Emma Thompson, Saving Mr Banks",
                                                        "Kate Winslet, Labor Day"]}, {
            "Best Motion Picture, Comedy or Musical": ["American Hustle", "Her", "Inside Llewyn Davis", "Nebraska",
                                                       "The Wolf of Wall Street"]}, {
            "Best Actor in a Motion Picture, Comedy or Musical": ["Christian Bale, American Hustle",
                                                                  "Bruce Dern, Nebraska",
                                                                  "Leonardo DiCaprio, The Wolf of Wall Street",
                                                                  "Oscar Isaac, Inside Llewyn Davis",
                                                                  "Joaquin Phoenix, Her"]}, {
            "Best Actress in a Motion Picture, Comedy or Musical": ["Amy Adams, American Hustle",
                                                                    "Julie Delpy, Before Midnight",
                                                                    "Greta Gerwig, Frances Ha",
                                                                    "Julia Louis-Dreyfus, Enough Said",
                                                                    "Meryl Streep, August: Osage County"]}, {
            "Best Supporting Actress in a Motion Picture": ["Sally Hawkins, Blue Jasmine",
                                                            "Jennifer Lawrence, American Hustle",
                                                            "Lupita Nyong'o, 12 Years a Slave",
                                                            "Julia Roberts, August: Osage County",
                                                            "June Squibb, Nebraska"]}, {
            "Best Supporting Actor in a Motion Picture": ["Barkhad Abdi, Captain Phillips", "Daniel Bruhl, Rush",
                                                          "Bradley Cooper, American Hustle",
                                                          "Michael Fassbender, 12 Years a Slave",
                                                          "Jared Leto, Dallas Buyers Club"]},
        {"Best Animated Feature Film": ["Frozen", "The Croods", "Despicable Me 2"]}, {
            "Best Foreign Language Film": ["Blue Is the Warmest Color", "The Great Beauty", "The Past", "The Hunt",
                                           "The Wind Rises"]}, {
            "Best Director - Motion Picture": ["Alfonso Cuaron, Gravity", "Paul Greengrass, Captain Phillips",
                                               "Steve McQueen, 12 Years a Slave", "Alexander Payne, Nebraska",
                                               "David O. Russell, American Hustle"]}, {
            "Best Screenplay - Motion Picture": ["Spike Jonze, Her", "Bob Nelson, Nebraska",
                                                 "Steve Coogan & Jeff Pope, Philomena", "John Ridley, 12 Years a Slave",
                                                 "David O. Russell and Eric Warren Singer, American Hustle"]}, {
            "Best Original Score - Motion Picture": ["Alex Ebert, All is Lost",
                                                     "Alex Heffes, Mandela: Long Walk to Freedom",
                                                     "Steven Price, Gravity",
                                                     "Hans Zimmer, 12 Years a Slave", "John Williams, The Book Thief"]},
        {
            "Best Original Song - Motion Picture": ["Atlas, The Hunger Games: Catching Fire", "Let It Go, Frozen",
                                                    "Ordinary Love, Mandela: Long Walk to Freedom",
                                                    "Please Mr. Kennedy, Inside Llewyn Davis",
                                                    "Sweeter Than Fiction, One Chance"]}, {
            "Best Television Series, Drama": ["Breaking Bad (AMC)", "Downton Abbey (PBS)", "The Good Wife (CBS)",
                                              "House of Cards (Netflix)", "Masters of Sex (Showtime)"]}, {
            "Best Actor in a Television Series, Drama": ["Bryan Cranston, Breaking Bad", "Liev Schreiber, Ray Donovan",
                                                         "Michael Sheen, Masters of Sex",
                                                         "Kevin Spacey, House of Cards",
                                                         "James Spader, The Blacklist"]}, {
            "Best Actress in a Television Series, Drama": ["Julianna Margulies, The Good Wife",
                                                           "Tatiana Maslany, Orphan Black",
                                                           "Taylor Schilling, Orange Is the New Black",
                                                           "Kerry Washington, Scandal",
                                                           "Robin Wright, House of Cards"]}, {
            "Best Televison Series, Comedy or Musical": ["The Big Bang Theory (CBS)", "Brooklyn Nine-Nine (Fox)",
                                                         "Girls (HBO)", "Modern Family (ABC)",
                                                         "Parks and Recreation (NBC)"]}, {
            "Best Actor in a Television Series, Comedy or Musical": ["Jason Bateman, Arrested Development",
                                                                     "Don Cheadle, House of Lies",
                                                                     "Michael J. Fox, The Michael J. Fox Show",
                                                                     "Jim Parsons, The Big Bang Theory",
                                                                     "Andy Samberg, Brooklyn Nine-Nine"]}, {
            "Best Actress in a Television Series, Comedy or Musical": ["Zooey Deschanel, New Girl",
                                                                       "Lena Dunham, Girls",
                                                                       "Edie Falco, Nurse Jackie",
                                                                       "Julia Louis-Dreyfus, Veep",
                                                                       "Amy Poehler, Parks and Recreation"]}]
    for category in categories:
        cat_name = list(category.keys())[0]
        cat_model = Category(cat_name)
        db.session.add(cat_model)
        db.session.commit()
        cat_values = category[cat_name]
        for value in cat_values:
            print value
            nom = Nominee(value, cat_model.id)
            db.session.add(nom)
            db.session.commit()


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
