from datetime import datetime
from src import fbcrawlerutils as fbutil
from src.fbgroupcrawler import GroupCrawler
from src.outputgenerator import OutputGenerator
from src.utils import loadConfiguration, getLogger
from src.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

config = loadConfiguration("config/config.yaml")
logger = getLogger("main")


def main():
    global driver
    fbutil.login(driver)
    try:
        crawlTillEndOfTime()
    except TimeoutException as timeOutException:
        logger.warn("Timeout exception. Relaunching...")
        driver.quit()
        driver = WebDriver(config['webdriver']['chromeoptions']).getDriver()
        main()
    except Exception as e:
        logger.exception(repr(e))

def crawlTillEndOfTime():
    while True:
        startTime = int(datetime.now().timestamp())
        crawlAllGroupsOnce()
        writeOutput(startTime)


def crawlAllGroupsOnce():
    for group in config['input']['groups']:
        GroupCrawler(driver, group).crawlGroup()


def writeOutput(startTime):
    logger.info("Job completed! Generating output.")
    outputFileName = config['output']['outputfileprefix'] + "_" + datetime.now().strftime("%d_%m_%Y_%I_%M_%p") + ".html"
    outputGenerator = OutputGenerator(outputFileName)
    outputGenerator.generateOuputFromDatabase()
    logger.info("Complete output written to file: {}".format(outputFileName))
    newPostsFileName = config['output']['newpostsfileprefix'] + "_" + datetime.now().strftime(
        "%d_%m_%Y_%I_%M_%p") + ".html"
    newPostsOutputGenerator = OutputGenerator(newPostsFileName)
    newPostsOutputGenerator.generateOuputFromDatabase(
        selectQuery="SELECT * FROM posts where timestamp>{}".format(startTime))
    logger.info("New posts written to file: {}".format(newPostsFileName))


if __name__=='__main__':
    driver = WebDriver(config['webdriver']['chromeoptions']).getDriver()
    main()

'''
def synchronized(func):
    func.__lock__ = threading.Lock()
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)
    return synced_func
'''