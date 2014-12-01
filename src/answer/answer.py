__author__ = 'alisonbento'

import src.base.arrayparsableentity as parsable
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
        print(self.status)
        array = {
            "status": self.status[0],
            "contents": self.contents
        }

        if configs.ANSWER_HUMAN_MODE:
            message = self.status[1]
            array.update({'message': message})

        return array