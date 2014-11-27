__author__ = 'alisonbento'

import flask_restful

import src.base.connector as connector
import src.dao.fullappliancedao as fullappliancedao
import src.answer.answer as hs_answer
import src.resstatus as _status


class ApplianceResource(flask_restful.Resource):

    def get(self, appliance_id):

        connection = connector.getcon()
        dao = fullappliancedao.FullApplianceDAO(connection)

        appliance = dao.get(appliance_id)

        reply = hs_answer.Answer()
        if appliance is None:
            reply.set_status(_status.STATUS_GENERAL_ERROR)
            reply.add_content('appliance', {})
        else:
            reply.set_status(_status.STATUS_OK)
            reply.add_content('appliance', appliance.to_array())

        connection.close()
        return reply.to_array()
