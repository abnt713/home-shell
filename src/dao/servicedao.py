__author__ = 'alisonbento'

import abstractdao
from src.entities.hsservice import HomeShellService


class ServiceDAO(abstractdao.AbstractDAO):

    def __init__(self, connection):
        abstractdao.AbstractDAO.__init__(self, connection, 'hs_appliance_services', 'service_id')

    def convert_row_to_object(self, entity_row):
        service = HomeShellService()
        service.id = entity_row['service_id']
        service.name = entity_row['service_trigger']

        return service
