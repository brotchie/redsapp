import webapp2
from webapp2_extras import jinja2

class BaseHandler(webapp2.RequestHandler):
    """
    Custom RequestHandler with added support for
    jinja2 template rendering and repoze.who identities.

    """
    @webapp2.cached_property
    def jinja2(self):
        def factory(app):
            config = jinja2.default_config
            config['template_path'] = app.config['template_path']
            config['environment_args']['line_statement_prefix'] = '%'
            return jinja2.Jinja2(app, config)
        return jinja2.get_jinja2(factory=factory, app=self.app)

    def render_response(self, _template, **context):
        # We also pass on the currently authed user through to the
        # template.
        context['user'] = self.user
        rv = self.jinja2.render_template(_template + '.html', **context)
        self.response.write(rv)

    def initialize(self, request, response):
        """
        Sets self.user to the repoze.who authed user as a convienience.
        """
        super(BaseHandler, self).initialize(request, response)

        try:
            self.user = self.request.environ['repoze.who.identity']['user']
        except KeyError:
            self.user = None

class AuthedBaseHandler(BaseHandler):
    """
    RequestHandler that requires mandatory authentication to
    serve requets. Options roles base auth if roles
    class variable is a set of valid roles.

    """
    roles = None

    def dispatch(self):
        if not self.user:
            self.response.set_status(401)
        elif self.roles and not self.user.rolenames & self.roles:
            self.response.set_status(403)
        else:
            super(AuthedBaseHandler, self).dispatch()
