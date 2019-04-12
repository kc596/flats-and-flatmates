from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.utils import *

class WebDriver:
	def __init__(self, options=None):
		self.logger = getLogger("WebDriver")
		self.driver = None
		try:
			chromeOptions  = Options()
			for option in options:
				chromeOptions.add_argument(option)
			self.driver = webdriver.Chrome('drivers/chromedriver', chrome_options=chromeOptions)
			self.logger.info("Initialized selenium webdriver.")
		except Exception as e:
			self.logger.exception("Unable to get selenium webdriver!")

	def getDriver(self):
		return self.getChromeDriver()

	def getChromeDriver(self):
		return self.driver
