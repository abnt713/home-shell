__author__ = 'alisonbento'

import basedao
from src.entities.hsparam import HomeShellParam


class ParamDAO(basedao.BaseDAO):

    def __init__(self, connection):
        basedao.BaseDAO.__init__(self, connection, 'hs_appliance_service_params', 'param_id')

    def convert_row_to_object(self, entity_row):
        param = HomeShellParam()
        param.id = entity_row['param_id']
        param.name = entity_row['param_key']

        return param