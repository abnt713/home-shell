__author__ = 'alisonbento'

import flask_restful

import src.res.connector as connector
import src.dao.fullgroupdao as fullgroupdao
from src.answer.answer import Answer
import src.resstatus as _status


class ListGroupResource(flask_restful.Resource):

    def get(self):
        connection = connector.getcon()

        dao = fullgroupdao.FullGroupDAO(connection)
        all_groups = dao.list()

        reply_groups = []
        for group in all_groups:
            reply_groups.append(group.to_array())

        reply = Answer()
        reply.set_status(_status.STATUS_OK)
        reply.add_content('groups', reply_groups)

        return reply.to_array()


