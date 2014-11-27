__author__ = 'alisonbento'

import abstractdao

import servicedao as hsservicedao
import paramdao as hsparamdao
import src.entities.hsfullservice as hsfullservice


class FullServiceDAO(abstractdao.AbstractDAO):

    def list(self, criteria=None, arguments=()):
        servicedao = hsservicedao.ServiceDAO(self.connection)
        paramdao = hsparamdao.ParamDAO(self.connection)

        all_services = servicedao.list(criteria, arguments)

        if len(all_services) <= 0:
            return all_services

        all_full_services = []
        for service in all_services:
            fullservice = hsfullservice.HomeShellFullService()
            fullservice.service = service
            fullservice.params = paramdao.list("service_id = ?", (service.id,))

            all_full_services.append(fullservice)

        return all_full_services

    def get(self, entity_id, criteria=None):
        fullservice = hsfullservice.HomeShellFullService()
        servicedao = hsservicedao.ServiceDAO(self.connection)
        fullservice.service= servicedao.get(entity_id, criteria)

        if fullservice.service is None:
            return None

        paramdao = hsparamdao.ParamDAO(self.connection)
        fullservice.params = paramdao.list("service_id = ?", (entity_id,))

        return fullservice

