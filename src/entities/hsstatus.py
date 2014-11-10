__author__ = 'alisonbento'

import src.requestentity.arrayparsableentity as parsable


class HomeShellStatus(parsable.ArrayParsableEntity):

    def __init__(self, id=0, name=None, value=0):
        self.id = id
        self.name = name
        self.value = value

    def to_array(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value
        }