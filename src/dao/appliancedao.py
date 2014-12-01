__author__ = 'alisonbento'

import basedao
from src.entities.hsappliance import HomeShellAppliance
import datetime
import configs

class ApplianceDAO(basedao.BaseDAO):

    def __init__(self, connection):
        basedao.BaseDAO.__init__(self, connection, 'hs_appliances', 'appliance_id')

    def convert_row_to_object(self, entity_row):
        appliance = HomeShellAppliance()

        appliance.id = entity_row['appliance_id']
        appliance.package = entity_row['package']
        appliance.type = entity_row['type']
        appliance.name = entity_row['type']
        appliance.key = None
        appliance.address = entity_row['address']
        appliance.hash = entity_row['appliance_hash']
        appliance.modified = entity_row['modified']
        appliance.modified_datetime = datetime.datetime.strptime(appliance.modified, configs.DATABASE_DATE_FORMAT)

        return appliance

    def update(self, entity):
        cursor = self.connection.cursor()

        sql = "UPDATE " + self.table + " SET modified = ? WHERE appliance_id = ?"
        cursor.execute(sql, (entity.modified, entity.id))
