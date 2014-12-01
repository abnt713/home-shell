__author__ = 'alisonbento'

import requests
import datetime

import configs
import src.res.hsres as hsres

import src.resstatus as _status

from src.dao.fullappliancedao import FullApplianceDAO
from src.dao.appliancedao import ApplianceDAO
from src.dao.servicedao import ServiceDAO
from src.dao.paramdao import ParamDAO
from src.dao.statusdao import StatusDAO

from flask import request


class ServiceResource(hsres.HomeShellResource):

    def get(self, appliance_id, service_id):

        dao = ServiceDAO(self.get_dbc())

        if service_id.isdigit():
            service = dao.get(service_id, "appliance_id = " + str(appliance_id))
        else:
            services = dao.select("appliance_id = ? AND service_trigger = ?", (appliance_id, service_id))
            if len(services) > 0:
                service = services[0]
            else:
                service = None

        if service is None:
            self.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
            return self.end()

        self.set_status(_status.STATUS_OK)
        self.add_content('service', service.to_array())

        return self.end()

    def post(self, appliance_id, service_id):
        appliancedao = ApplianceDAO(self.get_dbc())
        fullappliancedao = FullApplianceDAO(self.get_dbc())
        servicedao = ServiceDAO(self.get_dbc())

        if service_id.isdigit():
            service = servicedao.get(service_id, "appliance_id = " + str(appliance_id))
        else:
            services = servicedao.select("appliance_id = ? AND service_trigger = ?", (appliance_id, service_id))
            if len(services) > 0:
                service = services[0]
            else:
                service = None

        if service is None:
            self.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
            return self.end()
        else:
            paramdao = ParamDAO(self.get_dbc())
            params = paramdao.select("service_id = ?", (service.id,))

            all_params_with_values = []
            for param in params:
                p_value = request.form[param.name]
                if p_value is not None:
                    all_params_with_values.append(param.name + '=' + p_value)

            if len(all_params_with_values) > 0:
                param_string = '&'.join(all_params_with_values)
                param_string = '?' + param_string
            else:
                param_string = ''

            appliance = appliancedao.get(appliance_id)
            current_time = datetime.datetime.now()
            # address = 'http://' + appliance.address + '/services/' + service.name + '/' + param_string
            address = 'http://' + appliance.address + '/services/' + service.name + param_string

            try:
                r = requests.get(address)

                if r.status_code == '404':
                    self.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)
                elif r.status_code:

                    # Update status
                    print(r.text)
                    appjson = r.json()
                    statusdao = StatusDAO(self.get_dbc())

                    if 'status' in appjson:
                        statusjson = appjson['status']
                    else:
                        statusjson = appjson

                    statusdao.update_appliance_status(statusjson, appliance_id)
                    appliance.modified = current_time.strftime(configs.DATABASE_DATE_FORMAT)
                    appliancedao.update(appliance)
                    self.get_dbc().commit()
                    fullappliance = fullappliancedao.get(appliance_id)
                    self.set_status(_status.STATUS_OK)
                    self.add_content('appliance', fullappliance.to_array())

            except requests.ConnectionError:
                self.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)
                self.get_dbc().rollback()

        return self.end()
