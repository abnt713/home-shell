__author__ = 'alisonbento'


import src.base.arrayparsableentity as parsable


class HomeShellParam(parsable.ArrayParsableEntity):

    def __init__(self, param_id=0, name=None):
        self.id = param_id
        self.name = name

    def to_array(self):
        return {
            'id': self.id,
            'name': self.name
        }