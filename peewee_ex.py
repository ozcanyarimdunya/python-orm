import datetime

from peewee import (
    SqliteDatabase, Model, CharField, ForeignKeyField, TextField, DateTimeField, BooleanField
)

db = SqliteDatabase('peewee.db')


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        return "{name}<{pk}>".format(name=self.__class__.__name__, pk=super().__str__())


class User(BaseModel):
    username = CharField(unique=True)
    password = CharField(max_length=120)


class Task(BaseModel):
    user = ForeignKeyField(User, backref='task')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)


def initialise_db():
    """Initialise database"""
    _user1, _ = User.get_or_create(
        username="ozcan",
        password="123"
    )

    Task.get_or_create(
        user=_user1,
        message="Hello World"
    )

    Task.get_or_create(
        user=_user1,
        message="How are you?"
    )

    _user2, _ = User.get_or_create(
        username="naczo",
        password="321"
    )

    Task.create(
        user=_user2,
        message="Hello again"
    )


if __name__ == '__main__':
    db.connect()
    db.create_tables([User, Task])

    initialise_db()

    user = User.get_by_id(pk=1)
    print(
        user.username,
        user.password,
        user.task.count(),
    )

    task = Task.get(Task.user == user)
    print(task)

    try:
        task = Task.get(Task.message == "Hello World?")
        print(task)
    except Task.DoesNotExist:
        print("Model does not exists")

    tasks = Task.select().filter(Task.message.contains('Hello'))
    for task in tasks:
        print(task)
