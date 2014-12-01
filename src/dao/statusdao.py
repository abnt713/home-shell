__author__ = 'alisonbento'

import basedao
from src.entities.hsstatus import HomeShellStatus


class StatusDAO(basedao.BaseDAO):

    def __init__(self, connection):
        basedao.BaseDAO.__init__(self, connection, 'hs_appliance_status', 'status_id')

    def convert_row_to_object(self, entity_row):
        status = HomeShellStatus()

        status.id = entity_row['status_id']
        status.name = entity_row['status_key']
        status.value = entity_row['status_value']

        return status

    def update(self, entity):
        sql = "UPDATE " + self.table + " SET status_key = :key, status_value = :value WHERE status_id = :id"

        cursor = self.connection.cursor()

        values = {
            'key': entity.name,
            'value': entity.value,
            'id': entity.id
        }

        cursor.execute(sql, values)
        return

    def update_appliance_status(self, appjson, appliance_id):
        for status, value in appjson.items():
            print("try update status " + str(status) + " to value: " + str(value))
            basestatus = self.get_status_by_name(status, appliance_id)
            if basestatus is not None:
                print('updating ' + str(status))
                basestatus.value = value
                self.update(basestatus)

    def get_status_by_name(self, status_name, appliance_id):
        status_list = self.select('status_key = ? AND appliance_id = ?', (status_name, appliance_id))
        if len(status_list) <= 0:
            return None

        return status_list[0]
