from models import Event

__author__ = 'leswing'


class EventDao():
    def __init__(self, db):
        self.db = db

    def get(self, event_id):
        return self.db.session.query(Event).filter(Event.id == event_id).first()
