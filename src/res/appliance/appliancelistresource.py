__author__ = 'alisonbento'

import flask_restful

import src.base.connector as connector
import src.dao.fullappliancedao as appliancedao
import src.answer.answer
import src.resstatus as _status


class ApplianceListResource(flask_restful.Resource):

    def get(self):

        connection = connector.getcon()
        dao = appliancedao.FullApplianceDAO(connection)

        appliances = dao.list()
        reply = src.answer.answer.Answer()
        if len(appliances) > 0:
            reply.set_status(_status.STATUS_OK)
            all_appliances = []
            for appliance in appliances:
                all_appliances.append(appliance.to_array())

            reply.add_content('appliances', all_appliances)

        return reply.to_array()
