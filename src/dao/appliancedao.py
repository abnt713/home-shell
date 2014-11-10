__author__ = 'alisonbento'

import abstractdao
from src.entities.hsappliance import HomeShellAppliance


class ApplianceDAO(abstractdao.AbstractDAO):

    def __init__(self, connection):
        abstractdao.AbstractDAO.__init__(self, connection, 'hs_appliances', 'appliance_id')

    def convert_row_to_object(self, entity_row):
        appliance = HomeShellAppliance()

        appliance.id = entity_row['appliance_id']
        appliance.type = entity_row['type']
        appliance.name = entity_row['type']
        appliance.key = None
        appliance.address = entity_row['address']

        return appliance