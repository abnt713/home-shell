__author__ = 'alisonbento'

import src.base.arrayparsableentity as parsable


class HomeShellFullAppliance(parsable.ArrayParsableEntity):

    def __init__(self):
        self.appliance = None
        self.services = None
        self.status = None

    def to_array(self):
        appliance_array = self.appliance.to_array()

        all_services = []
        for service in self.services:
            all_services.append(service.to_array())

        all_status = {}
        for single_status in self.status:
            all_status[single_status.name] = single_status.value
            # all_status.append(single_status.to_array())

        appliance_array.update({'services': all_services})
        appliance_array.update({'status': all_status})

        return appliance_array
