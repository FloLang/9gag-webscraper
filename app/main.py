from scrapers import MainpageScraper
from Post import Post

if __name__ == "__main__":
    mainpageScraper = MainpageScraper()

    posts = mainpageScraper.scrape()

    Post.storePosts("posts/", posts)

    # TODO save to mysql
    # TODO report how many new posts saved in mysql