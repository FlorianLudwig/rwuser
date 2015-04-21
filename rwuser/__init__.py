"""An example using as many different features of rueckenwind as possible

"""
import tornado.web
import perm
import rw.testing
import rw.http
import rw.httpbase
import rw.scope
from rw import gen

from . import model

root = rw.http.Module('rwlogin')


@root.get('/')
def login_page():
    root.render_template('login.html')


plugin = rw.plugin.Plugin(__name__)


class UserService(object):
    @gen.coroutine
    @rw.scope.inject
    def current(self, handler):
        rwuser = handler.get_secure_cookie('rwuser')
        if rwuser:
            rwuser = yield model.User.by_id(rwuser)
        if rwuser is None:
            rwuser = perm.Anonymous()
        raise gen.Return(rwuser)

    @gen.coroutine
    @rw.scope.inject
    def set_current(self, user, handler, app):
        cfg = app.settings.get('rwuser', {})
        expires = cfg.get('session_time_h', 24)
        handler.set_secure_cookie('rwuser', str(user['_id']), expires_days=expires/24.)

    @gen.coroutine
    @rw.scope.inject
    def login(self, handler):
        email = handler.get_argument('email')
        password = handler.get_argument('password')
        user = yield model.User.find_one({'email': email})
        if user and user.check_password(password):
            self.set_current(user)
            raise gen.Return(user)

    @gen.coroutine
    @rw.scope.inject
    def register(self, handler):
        email = handler.get_argument('email')
        password = handler.get_argument('password')
        user = model.User()
        user.email = email
        user.set_password(password)
        yield user.insert()
        raise gen.Return(user)


class PermissionDenied(tornado.web.HTTPError):
    def __init__(self, permission, subject):
        super(PermissionDenied, self).__init__(403)


@gen.coroutine
@rw.scope.inject
def pre_request_handler(handler, scope, services):
    user = yield services['user'].current()
    scope['user'] = handler['user'] = user


@plugin.init
def init(scope, settings):
    perm.PERMISSION_DENIED_EXCEPTION = PermissionDenied

    scope.subscope('services')['user'] = UserService()

    preload = settings.get('rwuser', {}).get('preload_user', False)
    if preload:
        rw.httpbase.PRE_REQUEST.add(pre_request_handler)
