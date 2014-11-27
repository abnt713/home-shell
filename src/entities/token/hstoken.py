__author__ = 'alisonbento'


import src.base.arrayparsableentity as parsable


class HomeShellToken(parsable.ArrayParsableEntity):

    def __init__(self):
        self.id = 0
        self.user_id = 0
        self.token = None
        self.created = None
        self.valid = None

    def to_array(self):
        return {
            "id": self.id,
            "token": self.token,
            "created": self.created,
            "valid": self.valid
        }
