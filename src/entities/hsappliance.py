__author__ = 'alisonbento'

import src.requestentity.arrayparsableentity as parsable


class HomeShellAppliance(parsable.ArrayParsableEntity):

    def __init__(self):
        self.id = 0
        self.key = None
        self.type = None
        self.name = None
        self.address = None
        self.created = None
        self.modified = None

    def to_array(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name
        }
