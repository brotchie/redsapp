#!/usr/bin/env python
import os

import webapp2

from auth import auth_middleware
from model import User, CoachingSession, Session
from base import AuthedBaseHandler, BaseHandler

class Users(AuthedBaseHandler):
    roles = {'admin'}

    def get(self):
        users = User.query.order_by(User.fullname)
        self.render_response('Users', users=users)

class SessionList(AuthedBaseHandler):
    def get(self):
        sessions = CoachingSession.query.order_by(CoachingSession.time)
        self.render_response('Sessions', sessions=sessions)

class SessionChecklist(AuthedBaseHandler):
    def get(self, sessionid):
        session = CoachingSession.query.get(sessionid)
        self.render_response('SessionChecklist', session=session)

class Sessions(BaseHandler):
    roles = {'admin'}

    def delete(self, sessionid):
        s = Session()
        with s.transaction:
            session = s.query(CoachingSession).get(sessionid)
            if session:
                s.delete(session)
            else:
                self.response.set_status(404)

class Index(AuthedBaseHandler):
    def get(self):
        self.render_response('Index')

def build_application(env, template_path=None):
    assert template_path is None or \
           os.path.isdir(template_path), \
           'template_path argument must be a diretory.'

    if template_path:
        # Add templates to the paste reloader watchlist.
        from paste import reloader
        [reloader.watch_file(filename) for filename in
            os.listdir(template_path)]

    return auth_middleware(webapp2.WSGIApplication([
        (r'/', Index),
        (r'/users', Users),
        (r'/sessions', SessionList),
        (r'/sessions/(\d+)', Sessions),
        (r'/sessions/(\d+)/checklist', SessionChecklist),
        ], config={'template_path' : template_path},
           debug=True))
