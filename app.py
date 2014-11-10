#!homeshell/bin/python
__author__ = 'alisonbento'

from flask import Flask, jsonify
from flask_restful import Api

import configs
from src.res.homeshellres import *

app = Flask(__name__)
api = Api(app)

# Index
api.add_resource(IndexResource, '/')

# Session
api.add_resource(RequestTokenResource, '/access/')

# Appliances
api.add_resource(ApplianceListResource, '/appliances/')
api.add_resource(ApplianceResource, '/appliances/<int:appliance_id>/', endpoint='appliances')

# Services
api.add_resource(ApplianceListServicesResource, '/appliances/<int:appliance_id>/services/')
api.add_resource(ApplianceServiceResource, '/appliances/<int:appliance_id>/services/<int:service_id>/')

# Status
api.add_resource(ApplianceListStatusResource, '/appliances/<int:appliance_id>/status/')
api.add_resource(ApplianceStatusResource, '/appliances/<int:appliance_id>/status/<int:status_id>/')

if __name__ == '__main__':
    app.run(port=8080, debug=True)
