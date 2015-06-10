__author__ = 'alisonbento'

import flask_restful
from flask_restful import reqparse
import hsres
from src.dao.appliancedao import ApplianceDAO
import src.resstatus as _status

from src.scheme_loader import SchemeLoader
from src.lib.service_caller import call_service


class EventResource(hsres.HomeShellResource):

    def options(self, appliance_id):
        return {'Allow': 'POST,PUT'}, 200, \
        {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type, Accept',
            'Access-Control-Allow-Methods': 'POST,GET,PUT'
        }

    def post(self, appliance_id):
        parser = reqparse.RequestParser()
        parser.add_argument('control_id', type=str)
        parser.add_argument('value', type=str)
        parser.add_argument('callback_key', type=str)
        args = parser.parse_args()

        # Preciso da appliance e seu scheme
        dao = ApplianceDAO(self.get_dbc())
        appliance = dao.get(appliance_id)
        appliance_package = appliance.package
        loader = SchemeLoader()
        real_package = appliance_package + '.' + appliance.type
        scheme = loader.get_scheme(real_package)
        # Em seguida preciso achar o control que foi modificado
        control_id = args['control_id']
        control = None
        for single_control in scheme['controls']:
            if single_control['id'] == control_id:
                control = single_control
                break

        # Por fim, devo verificar o callback associado ao novo estado do control
        callback_key = args['callback_key']
        callback = control['event-callbacks'][callback_key]

        if 'param' in callback:
            if 'value' not in args:
                self.set_status(_status.STATUS_SERVICE_REQUIRE_PARAMETER)
                return self.end()
            value = args['value']
            form = {callback['param']: value}
        else:
            form = {}

        # Executar os servicos definidos
        return call_service(self, appliance_id, callback['service'], form)
