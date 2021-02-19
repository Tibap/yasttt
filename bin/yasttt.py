#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: Dimitri Kirchner @ vancity

import os
import sys
import json
import gzip
import csv
import logging
import logging.handlers

from lib.thehive import Thehive

def setup_logger(level):
    """
    Splunk logger.
    """
    logger = logging.getLogger('yasttt')
    logger.propagate = True # Prevent the log messages from being duplicated in the python.log file
    logger.setLevel(level)
    file_handler = logging.handlers.RotatingFileHandler(os.path.join(os.environ['SPLUNK_HOME'], 'var', 'log', 'splunk', 'yasttt.log'), maxBytes=25000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def get_config(config):

    url = config.get('url') # Get TheHive URL from Splunk configuration
    api_key = config.get('api_key') # Get TheHive API key from Splunk configuration

    # Get the payload for the case from the config, use defaults if they are not specified
    title = config.get('title')
    description = config.get('description', "No description provided.")
    severity = int(config.get('severity', 1))
    owner = config.get('owner')
    alert_type = config.get('alert_type')
    alert_source = config.get('alert_source')
    tlp = int(config.get('tlp', 2))
    tags = [] if config.get('tags') is None else config.get('tags').split(",")

    hive = Thehive(url, api_key, title, description, severity, owner, tlp, tags, alert_type, alert_source)
    return hive
    

if __name__ == '__main__':

    # make sure we have the right number of arguments - more than 1; and first argument is "--execute"
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        # read the payload from stdin as a json string
        payload = json.loads(sys.stdin.read())
        # extract the results file and alert config from the payload
        config = payload.get('configuration')
        
        log_level = config.get('log_level')
        if 'debug' == log_level.lower():
            logger = setup_logger(logging.DEBUG)
        elif 'info' == log_level.lower():
            logger = setup_logger(logging.INFO)
        elif 'warning' == log_level.lower():
            logger = setup_logger(logging.WARNING)
        elif 'error' == log_level.lower():
            logger = setup_logger(logging.ERROR)
        else:
            logger = setup_logger(logging.INFO)# Set default to INFO
        #logger.info("Logger level is set to: {}".format(logger.getEffectiveLevel()))
        
        logger.debug("Python version: {}".format(sys.version))
        
        results_file = payload.get('results_file')
        logger.debug("Results_file: {}".format(results_file))
        
        if os.path.exists(results_file):
            try:
                with gzip.open(results_file, 'rt') as f:
                    file_content = f.readlines()
                    #logger.debug("File Content: {}".format(file_content))
                    reader = csv.DictReader(file_content)
                    
                    logger.debug("Instanciating Hive class")
                    hive = get_config(config)
                    
                    if hive is None:
                        logger.error("Hive object has not been initialized, quitting")
                        sys.exit(-1)
                    
                    # iterate through each row, creating an alert for each 
                    for row in reader:
                        logger.debug(row)
                        res = hive.submitTheHive(row)
                        if not res:
                            logger.warn("SubmitTheHive method has failed.")
                            sys.exit(4)
                sys.exit(0)
            except IOError as e:
                logger.error("Results file exists but could not be opened/read")
                sys.exit(3)
        else:
            logger.error("Results file does not exist: {}".format(results_file))
            sys.exit(2)
    else:
        print("Unsupported execution mode (expected --execute flag)")
        sys.exit(1)