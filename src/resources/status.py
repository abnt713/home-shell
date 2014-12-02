__author__ = 'alisonbento'

import requests

import hsres
import src.resstatus as _status
import src.base.connector
from src.dao.appliancedao import ApplianceDAO
from src.dao.statusdao import StatusDAO
from src.answer.answer import Answer


class ListStatusResource(hsres.HomeShellResource):

    def get(self, appliance_id):
        connection = src.base.connector.getcon()
        dao = StatusDAO(connection)

        status = dao.list("appliance_id = " + str(appliance_id))

        reply = Answer()

        if len(status) > 0:
            reply.set_status(_status.STATUS_OK)
            all_services = []
            for single_status in status:
                all_services.append(single_status.to_array())

            reply.add_content('status', all_services)

        else:
            reply.set_status(_status.STATUS_GENERAL_ERROR)

        connection.close()
        return reply.to_array()

    def post(self, appliance_id):
        appliancedao = ApplianceDAO(self.get_dbc())

        appliance_list = appliancedao.select('appliance_hash = ?', (appliance_id,))
        if len(appliance_list) <= 0:
            self.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
            return self.end()

        appliance = appliance_list[0]

        address = 'http://' + appliance.address + '/status/'
        r = requests.get(address)

        appjson = r.json()

        statusdao = StatusDAO(self.get_dbc())
        statusdao.update_appliance_status(appjson, appliance.id)

        self.get_dbc().commit()
        self.set_status(_status.STATUS_OK)
        return self.end()


class StatusResource(hsres.HomeShellResource):

    def get(self, appliance_id, status_id):
        dao = StatusDAO(self.get_dbc())

        status = dao.get(status_id, "appliance_id = " + str(appliance_id))

        if status is None:
            self.set_status(_status.STATUS_GENERAL_ERROR)
        else:
            self.set_status(_status.STATUS_OK)
            self.add_content('status', status.to_array())

        return self.end()