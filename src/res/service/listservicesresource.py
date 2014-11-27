__author__ = 'alisonbento'

import flask_restful

import src.resstatus as _status
import src.base.connector as connector
from src.dao.servicedao import ServiceDAO
from src.answer.answer import Answer


class ListServicesResource(flask_restful.Resource):
    def get(self, appliance_id):

        connection = connector.getcon()
        dao = ServiceDAO(connection)

        services = dao.list("appliance_id = ?", (appliance_id,))

        reply = Answer()

        if len(services) > 0:
            reply.set_status(_status.STATUS_OK)
            all_services = []
            for service in services:
                all_services.append(service.to_array())

            reply.add_content('services', all_services)

        else:
            reply.set_status(_status.STATUS_GENERAL_ERROR)

        connection.close()
        return reply.to_array()
