__author__ = 'alisonbento'

import abstractdao


class BaseDAO(abstractdao.AbstractDAO):

    def __init__(self, connection, table, primary_key):
        abstractdao.AbstractDAO.__init__(self, connection)
        self.table = table
        self.primary_key = primary_key

    def list(self, criteria=None, arguments=()):
        cursor = self.connection.cursor()
        sql = "SELECT * FROM " + str(self.table)

        if criteria is not None:
            sql += ' WHERE ' + str(criteria)
            cursor.execute(sql, arguments)
        else:
            cursor.execute(sql)

        entity_rows = cursor.fetchall()
        all_entities = []

        if len(entity_rows) <= 0:
            return all_entities

        for entity_row in entity_rows:
            all_entities.append(self.convert_row_to_object(entity_row))

        return all_entities

    def get(self, entity_id, criteria=None, arguments=()):
        cursor = self.connection.cursor()

        sql = "SELECT * FROM " + str(self.table) + " WHERE " + str(self.primary_key) + " = " + str(entity_id)

        if criteria is not None:
            sql += " AND " + str(criteria)
            cursor.execute(sql, arguments)
        else:
            cursor.execute(sql)

        entity_row = cursor.fetchone()
        if entity_row is None:
            return None
        return self.convert_row_to_object(entity_row)

    def select(self, criteria=None, arguments=()):
        cursor = self.connection.cursor()

        sql = "SELECT * FROM " + str(self.table)

        if criteria is not None:
            sql += " WHERE " + str(criteria)
            cursor.execute(sql, arguments)
        else:
            cursor.execute(sql)

        entity_rows = cursor.fetchall()
        all_entities = []

        if len(entity_rows) <= 0:
            return all_entities

        for entity_row in entity_rows:
            all_entities.append(self.convert_row_to_object(entity_row))

        return all_entities

    def delete(self, entity_id):
        cursor = self.connection.cursor()
        sql = "DELETE FROM " + str(self.table) + " WHERE " + str(self.primary_key) + " = ?"
        return cursor.execute(sql, entity_id)

    # def insert(self, entity):
    #     pass
    #
    # def update(self, entity):
    #     pass
    #
    # def convert_row_to_object(self, entity_row):
    #     pass
