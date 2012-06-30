import webapp2
from webapp2_extras import jinja2

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        def factory(app):
            config = jinja2.default_config
            config['template_path'] = app.config['template_path']
            config['environment_args']['line_statement_prefix'] = '%'
            return jinja2.Jinja2(app, config)
        return jinja2.get_jinja2(factory=factory, app=self.app)

    def render_response(self, _template, **context):
        # Renders a template and writes the result to the response.
        rv = self.jinja2.render_template(_template + '.html', **context)
        self.response.write(rv)

