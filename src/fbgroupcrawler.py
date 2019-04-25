from src.utils import loadConfiguration, getLogger
from src import fbcrawlerutils as fbutil
from src.database import Database

config = loadConfiguration("config/config.yaml")


class GroupCrawler:
    def __init__(self, driver, groupSlug):
        self.driver = driver
        self.groupSlug = groupSlug
        self.logger = getLogger(groupSlug)
        self.database = Database(groupSlug)
        self.index = -1

    def crawlGroup(self):
        self.driver.get(config['input']['url'].format(self.groupSlug))
        self.logger.info("Crawling started.")
        try:
            while self.noOfCrawledPostIsLessThanLimit():
                self.crawlNextPost()
            self.database.closeSession()
        except Exception as e:
            self.logger.error("Error in post number : " + str(self.index))
            self.logger.exception(repr(e))
        finally:
            self.logger.info("Completed crawling " + str(self.groupSlug))

    def noOfCrawledPostIsLessThanLimit(self):
        return self.index <= config['input']['limit']

    def crawlNextPost(self):
        self.index += 1
        postElement = fbutil.getPostAtIndex(self.driver, self.index, self.logger)
        if self.isPostSignificant(postElement):
            self.addPostToDatabase(postElement)

    def addPostToDatabase(self, postElement):
        self.logger.debug("Inserting post number " + str(self.index) + " to database")
        bodyOfPost = fbutil.getBodyOfPost(postElement)
        timestamp = fbutil.getEpochOfPost(postElement, self.index, self.logger)
        linkToPost = fbutil.getLinkToPost(postElement, self.index, self.logger)
        keywordMatches = self.getKeywordMatches(bodyOfPost)
        post = (linkToPost, timestamp, str(keywordMatches), bodyOfPost.encode("utf-8"))
        self.database.insertPost(post)

    @staticmethod
    def isPostSignificant(postElement):
        bodyOfPost = fbutil.getBodyOfPost(postElement)
        searchSpace = bodyOfPost.lower()
        allKeywords = config['input']['keywords']
        allExceptions = config['input']['exceptions']
        if any(keyword in searchSpace for keyword in allKeywords):
            if not any(exceptionWord in searchSpace for exceptionWord in allExceptions):
                return True
        return False

    @staticmethod
    def getKeywordMatches(bodyOfPost):
        searchSpace = bodyOfPost.lower()
        allKeywords = config['input']['keywords']
        keywordMatches = []
        for keyword in allKeywords:
            if keyword in searchSpace:
                keywordMatches.append(keyword)
        return keywordMatches
