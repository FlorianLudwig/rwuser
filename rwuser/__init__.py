"""An example using as many different features of rueckenwind as possible

"""
import os
import json

import pkg_resources

import tornado.web
from rw import gen
from rw import scope
import rw.testing
import rw.http
import rw.httpbase

from . import model

root = rw.http.Module('rwlogin')


@root.get('/')
def login_page():
    root.render_template('login.html')


plugin = rw.plugin.Plugin(__name__)


class UserService(object):
    @gen.coroutine
    @scope.inject
    def current(self, handler):
        rwuser = handler.get_secure_cookie('rwuser')
        if rwuser:
            rwuser = yield model.User.by_id(rwuser)
        raise gen.Return(rwuser)

    @gen.coroutine
    @scope.inject
    def set_current(self, user, handler, app):
        cfg = app.settings.get('rwuser', {})
        expires = cfg.get('session_time_h', 24)
        handler.set_secure_cookie('rwuser', str(user['_id']), expires_days=expires/24.)

    @gen.coroutine
    @scope.inject
    def login(self, handler):
        email = handler.get_argument('email')
        password = handler.get_argument('password')
        user = yield model.User.find_one({'email': email})
        if user and user.check_password(password):
            self.set_current(user)
            raise gen.Return(user)

    @gen.coroutine
    @scope.inject
    def register(self, handler):
        email = handler.get_argument('email')
        password = handler.get_argument('password')
        user = model.User()
        user.email = email
        user.set_password(password)
        yield user.insert()
        raise gen.Return(user)

@plugin.init
def init(scope, app):
    scope.subscope('services')['user'] = UserService()