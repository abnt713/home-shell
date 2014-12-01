# encoding: utf-8
__author__ = 'paulobrizolara'

import datetime
import configs
from src.dao.statusdao import StatusDAO
from src.dao.fullappliancedao import FullApplianceDAO
from src.dao.appliancedao import ApplianceDAO

class StatusUpdater:
    def __init__(self, dbc):
        self.dbc = dbc
    def get_dbc(self):
        return self.dbc

    def updateStatus(self, appliance, appjson):
        statusdao = StatusDAO(self.get_dbc())
        appliancedao = ApplianceDAO(self.get_dbc())
        fullappliancedao = FullApplianceDAO(self.get_dbc())

        if 'status' in appjson:
            statusjson = appjson['status']
        else:
            statusjson = appjson

        statusdao.update_appliance_status(statusjson, appliance.id)
        
        current_time = datetime.datetime.now()
        appliance.modified = current_time.strftime(configs.DATABASE_DATE_FORMAT)
        appliancedao.update(appliance)
        self.get_dbc().commit()
        fullappliance = fullappliancedao.get(appliance.id)
        return fullappliance

