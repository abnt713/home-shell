__author__ = 'alisonbento'


import flask_restful
import flask
import requests

import src.hsstatus as _status
import src.res.connector as connector

from src.dao.appliancedao import ApplianceDAO
from src.dao.servicedao import ServiceDAO
from src.answer.answer import Answer


class ServiceResource(flask_restful.Resource):

    def get(self, appliance_id, service_id):

        connection = connector.getcon()
        dao = ServiceDAO(connection)

        if service_id.isdigit():
            service = dao.get(service_id, "appliance_id = " + str(appliance_id))
        else:
            services = dao.select("appliance_id = ? AND service_trigger = ?", (appliance_id, service_id))
            if len(services) > 0:
                service = services[0]
            else:
                service = None

        reply = Answer()
        if service is None:
            reply.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
        else:
            reply.set_status(_status.STATUS_OK)
            reply.add_content('service', service.to_array())

        connection.close()
        return flask.jsonify(reply.to_array())

    def post(self, appliance_id, service_id):
        connection = connector.getcon()
        appliancedao = ApplianceDAO(connection)
        servicedao = ServiceDAO(connection)

        if service_id.isdigit():
            service = servicedao.get(service_id, "appliance_id = " + str(appliance_id))
        else:
            services = servicedao.select("appliance_id = ? AND service_trigger = ?", (appliance_id, service_id))
            if len(services) > 0:
                service = services[0]
            else:
                service = None

        reply = Answer()
        if service is None:
            reply.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
        else:
            appliance = appliancedao.get(appliance_id)
            address = 'http://' + appliance.address + '/services/' + service.name

            try:
                r = requests.get(address)

                if r.status_code == '200':
                    reply.set_status(_status.STATUS_OK)
                    reply.add_content('service', service.to_array())
                else:
                    reply.set_status(_status.STATUS_APPLIANCE_UNREACHEBLE)

            except requests.ConnectionError:
                reply.set_status(_status.STATUS_APPLIANCE_UNREACHEBLE)

        connection.close()
        return flask.jsonify(reply.to_array())
