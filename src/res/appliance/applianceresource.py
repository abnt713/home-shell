# encoding: utf-8

__author__ = 'alisonbento'

import flask_restful
import datetime
import configs
import requests

import src.base.connector as connector
import src.dao.fullappliancedao as fullappliancedao
import src.answer.answer as hs_answer
import src.resstatus as _status
from src.appliances.statusupdater import StatusUpdater

class ApplianceResource(flask_restful.Resource):

    def get(self, appliance_id):

        connection = connector.getcon()
        dao = fullappliancedao.FullApplianceDAO(connection)

        fullappliance = dao.get(appliance_id)

        reply = hs_answer.Answer()
        reply.set_status(_status.STATUS_OK)
        if fullappliance is None:
            reply.set_status(_status.STATUS_GENERAL_ERROR)
            reply.add_content('appliance', {})
        else:
            try:
                if self.is_time_to_refresh_appliance(fullappliance):
                    fullappliance = self.refresh_appliance(fullappliance, connection)
                reply.add_content('appliance', fullappliance.to_array())
            except requests.ConnectionError, requests.HTTPError:
                reply.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)

        connection.close()
        return reply.to_array()

    def refresh_appliance(self, fullappliance, connection):
        appliance = fullappliance.appliance
        address = 'http://' + appliance.address

        response = requests.get(address)
        if response.status_code:
            applianceJson = response.json()
            print 'Appliance response: ' + str(applianceJson)
            updater = StatusUpdater(connection)
            fullappliance = updater.updateStatus(appliance, applianceJson)
        else:
            raise requests.HTTPError(response)
        return fullappliance

    def is_time_to_refresh_appliance(self, fullappliance):
        modified_datetime = fullappliance.appliance.modified_datetime

        delta = datetime.datetime.now() - modified_datetime
        delta_seconds = delta.total_seconds()

        return delta_seconds >= configs.MIN_SECONDS_TO_REFRESH_APPLIANCE

