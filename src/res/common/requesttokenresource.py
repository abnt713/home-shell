__author__ = 'alisonbento'

import flask
import flask_restful
import hashlib
import uuid
import datetime

import src.answer.answer
import src.hsstatus as _status
import src.res.connector as connector

import src.dao.userdao as userdao
import src.dao.tokendao as hstokendao

import src.entities.token.hstoken as hstoken

import configs


class RequestTokenResource(flask_restful.Resource):

    def get(self):
        reply = src.answer.answer.Answer()

        reply.set_status(_status.STATUS_INVALID_REQUEST)
        return flask.jsonify(reply.to_array())

    def post(self):
        username = flask_restful.request.form.get('username')
        password = flask_restful.request.form.get('password')

        reply = src.answer.answer.Answer()
        if username is None or password is None:
            reply.set_status(_status.STATUS_INCORRECT_ARGS)
            return flask.jsonify(reply.to_array())

        connection = connector.getcon()
        dao = userdao.UserDAO(connection)

        hasher = hashlib.sha1()
        hasher.update(password)

        hashed_password = hasher.hexdigest()
        matched_users = dao.select("username = ? AND password = ?", (username, hashed_password))

        if len(matched_users) <= 0:
            reply.set_status(_status.STATUS_LOGIN_FAIL)
        else:
            user = matched_users[0]
            token = hstoken.HomeShellToken()

            tokenvalue = uuid.uuid4()
            hashed_token = hashlib.sha1()
            hashed_token.update(tokenvalue.get_hex())

            current_time = datetime.datetime.now()
            valid_time = current_time + datetime.timedelta(minutes=configs.TOKEN_VALID_TIME)

            token.user_id = user.id
            token.token = hashed_token.hexdigest()
            token.created = current_time.strftime(configs.DATABASE_DATE_FORMAT)
            token.valid = valid_time.strftime(configs.DATABASE_DATE_FORMAT)

            tokendao = hstokendao.TokenDAO(connection)
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
