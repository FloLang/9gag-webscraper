import unittest

from peewee import MySQLDatabase

from app.Post import Post, global_database_object


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        my_runtime_db = MySQLDatabase('myDatabase', **{'host': 'localhost',
                                                       'user': 'test',
                                                       'password': "password",
                                                       'port': 3306})

        global_database_object.initialize(my_runtime_db)

        my_runtime_db.create_tables([Post])

    def test_upper(self):
        print("test")

        post = Post("23fgds3", "title Unit test", "http://boopy.org")

        post.save()


if __name__ == '__main__':
    unittest.main()
