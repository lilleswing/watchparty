__author__ = 'karl'
import json
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Nominee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    name = db.Column(db.String(256))

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "category_id": self.category_id,
            "name": self.name
        })

    def __repr__(self):
        return '<Name %r>' % self.name


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    event_id = db.Column(db.Integer)


class Categories_Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    point_value = db.Column(db.Integer)


class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    group_id = db.Column(db.Integer)
    points = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.points = 0

    def __repr__(self):
        return '<Name %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    winner = db.Column(db.Integer)
    point_value = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.winner = -1
        self.point_value = 1

    def __repr__(self):
        return '<Name %r>' % self.name

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "event_id": self.event_id,
            "name": self.name,
            "winner": self.winner,
            "point_value": self.point_value
        })


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


def seed():
    db.drop_all()
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
    event = Event()
    event.name = "Golden Globes 2014"
    db.session.add(event)
    db.session.commit()
    for category in categories:
        cat_name = list(category.keys())[0]
        cat_model = Category(cat_name)
        cat_model.event_id = event.id
        db.session.add(cat_model)
        db.session.commit()
        cat_values = category[cat_name]
        for value in cat_values:
            print value
            nom = Nominee(value, cat_model.id)
            db.session.add(nom)
            db.session.commit()
    group = Group()
    group.event_id = event.id
    group.name = "abc"
    db.session.add(group)
    db.session.commit()
