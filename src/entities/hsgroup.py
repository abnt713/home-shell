__author__ = 'alisonbento'

import src.requestentity.arrayparsableentity as parsable


class HomeShellGroup(parsable.ArrayParsableEntity):

    def __init__(self):
        self.id = 0
        self.author_id = 0
        self.name = None
        self.created = None
        self.modified = None

    def to_array(self):
        return {
            'id': self.id,
            'name': self.name
        }