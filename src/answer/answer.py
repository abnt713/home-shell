__author__ = 'alisonbento'

import src.requestentity.arrayparsableentity as parsable
import configs
import src.resstatus as _status

class Answer(parsable.ArrayParsableEntity):

    def __init__(self):
        self.status = 0
        self.contents = {}

    def set_status(self, status):
        self.status = status

    def add_content(self, index, content):
        self.contents.update({index: content})

    def to_array(self):
        array = {
            "status": self.status,
            "contents": self.contents
        }

        if configs.ANSWER_HUMAN_MODE:
            message = _status.RES_DICT[self.status]
            array.update({'message': message})

        return array