#!homeshell/bin/python
__author__ = 'alisonbento'

import flask
import flask_restful

from src.res.common.indexresource import IndexResource
from src.res.common.requesttokenresource import RequestTokenResource
from src.res.appliance.appliancelistresource import ApplianceListResource
from src.res.appliance.applianceresource import ApplianceResource
from src.res.appliance.service.listservicesresource import ListServicesResource
from src.res.appliance.service.serviceresource import ServiceResource
from src.res.appliance.status.liststatusresource import ListStatusResource
from src.res.appliance.status.statusresource import StatusResource


app = flask.Flask(__name__)
api = flask_restful.Api(app)

# Index
api.add_resource(IndexResource, '/')

# Session
api.add_resource(RequestTokenResource, '/access/')

# Appliances
api.add_resource(ApplianceListResource, '/appliances/')
api.add_resource(ApplianceResource, '/appliances/<int:appliance_id>/', endpoint='appliances')

# Services
api.add_resource(ListServicesResource, '/appliances/<int:appliance_id>/services/')
api.add_resource(ServiceResource, '/appliances/<int:appliance_id>/services/<service_id>/')

# Status
api.add_resource(ListStatusResource, '/appliances/<int:appliance_id>/status/')
api.add_resource(StatusResource, '/appliances/<int:appliance_id>/status/<int:status_id>/')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
