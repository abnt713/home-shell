__author__ = 'alisonbento'


import src.base.arrayparsableentity as parsable


class HomeShellExtra(parsable.ArrayParsableEntity):

    def __init__(self, extra_id=0, appliance_id=0, extra_key=None, extra_value=None, extra_date=None, created=None):
        self.id = extra_id
        self.appliance_id = appliance_id
        self.extra_key = extra_key
        self.extra_value = extra_value
        self.extra_date = extra_date
        self.created = created

    def to_array(self):
        return {
            'id': self.id,
            'key': self.extra_key,
            'value': self.extra_value,
            'date': self.extra_date
        }