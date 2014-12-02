__author__ = 'alisonbento'

import hsres
import src.dao.fullgroupdao as fullgroupdao
import src.resstatus as _status


class GroupResource(hsres.HomeShellResource):

    def get(self, group_id):
        dao = fullgroupdao.FullGroupDAO(self.get_dbc())
        group = dao.get(group_id)

        self.set_status(_status.STATUS_OK)
        self.add_content('group', group.to_array())

        return self.end()


class ListGroupResource(hsres.HomeShellResource):

    def get(self):
        dao = fullgroupdao.FullGroupDAO(self.get_dbc())
        all_groups = dao.list()

        reply_groups = []
        for group in all_groups:
            reply_groups.append(group.to_array())

        self.set_status(_status.STATUS_OK)
        self.add_content('groups', reply_groups)

        return self.end()