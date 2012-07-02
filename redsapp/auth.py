import sys
import logging

from repoze.who.middleware import PluggableAuthenticationMiddleware
from repoze.who.plugins.basicauth import BasicAuthPlugin

from model import User, lower

class UserModelAuthenticator(object):
    def __init__(self):
        self._metadata_cache = {}

    def authenticate(self, environ, identity):
        try:
            login = identity['login']
            password = identity['password']
        except KeyError:
            return None

        user = User.query.filter(lower(User.name) == login.lower()).first()
        if user and user.is_password_valid(password):
            self._metadata_cache[user.name] = { 'user' : user }
            return user.name
        else:
            return None

    def add_metadata(self, environ, identity):
        """Adds the roles that the user belongs to
        to metadata."""
        username = identity.get('repoze.who.userid')
        identity.update(self._metadata_cache.get(username, {}))

def authrequired(*args, **kwargs):
    """Decorator to enforce authentication."""
    roles = kwargs.get('roles', None)

    def outer(f):
        def closure(self, *handlerargs, **handlerkwargs):
            username = self.request.environ.get('REMOTE_USER')
            if not username:
                self.response.set_status(401)
            elif roles and self.user and not self.user.rolenames & roles:
                self.response.set_status(403)
            else:
                f(self, *handlerargs, **handlerkwargs)
        return closure

    if args:
        return outer(args[0])
    else:
        return outer

basicauth = BasicAuthPlugin('factorial.coaching')
userauth = UserModelAuthenticator()

identifiers = [('basicauth', basicauth)]
authenticators = [('dummy', userauth)]
challengers = [('basicauth', basicauth)]
mdproviders = [('usermd', userauth)]

from repoze.who.classifiers import default_request_classifier
from repoze.who.classifiers import default_challenge_decider

def auth_middleware(app):
    return PluggableAuthenticationMiddleware(
        app,
        identifiers,
        authenticators,
        challengers,
        mdproviders,
        default_request_classifier,
        default_challenge_decider,
        log_stream = sys.stdout,
        log_level = logging.DEBUG
    )

