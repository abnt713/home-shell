__author__ = 'alisonbnt'

import requests

import src.resstatus as _status

from src.appliances.statusupdater import StatusUpdater
from src.dao.appliancedao import ApplianceDAO
from src.dao.servicedao import ServiceDAO
from src.dao.paramdao import ParamDAO


def call_service(resource, appliance_id, service_id, form, method="get"):
    servicedao = ServiceDAO(resource.get_dbc())

    if service_id.isdigit():
        service = servicedao.get(service_id, "appliance_id = " + str(appliance_id))
    else:
        services = servicedao.select("appliance_id = ? AND service_trigger = ?", (appliance_id, service_id))
        if len(services) > 0:
            service = services[0]
        else:
            service = None

    if service is None:
        resource.set_status(_status.STATUS_APPLIANCE_NOT_FOUND)
        return resource.end()
    else:
        paramdao = ParamDAO(resource.get_dbc())
        params = paramdao.select("service_id = ?", (service.id,))

        all_params_with_values = []
        for param in params:
            p_value = form[param.name]
            if p_value is not None:
                all_params_with_values.append(param.name + '=' + p_value)

        if len(all_params_with_values) > 0:
            param_string = '&'.join(all_params_with_values)
            param_string = '?' + param_string
        else:
            param_string = ''

        appliancedao = ApplianceDAO(resource.get_dbc())
        appliance = appliancedao.get(appliance_id)
        address = 'http://' + appliance.address + '/services/' + service.name + param_string

        try:
            if method == 'get':
                r = requests.get(address)
            elif method == 'post':
                r = requests.get(address)

            if r.status_code == '404':
                resource.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)
            elif r.status_code:
                print(r.text)
                # Update status
                updater = StatusUpdater(resource.get_dbc())
                appjson = r.json()
                fullappliance = updater.updateStatus(appliance, appjson)
                resource.set_status(_status.STATUS_OK)
                resource.add_content('appliance', fullappliance.to_array())

        except requests.ConnectionError:
            resource.set_status(_status.STATUS_APPLIANCE_UNREACHABLE)
            resource.get_dbc().rollback()

        return resource.end()
