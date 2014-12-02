__author__ = 'alisonbento'

import nmap
import src.resources.hsres as hsres

import src.dao.fullappliancedao as fullappliancedao
import src.dao.appliancedao as appliancedao
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


class ScanAppliancesResource(hsres.HomeShellResource):

    def get(self):
        hsappliancedao = appliancedao.ApplianceDAO(self.get_dbc())

        all_appliances = hsappliancedao.list()

        already_know_hosts = []
        for appliance in all_appliances:
            already_know_hosts.append(appliance.address)

        nm = nmap.PortScanner()
        nm.scan(hosts=configs.NETWORK_IP_RANGE, arguments='-n -sP -PE -PA21,23,80,3389')
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

        valid_hosts = []
        for host, status in hosts_list:
            try:
                address = 'http://' + host
                r = requests.get(address)
                r.json()
                if host not in already_know_hosts:
                    valid_hosts.append(host)
            except:
                pass

        self.set_status(_status.STATUS_OK)
        self.add_content('new_appliances', len(valid_hosts))

        return self.end()
