__author__ = 'alisonbento'

import sqlite3 as lite
import configs


def getcon():
    connection = lite.connect(configs.DATABASE)
    connection.row_factory = lite.Row
    return connection