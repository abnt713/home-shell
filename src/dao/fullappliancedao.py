__author__ = 'alisonbento'

import abstractdao

import appliancedao as hsappliancedao
import servicedao as hsservicedao
import statusdao as hsstatusdao
import src.entities.hsfullappliance as hsfullappliance


class FullApplianceDAO(abstractdao.AbstractDAO):

    def list(self, criteria=None, arguments=()):
        appliancedao = hsappliancedao.ApplianceDAO(self.connection)
        servicedao = hsservicedao.ServiceDAO(self.connection)
        statusdao = hsstatusdao.StatusDAO(self.connection)

        all_appliances = appliancedao.list(criteria, arguments)

        if len(all_appliances) <= 0:
            return all_appliances

        all_full_appliances = []
        for appliance in all_appliances:
            fullappliance = hsfullappliance.HomeShellFullAppliance()
            fullappliance.appliance = appliance
            fullappliance.services = servicedao.list("appliance_id = ?", (appliance.id,))
            fullappliance.status = statusdao.list("appliance_id = ?", (appliance.id,))

            all_full_appliances.append(fullappliance)

        return all_full_appliances


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