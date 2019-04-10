from src.common.utils import *
from src.Crawler import Crawler
from queue import Queue

config = loadConfiguration("config/config.yaml")
jobQueue = Queue()

for i in range(config['input']['thread']):
	crawler = Crawler(jobQueue)
	crawler.start()

for group in config['input']['groups']:
	jobQueue.put(group)
jobQueue.join()
print("Job completed!")