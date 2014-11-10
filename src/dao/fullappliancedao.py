__author__ = 'alisonbento'

import abstractdao

import appliancedao as hsappliancedao
import servicedao as hsservicedao
import statusdao as hsstatusdao
import src.entities.hsfullappliance as hsfullappliance


class FullApplianceDAO(abstractdao.AbstractDAO):

    def get(self, entity_id, criteria=None):
        fullappliance = hsfullappliance.HomeShellFullAppliance()
        appliancedao = hsappliancedao.ApplianceDAO(self.connection)
        fullappliance.appliance = appliancedao.get(entity_id, criteria)

        if fullappliance.appliance is None:
            return None

        servicedao = hsservicedao.ServiceDAO(self.connection)
        fullappliance.services = servicedao.list("appliance_id = ?", (entity_id,))

        statusdao = hsstatusdao.StatusDAO(self.connection)
        fullappliance.status = statusdao.list("appliance_id = ?", (entity_id,))

        return fullappliance