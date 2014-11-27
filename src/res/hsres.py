__author__ = 'alisonbento'

import flask_restful
import src.base.connector as connector
import src.answer.answer as hsanswer


class DbConnectedResource(flask_restful.Resource):

    def __init__(self):
        flask_restful.Resource.__init__(self)
        self.dbc = None

    def init_dbc(self):
        self.dbc = connector.getcon()

    def get_dbc(self):
        if self.dbc is None:
            self.init_dbc()

        return self.dbc

    def end(self):
        if self.dbc is not None:
            self.dbc.close()


class ReplyResource(DbConnectedResource):

    def __init__(self):
        DbConnectedResource.__init__(self)
        self.hs_reply = hsanswer.Answer()

    def set_status(self, hs_status):
        self.hs_reply.set_status(hs_status)

    def add_content(self, index, content):
        self.hs_reply.add_content(index, content)

    def end(self):
        super(ReplyResource, self).end()
        return self.hs_reply.to_array()


class HomeShellResource(ReplyResource):

    def __init__(self):
        super(HomeShellResource, self).__init__()