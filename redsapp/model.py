from bcrypt import hashpw
from sqlalchemy import create_engine, Boolean, Column, Integer, String, DateTime, text, Table, ForeignKey, func, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship

NOW = text("(datetime('now'))")
SALT = '$2a$06$a7/qLH5WcehYZ2oggNWAB.'

DATABASE_PATH = 'redsapp.db'

engine = create_engine('sqlite:///%s' % (DATABASE_PATH,), echo=True)
Session = scoped_session(sessionmaker(bind=engine))

Model = declarative_base()

userroles = Table(
        'userroles', Model.metadata,
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('role_id', Integer, ForeignKey('roles.id'))
        )

lower = func.lower

class Role(Model):
    __tablename__ = 'roles'

    query = Session.query_property()

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role('{r.name}')>".format(r=self)

class User(Model):
    __tablename__ = 'users'

    query = Session.query_property()

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    passwordhash = Column(String)
    mobilephonenumber = Column(String)

    creationdate = Column(DateTime(timezone=True),
                          server_default=NOW)
    enabled = Column(Boolean, default=True)

    roles = relationship("Role", secondary=userroles, backref='users')

    #__table_args__ = (Index('name'),)

    def _hashpw(self, password):
        return hashpw(password, SALT)

    def is_password_valid(self, prospective):
        return self._hashpw(prospective) == self.passwordhash

    @property
    def rolenames(self):
        return {role.name for role in self.roles}

    def __init__(self, name, fullname, password, mobilephonenumber=None, enabled=True):
        self.name = name
        self.fullname = fullname
        self.mobilephonenumber = mobilephonenumber
        self.passwordhash = self._hashpw(password)
        self.enabled = enabled

    def __repr__(self):
        return "<User('{u.name}','{u.fullname}','{u.mobilephonenumber}','{u.creationdate}',{u.enabled})>".format(u=self)


class CoachingSession(Model):
    __tablename__ = 'sessions'

    query = Session.query_property()

    id = Column(Integer, primary_key=True)
    week = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    time = Column(DateTime(timezone=True), nullable=False)
    coordinator_id = Column(ForeignKey('users.id'))
    coordinator = relationship("User", backref='sessions')

    complete = Column(Boolean, default=False)
    completiontime = Column(DateTime(timezone=True))

    def __init__(self, location, week, time,
                 coordinator, complete=False,
                 completiontime=None):
        self.location = location
        self.week = week
        self.time = time
        self.coordinator = coordinator
        self.complete = complete
        self.completiontime = completiontime

if __name__ == '__main__':
    import os
    if os.path.exists(DATABASE_PATH):
        os.unlink(DATABASE_PATH)
    Model.metadata.create_all(engine)

    s = Session()
    with s.transaction:
        role = Role('admin')
        user1 = User('James', 'James Brotchie', 'asdf1234', '+61422015622')
        user1.roles.append(role)

        user2 = User('Tom', 'Tom Percy', 'tom22', enabled=False)

        from dateutil.parser import parse
        s.add_all([user1, user2])
        s.add_all([CoachingSession('BGS', 1, parse('2012-06-03 13:00'), user2, complete=True, completiontime=parse('2012-06-03 14:07')),
                   CoachingSession('BGS', 2, parse('2012-06-10 13:00'), user2),
                   CoachingSession('BGS', 3, parse('2012-06-17 13:00'), user2)])

