__author__ = 'alisonbento'

import flask

import flask_restful

import src.resstatus as _status
import src.res.connector as connector
from src.dao.statusdao import StatusDAO
from src.answer.answer import Answer


class StatusResource(flask_restful.Resource):

    def get(self, appliance_id, status_id):
        connection = connector.getcon()
        dao = StatusDAO(connection)

        status = dao.get(status_id, "appliance_id = " + str(appliance_id))

        reply = Answer()
        if status is None:
            reply.set_status(_status.STATUS_GENERAL_ERROR)
        else:
            reply.set_status(_status.STATUS_OK)
            reply.add_content('status', status.to_array())

        connection.close()
        return reply.to_array()
