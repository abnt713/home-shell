__author__ = 'alisonbento'


import flask_restful
import flask

import src.hsstatus as _status
import src.res.connector as connector

from src.dao.servicedao import ServiceDAO
from src.answer.answer import Answer


class ServiceResource(flask_restful.Resource):

    def get(self, appliance_id, service_id):

        connection = connector.getcon()
        dao = ServiceDAO(connection)

        service = dao.get(service_id, "appliance_id = " + str(appliance_id))

        reply = Answer()
        if service is None:
            reply.set_status(_status.STATUS_GENERAL_ERROR)
        else:
            reply.set_status(_status.STATUS_OK)
            reply.add_content('service', service.to_array())

        connection.close()
        return flask.jsonify(reply.to_array())
