__author__ = 'alisonbento'

import abstractdao
import src.entities.hsfullgroup as hsfullgroup
import fullappliancedao as hsappliancedao
import groupdao as hsgroupdao


class FullGroupDAO(abstractdao.AbstractDAO):

    def __init__(self, connection):
        abstractdao.AbstractDAO.__init__(self, connection)

    def list(self, criteria=None, arguments=()):
        groupdao = hsgroupdao.GroupDAO(self.connection)

        all_groups = groupdao.list(criteria, arguments)

        if len(all_groups) <= 0:
            return all_groups

        fullappliancedao = hsappliancedao.FullApplianceDAO(self.connection)
        all_full_groups = []
        for group in all_groups:
            fullgroup = hsfullgroup.HomeShellFullGroup()
            fullgroup.group = group
            subquery = "appliance_id IN (SELECT appliance_id FROM hs_group_appliances WHERE group_id = ?)"
            all_appliances = fullappliancedao.list(subquery, (group.id,))
            fullgroup.appliances = all_appliances

            all_full_groups.append(fullgroup)

        return all_full_groups

    def get(self, entity_id, criteria=None, arguments=()):
        fullgroup = hsfullgroup.HomeShellFullGroup()
        groupdao = hsgroupdao.GroupDAO(self.connection)

        fullgroup.group = groupdao.get(entity_id, criteria, arguments)

        if fullgroup.group is None:
            return None

        fullappliancedao = hsappliancedao.FullApplianceDAO(self.connection)
        subquery = "appliance_id IN (SELECT appliance_id FROM hs_group_appliances WHERE group_id = ?)"
        all_appliances = fullappliancedao.list(subquery, (fullgroup.group.id,))
        fullgroup.appliances = all_appliances

        return fullgroup
