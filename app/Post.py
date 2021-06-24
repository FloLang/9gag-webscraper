import csv
import os
import urllib.request
import time


class Post:
    def __init__(self, postID, title, mediaURL):
        self.postID = postID ## TODO __postID immutable
        self.title = title
        if "," in self.title:
            print("replacing comma in title of post " + postID)
            self.title.replace(",", "|")
        self.mediaURL = mediaURL

        self.mediaFileType = self.mediaURL.split(".")[-1]
        self.mediaFilePath = ""

    def __repr__(self):
        return "\npostID: {}\npostTitle: {}\nmediaURL: {}\npostURL: {}\n".format(
            self.postID, self.title, self.mediaURL, self.getURL())

    @staticmethod
    def storePosts(rootFolder, posts):
        # TODO replace commas in titles, give exception when url contains one
        # TODO improve robustness, download and writing at same time no goody
        # TODO consider JSON or XML instead
        folder = rootFolder + str(int(time.time())) + "/"
        os.mkdir(folder) # TODO create folder inside docker container first before doing this

        with open(folder + "metadata.csv", "w+") as f:
            f.write("id,title,mediaURL\n")
            for post in posts:
                post.downloadMedia(folder)
                f.write("{},{},{}\n".format(post.postID, post.title, post.mediaURL))


    def downloadMedia(self, folder):
        self.mediaFilePath = folder + self.postID + "." + self.mediaFileType

        urllib.request.urlretrieve(self.mediaURL, self.mediaFilePath) # TODO will be deprecated
        # TODO file permission, owner root because of docker

        return self.mediaFilePath

    def downloadComments(self):
        # beautifulsoup because static?
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
