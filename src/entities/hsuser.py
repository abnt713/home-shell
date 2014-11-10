__author__ = 'alisonbento'

import src.requestentity.arrayparsableentity as parsable


class HomeShellUser(parsable.ArrayParsableEntity):

    def __init__(self):
        self.id = 0
        self.name = None
        self.gender = None
        self.email = None
        self.username = None
        self.password = None
        self.locale = None
        self.created = None
        self.modified = None

    def to_array(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "email": self.email,
            "locale": self.locale,
            "created": self.created,
            "modified": self.modified
        }
