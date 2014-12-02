__author__ = 'alisonbento'

import src.resources.hsres as hsres

import src.dao.fullappliancedao as fullappliancedao
import src.resstatus as _status
import requests
import datetime
import configs

from src.appliances.statusupdater import StatusUpdater


class ApplianceListResource(hsres.HomeShellResource):

    def get(self):

        dao = fullappliancedao.FullApplianceDAO(self.get_dbc())
        appliances = dao.list()

        if len(appliances) > 0:
            self.set_status(_status.STATUS_OK)
            all_appliances = []
            for appliance in appliances:
                all_appliances.append(appliance.to_array())

            self.add_content('appliances', all_appliances)

        return self.end()


class ApplianceResource(hsres.HomeShellResource):

    def get(self, appliance_id):

        dao = fullappliancedao.FullApplianceDAO(self.get_dbc())
        fullappliance = dao.get(appliance_id)

        self.set_status(_status.STATUS_OK)
        if fullappliance is None:
            self.set_status(_status.STATUS_GENERAL_ERROR)
        else:
            try:
                if self.is_time_to_refresh_appliance(fullappliance):
                    fullappliance = self.refresh_appliance(fullappliance, self.get_dbc())
                self.add_content('appliance', fullappliance.to_array())
            except requests.ConnectionError, requests.HTTPError:
                self.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)

        return self.end()

    def refresh_appliance(self, fullappliance, connection):
        appliance = fullappliance.appliance
        address = 'http://' + appliance.address

        response = requests.get(address)
        if response.status_code:
            appliance_json = response.json()
            print 'Appliance response: ' + str(appliance_json)
            updater = StatusUpdater(connection)
            fullappliance = updater.updateStatus(appliance, appliance_json)
        else:
            raise requests.HTTPError(response)
        return fullappliance

    def is_time_to_refresh_appliance(self, fullappliance):
        modified_datetime = fullappliance.appliance.modified_datetime

        delta = datetime.datetime.now() - modified_datetime
        delta_seconds = delta.total_seconds()

        return delta_seconds >= configs.MIN_SECONDS_TO_REFRESH_APPLIANCE