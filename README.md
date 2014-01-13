# Watchparty
[See It Live](http://watchparty.herokuapp.com)

This repository contains a Flask application for watching award shows.

Allows users to select which nominees they think will win in each category.
Shows an overall scoreboard of points users get from correct guesses.
Allows users to see their selections.

## Usage

### Initial

```bash
$ git clone https://github.com/lilleswing/watchparty.git
$ cd watchparty
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python watchparty.py
```

## Heroku

### Setup
````bash
$ heroku create
$ git push heroku master
```


### Database

```bash
$ heroku addons:add heroku-postgresql:dev
-----> Adding heroku-postgresql:dev to some-app-name... done, v196 (free)
Attached as HEROKU_POSTGRESQL_COLOR
Database has been created and is available
$ heroku pg:promote HEROKU_POSTGRESQL_COLOR
$ heroku run python
```

and in the Python REPL:

```python
>>> import watchparty
>>> watchparty.seed()
```

## TODO
- [ ] Create default sqlite data with 2014 Golden Globes.
    * Load from sqlite if can't find os.environ['DATABASE_URL']
    * Before the night has started
    * Middle of the night
    * After the night has ended
- [ ] Use templates for HTML files instead of copy-pasta
    * Considering switching to backbone + resty json
- [ ] Fix headers showing up under the tab-header
- [ ] Create groups.  Only see other selections from the same group.
    * Groups can also set points for each category
    * Have default point-set
- [ ] See who selected which nominee to win each category.
    * With category announced
    * With category unannounced
- [ ] Create "Categories" tab which list categories announced and to be announced
- [ ] Show Points Left to be announced at top of scoreboard. Also Available Points
- [ ] Edit Selections -- requires some sort of auth system
- [ ] Use jquery to load the screen of what is happening --> "watch" tab
    * Category when it is being announced + 30 seconds after announced
    * Scoreboard when no category is being being announced
- [ ] When selecting a nominee to win a category load relevant picture
- [ ] Create "events" so I don't have to wipe the DB for every new event
- [ ] Get a favicon
- [ ] Create admin panel to set winners, create events
