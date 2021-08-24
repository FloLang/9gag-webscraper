import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

from Post import Post


class MainpageScraper:
    def __init__(self):

        # Try 10 times, wait 3s if exception to give Firefox a moment to start
        for i in range(9):
            try:
                self.driver = webdriver.Remote("http://firefox:4444/wd/hub", DesiredCapabilities.FIREFOX) # TODO make config
                logging.info("Connected to Firefox Selenium!")

                break
            except:  # TODO which exception is given?
                logging.error("Exception while trying to connect to Selenium Firefox container, retrying after 3 seconds...")
                sleep(3)

    def scrollMainpage(self):
        # TODO abort when no connection with Selenium

        self.driver.get("https://9gag.com/")

        streamNumber = 0
        scrollHeight = 0
        retries = 0

        while True:
            stream = None
            
            # Scroll down in Selenium browser (max 15 times) and collect the HTML stream containing posts.
            while stream is None and retries < 15:
                try:
                    # Streams are numbered: stream-0...x
                    stream = WebDriverWait(self.driver, 2).until(
                        expected_conditions.presence_of_element_located((By.ID, "stream-" + str(streamNumber)))
                    )
                    logging.info("stream-%s found", str(streamNumber))
                    streamNumber += 1
                    break

                except TimeoutException:
                    logging.info("timeout while waiting for list-stream-" + str(streamNumber) + ", scrolling down 700px")
                    scrollHeight += 700
                    self.driver.execute_script("window.scrollTo(0, " + str(scrollHeight) + ");")
                    retries += 1

            if stream is None:
                # TODO press the "more" button
                logging.critical("Can't find new stream, aborting scraping")
                break

            # Loop trough stream articles and collect the data for post
            for article in stream.find_elements_by_tag_name("article"):
                # Get the post ID
                articleID = article.get_property("id")  # Example ID string: "jsid-post-a7EpzDx"
                if articleID != "":
                    articleID = articleID.split("-")[2]
                else:
                    logging.info("no ID in this article, probably advert, skipping")
                    continue

                # Get the post title
                articleTitle = article.find_element_by_tag_name("h1").text

                # Get the mediaURL (mp4 or jpg) of the post
                mediaURL = ""
                try:
                    mediaURL = article.find_element_by_class_name("post-container"). \
                        find_element_by_tag_name("video").find_element_by_tag_name("source").get_attribute("src")
                except NoSuchElementException:
                    try:
                        mediaURL = article.find_element_by_class_name("post-container"). \
                            find_element_by_tag_name("picture").find_element_by_tag_name("img").get_attribute("src")
                    except NoSuchElementException:
                        logging.warning("No mediaURL found for postID: %s", articleID)

                yield Post(articleID, articleTitle, mediaURL)

        self.driver.quit()
