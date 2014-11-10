__author__ = 'alisonbento'


class AbstractDAO:

    def __init__(self, connection):
        self.connection = connection

    def list(self, criteria=None, arguments=()):
        pass

    def get(self, entity_id, criteria=None):
        pass

    def select(self, criteria=None, arguments=()):
        pass

    def delete(self, entity_id):
        pass

    def insert(self, entity):
        pass

    def update(self, entity):
        pass

    def convert_row_to_object(self, entity_row):
        pass
