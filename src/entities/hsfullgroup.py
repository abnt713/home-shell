__author__ = 'alisonbento'

import src.base.arrayparsableentity as parsable


class HomeShellFullGroup(parsable.ArrayParsableEntity):

    def __init__(self):
        self.group = None
        self.appliances = []

    def to_array(self):
        all_appliances = []

        for appliance in self.appliances:
            all_appliances.append(appliance.to_array())

        group_array = self.group.to_array()
        group_array.update({'appliances': all_appliances})

        return group_array
