#!/usr/bin/env python

def main():
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with session.transaction:
        session.add(User('James', 'James Brotchie', 'asdf1234', '+61422015622'))

    print list(session.query(User).order_by(User.id))

if __name__ == '__main__':
    main()
