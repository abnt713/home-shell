__author__ = 'alisonbento'


import src.requestentity.arrayparsableentity as parsable


class HomeShellService(parsable.ArrayParsableEntity):

    def __init__(self, service_id=0, name=None):
        self.id = service_id
        self.name = name

    def to_array(self):
        return {
            'id': self.id,
            'name': self.name
        }