__author__ = 'alisonbento'

import flask
import flask_restful
import src.res.connector as connector

import src.dao.appliancedao as appliancedao
import src.answer.answer


class ApplianceListResource(flask_restful.Resource):

    def get(self):

        connection = connector.getcon()
        dao = appliancedao.ApplianceDAO(connection)

        appliances = dao.list()
        reply = src.answer.answer.Answer()
        if len(appliances) > 0:
            reply.set_status(1)
            all_appliances = []
            for appliance in appliances:
                all_appliances.append(appliance.to_array())

            reply.add_content('appliances', all_appliances)

        return flask.jsonify(reply.to_array())
