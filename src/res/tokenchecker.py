__author__ = 'alisonbento'

import datetime
import connector
import configs
from src.dao.tokendao import TokenDAO


def check_token(token):

    connection = connector.getcon()
    tokendao = TokenDAO(connection)

    tokens = tokendao.select("token = ?", (token,))

    if len(tokens) > 0:
        token = tokens[0]

        current_time = datetime.datetime.now()
        valid_time = datetime.datetime.strptime(token.valid, configs.DATABASE_DATE_FORMAT)

        return current_time < valid_time

    return False