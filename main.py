from datetime import datetime
from queue import Queue
from src.crawler import Crawler
from src.outputgenerator import OutputGenerator
from src.utils import loadConfiguration
import time

config = loadConfiguration("config/config.yaml")
jobQueue = Queue()
crawlers = []

for i in range(config['input']['thread']):
    crawler = Crawler(jobQueue)
    crawler.start()
    crawlers.append(crawler)

while True:
    startTime = int(datetime.now().timestamp())
    print("Starting crawling at {}".format(datetime.now()))
    for group in config['input']['groups']:
        jobQueue.put(group)

    if len(crawlers) > len(config['input']['groups']):
        for i in range(len(crawlers)-len(config['input']['groups'])):
            jobQueue.put("dummy")

    # wait for completion of all jobs in queue
    while True:
        terminate = True
        for retry in range(5):
            for crawler in crawlers:
                terminate = terminate and crawler.idle
            time.sleep(60)
        if terminate:
            break

    print("Job completed! Generating output.")
    outputFileName = config['output']['outputfileprefix']+"_"+datetime.now().strftime("%d_%m_%Y_%I_%M_%p")+".html"
    outputGenerator = OutputGenerator(outputFileName)
    outputGenerator.generateOuputFromDatabase()
    print("Complete output written to file: {}".format(outputFileName))

    newPostsFileName = config['output']['newpostsfileprefix']+"_"+datetime.now().strftime("%d_%m_%Y_%I_%M_%p")+".html"
    newPostsOutputGenerator = OutputGenerator(newPostsFileName)
    newPostsOutputGenerator.generateOuputFromDatabase(selectQuery="SELECT * FROM posts where timestamp>{}".format(startTime))
    print("New posts written to file: {}".format(newPostsFileName))