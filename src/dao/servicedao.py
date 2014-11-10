__author__ = 'alisonbento'

import basedao
from src.entities.hsservice import HomeShellService


class ServiceDAO(basedao.BaseDAO):

    def __init__(self, connection):
        basedao.BaseDAO.__init__(self, connection, 'hs_appliance_services', 'service_id')

    def convert_row_to_object(self, entity_row):
        service = HomeShellService()
        service.id = entity_row['service_id']
        service.name = entity_row['service_trigger']

        return service
