__author__ = 'alisonbento'

import flask_restful
import hashlib
import uuid
import datetime

import src.resstatus as _status
import configs
import src.resources.hsres as hsres
import src.base.tokenchecker as tokenchecker
import src.entities.token.hstoken as hstoken
import src.dao.tokendao as hstokendao

import src.dao.userdao as userdao


class IndexResource(hsres.HomeShellResource):

    def get(self):
        token = flask_restful.request.headers.get(configs.HEADER_AUTH_INDEX)
        valid_token = tokenchecker.check_token(token, self.get_dbc())
        if valid_token is None:
            self.set_status(_status.STATUS_TOKEN_INVALID)
            return self.end()

        self.set_status(1)
        self.add_content('version', configs.VERSION)
        self.add_content('user', valid_token.user_id)

        return self.end()


class RequestTokenResource(hsres.HomeShellResource):

    def get(self):
        token = flask_restful.request.headers.get(configs.HEADER_AUTH_INDEX)
        valid_token = tokenchecker.check_token(token, self.get_dbc())
        if valid_token is None:
            self.set_status(_status.STATUS_TOKEN_INVALID)
            return self.end()

        self.set_status(_status.STATUS_INVALID_REQUEST)
        return self.end()

    def post(self):
        username = flask_restful.request.form.get('username')
        password = flask_restful.request.form.get('password')

        if username is None or password is None:
            self.set_status(_status.STATUS_INCORRECT_ARGS)
            return self.end()

        dao = userdao.UserDAO(self.get_dbc())

        hasher = hashlib.sha1()
        hasher.update(password)

        hashed_password = hasher.hexdigest()
        matched_users = dao.select("username = ? AND password = ?", (username, hashed_password))

        if len(matched_users) <= 0:
            self.set_status(_status.STATUS_LOGIN_FAIL)
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

            tokendao = hstokendao.TokenDAO(self.get_dbc())
            token.id = tokendao.insert(token)

            if token.id > 0:
                self.get_dbc().commit()
                self.set_status(_status.STATUS_TOKEN_SUCCESS)
                self.add_content('token', {'key': token.token, 'valid': token.valid})
            else:
                self.get_dbc().rollback()
                self.set_status(_status.STATUS_TOKEN_FAILED)

        return self.end()
