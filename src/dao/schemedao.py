__author__ = 'alisonbnt'

import basedao


class SchemeDAO(basedao.BaseDAO):

    def __init__(self, connection):
        basedao.BaseDAO.__init__(self, connection, 'hs_schemes', 'scheme_id')