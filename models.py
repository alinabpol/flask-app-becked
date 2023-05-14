from peewee import *


DATABASE = SqliteDatabase('dogs.sqlite')


class Dog(Model):
    name = CharField()
    age = IntegerField()
    breed = CharField()

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog], safe=True)
    print("TABLES Created")
    DATABASE.close()