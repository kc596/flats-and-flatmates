from datetime import datetime
from queue import Queue
from src.crawler import Crawler
from src.outputgenerator import OutputGenerator
from src.utils import loadConfiguration

config = loadConfiguration("config/config.yaml")
jobQueue = Queue()

startTime = int(datetime.now().timestamp())

for i in range(config['input']['thread']):
    crawler = Crawler(jobQueue)
    crawler.start()

for group in config['input']['groups']:
    jobQueue.put(group)

jobQueue.join()
print("Job completed! Generating output.")

outputFileName = config['output']['outputfileprefix']+"_"+datetime.now().strftime("%d_%m_%Y_%I_%M_%p")+".html"
outputGenerator = OutputGenerator(outputFileName)
outputGenerator.generateOuputFromDatabase()
print("Complete output written to file: {}".format(outputFileName))

newPostsFileName = config['output']['newpostsfileprefix']+"_"+datetime.now().strftime("%d_%m_%Y_%I_%M_%p")+".html"
newPostsOutputGenerator = OutputGenerator(newPostsFileName)
newPostsOutputGenerator.generateOuputFromDatabase(selectQuery="SELECT * FROM posts where timestamp>{}".format(startTime))
print("New posts written to file: {}".format(newPostsFileName))