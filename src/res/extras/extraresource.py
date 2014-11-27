__author__ = 'alisonbento'

import time

import src.res.hsres as hsres

import src.resstatus as _status

from src.entities.hsextra import HomeShellExtra

from src.dao.appliancedao import ApplianceDAO
from src.dao.extradao import ExtraDAO

from flask import request


class ExtraResource(hsres.HomeShellResource):

    def get(self, appliance_id, extra_key):

        appliancedao = ApplianceDAO(self.get_dbc())

        if not appliance_id.isdigit():
            self.set_status(_status.STATUS_INVALID_REQUEST)
            return self.end()

        appliance = appliancedao.get(appliance_id)

        if appliance is None:
            self.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
            return self.end()

        extradao = ExtraDAO(self.get_dbc())
        all_extras = extradao.list('appliance_id = ? AND extra_key = ?', (appliance.id, extra_key))

        parsed_extras = []
        for extra in all_extras:
            parsed_extras.append(extra.to_array())

        self.set_status(_status.STATUS_OK)
        self.add_content('extras', parsed_extras)

        return self.end()

    def post(self, appliance_id, extra_key):
        appliancedao = ApplianceDAO(self.get_dbc())

        appliance_list = appliancedao.select('appliance_hash = ?', (appliance_id,))

        if len(appliance_list) <= 0:
            self.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
            return self.end()

        appliance = appliance_list[0]
        value = str(request.form.get('value'))
        date = str(request.form.get('date'))
        created = time.strftime('%Y-%m-%d %H:%M:%S')

        extradao = ExtraDAO(self.get_dbc())
        extra = HomeShellExtra(0, appliance.id, str(extra_key), value, date, created)

        result = extradao.insert(extra)

        if result:
            self.get_dbc().commit()
            self.set_status(_status.STATUS_OK)
        else:
            self.get_dbc().rollback()
            self.set_status(_status.STATUS_GENERAL_ERROR)

        return self.end()
