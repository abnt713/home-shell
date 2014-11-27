__author__ = 'alisonbento'

import basedao
from src.entities.hsextra import HomeShellExtra


class ExtraDAO(basedao.BaseDAO):

    def __init__(self, connection):
        basedao.BaseDAO.__init__(self, connection, 'hs_appliance_extras', 'extra_id')

    def convert_row_to_object(self, entity_row):
        extra = HomeShellExtra()
        extra.id = entity_row['extra_id']
        extra.extra_key = entity_row['extra_key']
        extra.extra_value = entity_row['extra_value']
        extra.extra_date = entity_row['extra_date']
        extra.created = entity_row['created']

        return extra

    def insert(self, entity):
        cursor = self.connection.cursor()
        sql = "INSERT INTO " + self.table + "(appliance_id, extra_key, extra_value, extra_date, created) VALUES "
        sql += "(:appliance_id, :extra_key, :extra_value, :extra_date, :created)"

        values = {
            'appliance_id': entity.appliance_id,
            'extra_key': entity.extra_key,
            'extra_value': entity.extra_value,
            'extra_date': entity.extra_date,
            'created': entity.created
        }

        print(values)

        cursor.execute(sql, values)
        entity.id = cursor.lastrowid

        print(entity.id)

        return entity.id is not None and entity.id > 0