from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db/database.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'Users'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String)
    password = Column('password', String)
    created = Column('created', DateTime, default=lambda: datetime.now())
    posts = relationship('Post')

    def __str__(self):
        return f'<User(id={self.id}, username={self.username}, password={self.password}, ' \
               f'created={self.created})>'


class Post(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    created = Column(DateTime, default=lambda: datetime.now())
    user = Column(Integer, ForeignKey('Users.id'))

    def __str__(self):
        return f'<Post(id={self.id}, title={self.title}, description={self.description}, ' \
               f'created={self.created}, user={self.user})>'


if __name__ == '__main__':
    """
    Base.metadata.create_all(engine)
            or
    User.metadata.create_all(engine)
    Post.metadata.create_all(engine)
    """
    User.metadata.create_all(engine)

    # user = User(username='test user', password='test password')
    # session.add(user)
    # session.commit()
    #
    # session.add(Post(title='test title', description='test description', user=user.id))
    # session.commit()

    user_query = session.query(User).filter(User.username.__eq__('test user')).first()
    post_query = session.query(Post).filter(Post.user.__eq__(user_query.id)).first()
    print(f'user: {user_query}\n'
          f'post: {post_query}')
    '''
    user: <User(id=1, username=test user, password=test password, created=2018-02-12 00:36:34.773818)>
    post: <Post(id=1, title=test title, description=test description, created=2018-02-12 00:36:34.827158, user=1)>
    '''
