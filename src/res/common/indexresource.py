__author__ = 'alisonbento'

import flask
import flask_restful

import src.res.connector as connector
import src.answer.answer as hsanswer
import src.res.tokenchecker as tokenchecker
import src.resstatus as _status

import configs


class IndexResource(flask_restful.Resource):

    def get(self):
        connection = connector.getcon()
        reply = hsanswer.Answer()

        valid_token = tokenchecker.check_token(flask_restful.request.args.get('authtoken'), connection)
        if valid_token is None:
            reply.set_status(_status.STATUS_TOKEN_INVALID)
            return reply.to_array()

        reply.set_status(1)
        reply.add_content('version', configs.VERSION)
        reply.add_content('user', valid_token.user_id)

        connection.close()
        return reply.to_array()