__author__ = 'alisonbento'

import flask

import flask_restful

import src.hsstatus as _status
import src.res.connector
from src.dao.statusdao import StatusDAO
from src.answer.answer import Answer


class ListStatusResource(flask_restful.Resource):

    def get(self, appliance_id):
        connection = src.res.connector.getcon()
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
        return flask.jsonify(reply.to_array())
