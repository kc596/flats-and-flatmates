from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.common.utils import loadConfiguration, loadCredentials
import selenium
import time

config = loadConfiguration("config/config.yaml")
credential = loadCredentials("config/credentials.yaml")

def login(driver):
	wait = WebDriverWait(driver, config['webdriver']['wait']['time'])
	driver.get("https://www.facebook.com/login/")
	wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email'][@type='text']")))
	userNameInput = driver.find_element_by_xpath("//input[@name='email'][@type='text']")
	passwordInput = driver.find_element_by_xpath("//input[@name='pass'][@type='password']")
	userNameInput.send_keys(credential['email'])
	passwordInput.send_keys(credential['password'])
	driver.find_element_by_xpath("//button[@type='submit']").click()

def getPostAtIndex(driver, index, logger):
	ActionChains(driver).send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
	time.sleep(config['webdriver']['sleep'])
	posts = driver.find_elements_by_xpath("//div[@role='article'][contains(@id, 'post')]")
	postElement = posts[index]
	ActionChains(driver).move_to_element(postElement).perform()
	try:
		seeMoreLinkElement = postElement.find_element_by_xpath(".//a[@class='see_more_link']")
		ActionChains(driver).move_to_element(seeMoreLinkElement).perform()
		seeMoreLinkElement.click()
	except NoSuchElementException as e:
		logger.debug("See more link not present")
	return postElement

def getBodyOfPost(postElement, logger):
	bodyOfThisPost = ""
	paragraphsOfThisPost = postElement.find_elements_by_xpath(".//p")
	for paragraph in paragraphsOfThisPost:
		bodyOfThisPost += paragraph.text
	return bodyOfThisPost

def getEpochOfPost(postElement, logger):
	try:
		timeElement = postElement.find_element_by_xpath(".//div[@data-testid='story-subtitle']//*[@data-utime]")
		return int((timeElement).get_attribute("data-utime"))
	except Exception as e:
		logger.exception("Unable to get time stamp of post. Trying to get link of post for debugging.")
		time.sleep(20)
		logger.error("Link to post: "+getLinkToPost(postElement, logger))
		time.sleep(20)
		return 0

def getLinkToPost(postElement, logger):
	links = postElement.find_elements_by_xpath(".//div[@data-testid='story-subtitle']//a")
	for link in links:
		if 'permalink' in str(link.get_attribute("href")):
			return str(link.get_attribute("href"))
	logger.exception("Link to post not found")
	return "linknotfound"