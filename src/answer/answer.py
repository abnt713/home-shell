__author__ = 'alisonbento'

import src.requestentity.arrayparsableentity as parsable


class Answer(parsable.ArrayParsableEntity):

    def __init__(self):
        self.status = 0
        self.contents = {}

    def set_status(self, status):
        self.status = status

    def add_content(self, index, content):
        self.contents.update({index: content})

    def to_array(self):
        return {
            "status": self.status,
            "contents": self.contents
        }