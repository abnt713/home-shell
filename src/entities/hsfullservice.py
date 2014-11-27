__author__ = 'alisonbento'

import src.base.arrayparsableentity as parsable


class HomeShellFullService(parsable.ArrayParsableEntity):

    def __init__(self):
        self.service = None
        self.params = None

    def to_array(self):
        service_array = self.service.to_array()

        all_params = []
        for param in self.params:
            all_params.append(param.to_array())

        service_array.update({'params': all_params})

        return service_array
