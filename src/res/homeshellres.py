__author__ = 'alisonbento'

import flask_restful
import flask

import hashlib
import uuid
import datetime

import configs
import src.hsstatus as _status
import connector
import src.res.tokenchecker as tokenchecker

from src.dao.appliancedao import ApplianceDAO
from src.dao.servicedao import ServiceDAO
from src.dao.statusdao import StatusDAO
from src.dao.userdao import UserDAO
from src.dao.tokendao import TokenDAO
from src.entities.token.hstoken import HomeShellToken

from src.answer.answer import Answer


# Index
class IndexResource(flask_restful.Resource):

    def get(self):
        reply = Answer()

        valid_token = tokenchecker.check_token(flask_restful.request.args.get('authtoken'))
        if not valid_token:
            reply.set_status(_status.STATUS_TOKEN_INVALID)
            return flask.jsonify(reply.to_array())

        reply.set_status(1)
        reply.add_content('version', configs.VERSION)

        return flask.jsonify(reply.to_array())


# Token request
class RequestTokenResource(flask_restful.Resource):

    def get(self):
        reply = Answer()

        reply.set_status(_status.STATUS_INVALID_REQUEST)
        return flask.jsonify(reply.to_array())

    def post(self):
        username = flask_restful.request.form.get('username')
        password = flask_restful.request.form.get('password')

        reply = Answer()
        if username is None or password is None:
            reply.set_status(_status.STATUS_INCORRECT_ARGS)
            return flask.jsonify(reply.to_array())

        connection = connector.getcon()
        dao = UserDAO(connection)

        hasher = hashlib.sha1()
        hasher.update(password)

        hashed_password = hasher.hexdigest()
        matched_users = dao.select("username = ? AND password = ?", (username, hashed_password))

        if len(matched_users) <= 0:
            reply.set_status(_status.STATUS_LOGIN_FAIL)
        else:
            user = matched_users[0]
            token = HomeShellToken()

            tokenvalue = uuid.uuid4()
            hashed_token = hashlib.sha1()
            hashed_token.update(tokenvalue.get_hex())

            current_time = datetime.datetime.now()
            valid_time = current_time + datetime.timedelta(minutes=configs.TOKEN_VALID_TIME)

            token.user_id = user.id
            token.token = hashed_token.hexdigest()
            token.created = current_time.strftime(configs.DATABASE_DATE_FORMAT)
            token.valid = valid_time.strftime(configs.DATABASE_DATE_FORMAT)

            tokendao = TokenDAO(connection)
            token.id = tokendao.insert(token)

            if token.id > 0:
                connection.commit()
                reply.set_status(_status.STATUS_TOKEN_SUCCESS)
                reply.add_content('token', {'key': token.token, 'valid': token.valid})
            else:
                connection.rollback()
                reply.set_status(_status.STATUS_TOKEN_FAILED)

        connection.close()
        return flask.jsonify(reply.to_array())


# Appliances
class ApplianceListResource(flask_restful.Resource):

    def get(self):

        connection = connector.getcon()
        dao = ApplianceDAO(connection)

        appliances = dao.list()
        reply = Answer()
        if len(appliances) > 0:
            reply.set_status(1)
            all_appliances = []
            for appliance in appliances:
                all_appliances.append(appliance.to_array())

            reply.add_content('appliances', all_appliances)

        return flask.jsonify(reply.to_array())


class ApplianceResource(flask_restful.Resource):

    def get(self, appliance_id):

        connection = connector.getcon()
        dao = ApplianceDAO(connection)

        appliance = dao.get(appliance_id)

        reply = Answer()
        if appliance is None:
            reply.set_status(_status.STATUS_GENERAL_ERROR)
            reply.add_content('appliance', {})
        else:
            reply.set_status(_status.STATUS_OK)
            reply.add_content('appliance', appliance.to_array())

        connection.close()
        return flask.jsonify(reply.to_array())


# Services
class ApplianceListServicesResource(flask_restful.Resource):
    def get(self, appliance_id):

        connection = connector.getcon()
        dao = ServiceDAO(connection)

        services = dao.list("appliance_id = ?", (appliance_id,))

        reply = Answer()

        if len(services) > 0:
            reply.set_status(_status.STATUS_OK)
            all_services = []
            for service in services:
                all_services.append(service.to_array())

            reply.add_content('services', all_services)

        else:
            reply.set_status(_status.STATUS_GENERAL_ERROR)

        connection.close()
        return flask.jsonify(reply.to_array())


class ApplianceServiceResource(flask_restful.Resource):

    def get(self, appliance_id, service_id):

        connection = connector.getcon()
        dao = ServiceDAO(connection)

        service = dao.get(service_id, "appliance_id = " + str(appliance_id))

        reply = Answer()
        if service is None:
            reply.set_status(_status.STATUS_GENERAL_ERROR)
        else:
            reply.set_status(_status.STATUS_OK)
            reply.add_content('service', service.to_array())

        connection.close()
        return flask.jsonify(reply.to_array())


# Status
class ApplianceListStatusResource(flask_restful.Resource):

    def get(self, appliance_id):
        connection = connector.getcon()
        dao = StatusDAO(connection)

        status = dao.list("appliance_id = " + str(appliance_id))

        reply = Answer()

        if len(status) > 0:
            reply.set_status(_status.STATUS_OK)
            all_services = []
            for single_status in status:
                all_services.append(single_status.to_array())

            reply.add_content('status', all_services)

        else:
            reply.set_status(_status.STATUS_GENERAL_ERROR)

        connection.close()
        return flask.jsonify(reply.to_array())


class ApplianceStatusResource(flask_restful.Resource):

    def get(self, appliance_id, status_id):
        connection = connector.getcon()
        dao = StatusDAO(connection)

        status = dao.get(status_id, "appliance_id = " + str(appliance_id))

        reply = Answer()
        if status is None:
            reply.set_status(_status.STATUS_GENERAL_ERROR)
        else:
            reply.set_status(_status.STATUS_OK)
            reply.add_content('status', status.to_array())

        connection.close()
        return flask.jsonify(reply.to_array())