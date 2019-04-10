from src.common.utils import loadConfiguration, getLogger
from src import fbcrawlerutils as fbutil
from src.common.Database import Database
from src.common.WebDriver import WebDriver
from threading import Thread
import time

config = loadConfiguration("config/config.yaml")

class Crawler(Thread):
	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue
		self.driver = WebDriver(config['webdriver']['chromeoptions']).getDriver()
		fbutil.login(self.driver)
	
	def run(self):
		while True:
			groupSlug = self.queue.get()
			databaseSession = False
			logger = getLogger(groupSlug)
			logger.info("Crawling started.")
			try:
				database = Database(groupSlug)
				databaseSession = True
				self.driver.get(config['input']['url'].format(groupSlug))
				index = 0
				posts = []
				logger.info("Scrolling posts")
				while index < config['input']['limit']:
					try:
						postElement = fbutil.getPostAtIndex(self.driver, index, logger)
						bodyOfPost = fbutil.getBodyOfPost(postElement, logger)
						timestamp = fbutil.getEpochOfPost(postElement, logger)
						linkToPost = fbutil.getLinkToPost(postElement, logger)
						if self.isPostSignificant(bodyOfPost):
							keywordMatches = self.getKeywordMatches(bodyOfPost)
							post = (linkToPost, timestamp, str(keywordMatches))
							database.insertPost(post)
					except Exception as e:
						logger.error("Error in post number : "+str(index))
						logger.exception(repr(e))
					index += 1
				logger.info("Completed crawling.")
			except Exception as e:
			   logger.exception(repr(e))
			finally:
				if databaseSession:
					database.closeSession()
				self.queue.task_done()
	
	@staticmethod
	def isPostSignificant(bodyOfPost):
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