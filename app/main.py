from scrapers import MainpageScraper
from Post import Post

if __name__ == "__main__":
    mainpageScraper = MainpageScraper()

    postGenerator = mainpageScraper.scrollMainpage()

    try:
        # Get 15 posts
        for x in range(15):
            post = next(postGenerator)
            print(post)

            # TODO multiprocessing when persisting posts to db (to utilize timeout time while scraping)
    except StopIteration:
        print("stopped iteration")
