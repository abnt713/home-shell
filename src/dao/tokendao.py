__author__ = 'alisonbento'

import abstractdao
from src.entities.token.hstoken import HomeShellToken


class TokenDAO(abstractdao.AbstractDAO):

    def __init__(self, connection):
        abstractdao.AbstractDAO.__init__(self, connection, 'hs_tokens', 'token_id')

    def insert(self, entity):
        cursor = self.connection.cursor()
        sql = "INSERT INTO " + self.table + " (user_id, token, created, valid) VALUES (?, ?, ?, ?)"

        entity_tuple = (
            entity.user_id,
            entity.token,
            entity.created,
            entity.valid
        )

        cursor.execute(sql, entity_tuple)

        return cursor.lastrowid

    def convert_row_to_object(self, entity_row):
        token = HomeShellToken()

        token.id = entity_row['token_id']
        token.token = entity_row['token']
        token.user_id = entity_row['user_id']
        token.created = entity_row['created']
        token.valid = entity_row['valid']

        return token

