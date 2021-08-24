import csv
import logging
import os
import shutil
import urllib.request
import time

# https://stackoverflow.com/questions/448684/why-should-you-use-an-orm
# "portability, abstraction (vendor specific SQL). ORM bad choice when you want to tweak queries for performance"
from peewee import *

global_database_object = Proxy()  # https://timlehr.com/lazy-database-initialization-with-peewee-proxy-subclasses/


class Post(Model):
    class Meta:
        database = global_database_object

    # TODO fix mysql inserting not wokring anymore
    postID = CharField(primary_key=True)
    # TODO using non-integer primary keys is a good idea. The cost in storage is higher, the index lookups will be slower, and foreign key joins will be more expensive
    title = CharField(max_length=256)
    mediaURL = CharField(max_length=128)
    mediaFileType = CharField(max_length=8)

    def __init__(self, postID, title, mediaURL, *args, **kwargs):

        super().__init__(*args, **kwargs)  # https://github.com/coleifer/peewee/issues/856#issuecomment-412353441
        self.postID = postID  # TODO __postID immutable
        # self.title = title.replace(",", "|") only do this when writing to csv
        self.title = title
        self.mediaURL = mediaURL
        self.mediaFileType = self.mediaURL.split(".")[-1]
        self.mediaFilePath = ""

    def __repr__(self):
        return "\npostID: {}\npostTitle: {}\nmediaURL: {}\npostURL: {}\n".format(
            self.postID, self.title, self.mediaURL, self.getURL())

    @staticmethod
    def storePostsCSV(rootFolder, posts):
        # TODO replace commas in titles, give exception when url contains one
        # TODO improve robustness, download and writing at same time no goody
        # TODO consider JSON or XML instead
        folder = rootFolder + str(int(time.time())) + "/"
        os.mkdir(folder)  # TODO create folder inside docker container first before doing this

        with open(folder + "metadata.csv", "w+") as f:
            f.write("id,title,mediaURL\n")
            for post in posts:
                # post.downloadMedia(folder)
                f.write("{},{},{}\n".format(post.postID, post.title, post.mediaURL))

    def downloadMedia(self, folder="/usr/src/app/posts"):
        self.mediaFilePath = folder + "/" + self.postID + "." + self.mediaFileType

        logging.info("Downloading media from %s", self.mediaURL)

        urllib.request.urlretrieve(self.mediaURL, self.mediaFilePath)

        # TODO find solution to files owned by root problem
        # shutil.chown(self.mediaFilePath, user="floris", group="floris")
        # will give LookupError: no such user: 'floris'

        return self.mediaFilePath

    def downloadComments(self):
        # beautifulsoup because static? (no, because it will not load comments)
        pass

    def getURL(self):
        return "https://9gag.com/gag/" + self.postID

    # https://stackoverflow.com/questions/17493307/creating-set-of-objects-of-user-defined-class-in-python
    def __hash__(self):
        return hash(self.postID)

    def __eq__(self, other):
        # Check if other object is a Post Class
        if not isinstance(other, type(self)):
            return False

        return self.postID == other.postID
