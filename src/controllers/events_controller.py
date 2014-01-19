from dao.category_dao import CategoryDao
from dao.event_dao import EventDao

__author__ = 'leswing'


class EventsController():

    def __init__(self, db):
        self.category_dao = CategoryDao(db)
        self.event_dao = EventDao(db)

    def get_category(self, event_id):
        return self.category_dao.get_by_event(event_id)

    def get_id(self, event_id):
        return self.event_dao.get(event_id)
