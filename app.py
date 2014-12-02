#!venv/bin/python
__author__ = 'alisonbento'

import flask

from src.resources.appliances import *
from src.resources.common import *
from src.resources.extras import *
from src.resources.groups import *
from src.resources.services import *
from src.resources.status import *


app = flask.Flask(__name__)
api = flask_restful.Api(app)

# Index
api.add_resource(IndexResource, '/')

# Session
api.add_resource(RequestTokenResource, '/access/')

# Groups
api.add_resource(ListGroupResource, '/groups/')
api.add_resource(GroupResource, '/groups/<int:group_id>/')

# Appliances
api.add_resource(ApplianceListResource, '/appliances/')
api.add_resource(ApplianceResource, '/appliances/<int:appliance_id>/', endpoint='appliances')


# Services
api.add_resource(ListServicesResource, '/appliances/<int:appliance_id>/services/')
api.add_resource(ServiceResource, '/appliances/<int:appliance_id>/services/<service_id>/')

# Status
api.add_resource(ListStatusResource, '/appliances/<appliance_id>/status/')
# api.add_resource(StatusResource, '/appliances/connect/')
api.add_resource(StatusResource, '/appliances/<int:appliance_id>/status/<int:status_id>/')

# Extras
api.add_resource(ListExtrasResource, '/appliances/<int:appliance_id>/extras/')
api.add_resource(ExtraResource, '/appliances/<appliance_id>/extras/<extra_key>/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=configs.DEBUG_MODE)
    #app.run(port=8080, debug=configs.DEBUG_MODE)
