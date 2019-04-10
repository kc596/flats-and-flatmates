import logging
import logging.config
import os
import yaml

configuration = ''
loggerInitialized = False

def loadConfiguration(configfile='config/config.yaml'):
	global configuration 					#needed to modify global copy of variable
	with open(configfile, 'r') as cf:
		config = yaml.safe_load(cf.read())
		configuration = config
	return config

def loadCredentials(credfile='config/credentials.yaml'):
	with open(credfile, 'r') as cf:
		credentials = yaml.safe_load(cf.read())
	return credentials

def getLogger(name):
	global loggerInitialized
	if loggerInitialized is False:
		initializeLogger()
		loggerInitialized = True
	logger = logging.getLogger(name)
	return logger


############ HELPER FUNCTIONS - not referred outside file ##############

def initializeLogger():	
	if len(configuration) == 0:
		loadConfiguration()
	createLogFileDirectory()
	logging.config.dictConfig(configuration['logs'])

def createLogFileDirectory():
	os.makedirs(os.path.dirname(str(configuration['logs']['handlers']['file']['filename'])), exist_ok=True)
