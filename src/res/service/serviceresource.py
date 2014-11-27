__author__ = 'alisonbento'

import requests

import src.res.hsres as hsres

import src.resstatus as _status
import src.base.connector as connector

from src.dao.appliancedao import ApplianceDAO
from src.dao.servicedao import ServiceDAO
from src.dao.paramdao import ParamDAO

from src.answer.answer import Answer

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
        connection = connector.getcon()
        appliancedao = ApplianceDAO(connection)
        servicedao = ServiceDAO(connection)

        if service_id.isdigit():
            service = servicedao.get(service_id, "appliance_id = " + str(appliance_id))
        else:
            services = servicedao.select("appliance_id = ? AND service_trigger = ?", (appliance_id, service_id))
            if len(services) > 0:
                service = services[0]
            else:
                service = None

        reply = Answer()
        if service is None:
            reply.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
            return
        else:
            paramdao = ParamDAO(connection)
            params = paramdao.select("service_id = ?", (service.id,))

            all_params_with_values = []
            for param in params:
                p_value = request.form[param.name]
                if p_value is not None:
                    print(param.name)
                    all_params_with_values.append(param.name + '=' + p_value)

            if len(all_params_with_values) > 0:
                param_string = '&'.join(all_params_with_values)
            else:
                param_string = ''


            appliance = appliancedao.get(appliance_id)
            address = 'http://' + appliance.address + '/services/' + service.name + '/?' + param_string
            print(address)

            try:
                r = requests.get(address)

                if r.status_code == '404':
                    reply.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)
                else:
                    reply.set_status(_status.STATUS_OK)
                    reply.add_content('service', service.to_array())

            except requests.ConnectionError:
                reply.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)

        connection.close()
        return reply.to_array()
