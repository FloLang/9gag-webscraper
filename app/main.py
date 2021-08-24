import logging

from peewee import MySQLDatabase
from scrapers import MainpageScraper
from Post import Post, global_database_object

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    mainpageScraper = MainpageScraper()

    postGenerator = mainpageScraper.scrollMainpage()

    # TODO config file
    my_runtime_db = MySQLDatabase('test_db', **{'host': 'mysql',
                                                'user': 'test',
                                                'password': "password",
                                                'port': 3306})
    global_database_object.initialize(my_runtime_db)
    my_runtime_db.create_tables([Post])

    try:
        # Get 15 posts
        for x in range(15):
            post = next(postGenerator)

            post.save()
            logging.info("Stored post in %s", post.downloadMedia())

            logging.info("Retrieved post from generator:\n%s ", post.__repr__())

            # TODO multiprocessing when persisting posts to db (to utilize timeout time while scraping)
            # TODO send to slack server
    except StopIteration:
        logging.info("stopped iteration")

    logging.info("Completed scraping successfully, shutting down...")
