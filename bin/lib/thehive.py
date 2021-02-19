#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: Dimitri Kirchner @ vancity

import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact
import logging

logger = logging.getLogger('yasttt')

class Thehive:

    def __init__(self, url, api_key, title, description, severity, owner, tlp, tags, alert_type, alert_source):
        self.url = url
        self.title = title
        self.description = description
        self.severity = severity
        self.owner = owner
        self.tlp = tlp
        self.alert_type = alert_type
        self.tags = tags
        self.alert_source = alert_source
        
        self.__apikey = api_key
        logger.debug("url: {} ; apikey: {}".format(self.url, self.__apikey))
        self.api = TheHiveApi(self.url, self.__apikey, cert=False)

    def create_observable(self, csv_rows):
        logger.debug('Creating default observables')
        
        artifacts = []
        for (key, value) in csv_rows.items():
            # Do not take empty keys
            if not key.startswith("__mv_"):
                if key.endswith('url'):
                    artifacts.append(AlertArtifact(dataType='url', data=value)) 
                elif key.endswith('other'):
                    artifacts.append(AlertArtifact(dataType='other', data=value)) 
                elif key.endswith('user-agent'):
                    artifacts.append(AlertArtifact(dataType='user-agent', data=value))  
                elif key.endswith('regexp'):
                    artifacts.append(AlertArtifact(dataType='regexp', data=value))
                elif key.endswith('mail_subject'):
                    artifacts.append(AlertArtifact(dataType='mail_subject', data=value)) 
                elif key.endswith('registry'):
                    artifacts.append(AlertArtifact(dataType='registry', data=value))
                elif key.endswith('mail'):
                    artifacts.append(AlertArtifact(dataType='mail', data=value))
                elif key.endswith('autonomous-system'):
                    artifacts.append(AlertArtifact(dataType='autonomous-system', data=value))
                elif key.endswith('domain'):
                    artifacts.append(AlertArtifact(dataType='domain', data=value)) 
                elif key.endswith('ip'):
                    artifacts.append(AlertArtifact(dataType='ip', data=value)) 
                elif key.endswith('uri_path'):
                    artifacts.append(AlertArtifact(dataType='uri_path', data=value))
                elif key.endswith('filename'):
                    artifacts.append(AlertArtifact(dataType='filename', data=value))                    
                elif key.endswith('hash'):
                    artifacts.append(AlertArtifact(dataType='hash', data=value)) 
                elif key.endswith('fqdn'):
                    artifacts.append(AlertArtifact(dataType='fqdn', data=value))
                
        return artifacts
    

    def submitTheHive(self, csv_rows):
        '''Create a new case in TheHive based on the email'''
        logger.debug("Creating alert with title: {}, description: {}".format(self.title, self.description))
        sourceRef = str(uuid.uuid4())[0:6]
        logger.debug("uuid: {}".format(sourceRef))
        
        artifacts = self.create_observable(csv_rows)
        
        formatted_result = "```"
        for key, value in csv_rows.items():
            if not key.startswith("__mv_"):
                formatted_result = "{}\n{}: {}".format(formatted_result, key, value)
        formatted_result += "```"
            
        self.description = "{}\n{}".format(self.description, formatted_result)
        
        alert = Alert(title=self.title,
                      tlp = self.tlp,
                      tags = self.tags,
                      description=self.description,
                      type=self.alert_type,
                      source=self.alert_source,
                      sourceRef=sourceRef,
                      artifacts=artifacts,
                      severity=self.severity
                )

        # Create the Alert
        if self.api:
            logger.debug("Sending alert to thehive: {}".format(self.url))
            response = self.api.create_alert(alert)
            logger.debug("response status code: {}".format(response.status_code))
            
            if response.status_code == 201:
                logger.info("Alert {} created successfully: {}".format(sourceRef, self.title))
                return True
            else:
                logger.error("Alert has not been created: {} ({})".format(response.status_code, response.text))

        else:
            logger.error("HiveAPI is None")

        return False
