__author__ = 'alisonbento'

import datetime

import configs
from src.dao.tokendao import TokenDAO


def check_token(token, connection):

    tokendao = TokenDAO(connection)

    tokens = tokendao.select("token = ?", (token,))

    if len(tokens) > 0:
        token = tokens[0]

        current_time = datetime.datetime.now()
        valid_time = datetime.datetime.strptime(token.valid, configs.DATABASE_DATE_FORMAT)

        if current_time > valid_time:
            return None
        else:
            newvalidtime = current_time + datetime.timedelta(minutes=configs.TOKEN_VALID_TIME)
            token.valid = newvalidtime.strftime(configs.DATABASE_DATE_FORMAT)
            tokendao.update(token)

            connection.commit()

            return token
    return None