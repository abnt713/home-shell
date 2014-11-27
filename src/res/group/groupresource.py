__author__ = 'alisonbento'

import flask_restful

import src.base.connector as connector
import src.dao.fullgroupdao as fullgroupdao
import src.resstatus as _status
from src.answer.answer import Answer


class GroupResource(flask_restful.Resource):

    def get(self, group_id):
        connection = connector.getcon()

        dao = fullgroupdao.FullGroupDAO(connection)
        group = dao.get(group_id)


        reply = Answer()
        reply.set_status(_status.STATUS_OK)
        reply.add_content('group', group.to_array())

        return reply.to_array()

