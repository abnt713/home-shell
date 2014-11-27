__author__ = 'alisonbento'

import src.res.hsres as hsres

import src.resstatus as _status

from src.dao.extradao import ExtraDAO
from src.dao.appliancedao import ApplianceDAO


class ListExtrasResource(hsres.HomeShellResource):

    def get(self, appliance_id):
        appliancedao = ApplianceDAO(self.get_dbc())
        appliance = appliancedao.get(appliance_id)

        if appliance is None:
            self.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
            return self.end()

        extradao = ExtraDAO(self.get_dbc())
        all_extras = extradao.list('appliance_id = ?', (appliance.id,))

        parsed_extras = []
        for extra in all_extras:
            parsed_extras.append(extra.to_array())

        self.set_status(_status.STATUS_OK)
        self.add_content('extras', parsed_extras)

        return self.end()