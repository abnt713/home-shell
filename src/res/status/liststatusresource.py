__author__ = 'alisonbento'

import requests

import src.res.hsres as hsres
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
