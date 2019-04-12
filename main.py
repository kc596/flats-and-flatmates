from queue import Queue
from src.crawler import Crawler
from src.outputgenerator import OutputGenerator
from src.utils import loadConfiguration
import sys

config = loadConfiguration("config/config.yaml")
jobQueue = Queue()

for i in range(config['input']['thread']):
    crawler = Crawler(jobQueue)
    crawler.start()

for group in config['input']['groups']:
    jobQueue.put(group)

jobQueue.join()
print("Job completed! Generating output.")

outputGenerator = OutputGenerator()
print("Output written to file.")
