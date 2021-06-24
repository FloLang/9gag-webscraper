from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from time import sleep

from Post import Post


class MainpageScraper:
    def __init__(self):
        self.streamCount = 0
        self.scrollHeight = 0

        # Try 5 times, wait 3s if exception to give Firefox a moment to start
        for i in range(0, 5):
            while True:
                try:
                    self.driver = webdriver.Remote("http://firefox:4444/wd/hub", DesiredCapabilities.FIREFOX)
                except: #TODO which exception is given
                    print("\nException while trying to connect to Selenium Firefox container, retrying after 3 seconds...\n") #TODO replace prints with logging
                    sleep(3)
                    continue
                break

        # On a user-defined bridge network, containers can resolve each other by name or alias.
        # TODO remote debugging


    def status(self):
        return "status"

    # TODO yield (like in java?) posts
    def scrape(self):
        posts = set()
        self.driver.get("https://9gag.com/")

        while self.streamCount < 3:
            try:
                stream = WebDriverWait(self.driver, 1).until(
                    expected_conditions.presence_of_element_located((By.ID, "stream-" + str(self.streamCount)))
                )
                print("stream-" + str(self.streamCount) + " found")

                # Iterate trough stream articles and collect post data
                streamArticles = stream.find_elements_by_tag_name("article")
                for article in streamArticles:
                    articleID = article.get_property("id")  # Example ID string: "jsid-post-a7EpzDx"
                    if articleID != "":
                        articleID = articleID.split("-")[2]
                    else:
                        print("no ID in this article, probably advert, skipping")
                        continue

                    articleTitle = article.find_element_by_tag_name("h1").text

                    mediaURL = ""
                    try:
                        mediaURL = article.find_element_by_class_name("post-container"). \
                            find_element_by_tag_name("video").find_element_by_tag_name("source").get_attribute("src")
                    except NoSuchElementException:
                        try:
                            mediaURL = article.find_element_by_class_name("post-container"). \
                                find_element_by_tag_name("picture").find_element_by_tag_name("img").get_attribute("src")
                        except NoSuchElementException:
                            print("neither mp4 nor jpg found")

                    post = Post(articleID, articleTitle, mediaURL)
                    posts.add(post)
                    print("new post added: " + articleID)

                self.streamCount += 1

            except TimeoutException:
                print("timeout while waiting for list-stream-" + str(self.streamCount) + ", scrolling down 700px")
                self.scrollHeight += 700
                self.driver.execute_script("window.scrollTo(0, " + str(self.scrollHeight) + ");")

        self.driver.quit()
        print("Scraping complete, found posts: " + str(len(posts)))
        return posts


class SectionScraper:
    #TODO interface, some sections different structure
    pass
