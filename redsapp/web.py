#!/usr/bin/env python

import os

import webapp2

from model import User, CoachingSession
from base import BaseHandler

class Users(BaseHandler):
    def get(self):
        users = User.query.order_by(User.fullname)
        self.render_response('Users', users=users)

class Sessions(BaseHandler):
    def get(self):
        sessions = CoachingSession.query.order_by(CoachingSession.time)
        self.render_response('Sessions', sessions=sessions)

class SessionChecklist(BaseHandler):
    def get(self, sessionid):
        session = CoachingSession.query.get(sessionid)
        self.render_response('SessionChecklist', session=session)

class Index(BaseHandler):
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

    return webapp2.WSGIApplication([
        (r'/', Index),
        (r'/users', Users),
        (r'/sessions', Sessions),
        (r'/sessions/(\d+)/checklist', SessionChecklist),
        ], config={'template_path' : template_path},
           debug=True)
