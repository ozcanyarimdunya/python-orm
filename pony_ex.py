from datetime import datetime
import pony.orm as p

db = p.Database()


class Post(db.Entity):
    id = p.PrimaryKey(int, auto=True)
    title = p.Required(str)
    description = p.Required(str, 1000)
    created = p.Optional(datetime, default=lambda: datetime.now())
    user = p.Required('User')

    def __str__(self):
        return f'<Post(id={self.id}, title={self.title}, description={self.description}, ' \
               f'created={self.created}, user={self.user})>'


class User(db.Entity):
    id = p.PrimaryKey(int, auto=True)
    username = p.Required(str)
    password = p.Required(str, 1000, unique=True)
    created = p.Optional(datetime, default=lambda: datetime.now())
    posts = p.Set(Post)

    def __str__(self):
        return f'<User(id={self.id}, username={self.username}, ' \
               f'password={self.password}, created={self.created})>'


@p.db_session
def add_data():
    _user = User(username='test user', password='test password')
    Post(title='test title', description='test description', user=_user)


if __name__ == '__main__':
    # p.set_sql_debug(True)
    db.bind(provider='sqlite', filename='db/pony.sqlite', create_db=True)
    db.generate_mapping(create_tables=True)

    # add_data()
    with p.db_session:
        user = User.get(username='test user')
        post = Post.get(user=user)
        print(f'user: {user}\n'
              f'post: {post}')
        '''
        user: <User(id=1, username=test user, password=test password, created=2018-02-11 23:54:55.349382)>
        post: <Post(id=1, title=test title, description=test description, created=2018-02-11 23:54:55.349486, user=<User(id=1, username=test user, password=test password, created=2018-02-11 23:54:55.349382)>)>
        '''
