# Watchparty

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
$ pip install -r requirements.txt
$ source venv/bin/activate
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
Create default sqlite data with 2014 Golden Globes.
    Load from sqlite if can't find os.environ['DATABASE_URL']
    Before the night has started
    Middle of the night
    After the night has ended
Fix headers showing up under the tab-header
Create groups.  Only see other selections from the same group.
    Groups can also set points for each category
    Have default point-set
See who selected which nominee to win each category.
    With category announced
    With category unnanounced
Create "Categories" tab which list categories announced and to be announced
Show Points Left to be announced at top of scoreboard.
Edit Selections -- requires some sort of auth system
Use jquery to load the screen of what is happening --> "watch" tab
    Category when it is being announced + 30 seconds after announds
    Scoreboard when no category is being being announced
