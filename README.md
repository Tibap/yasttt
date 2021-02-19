# Yet Another Splunk To TheHive Tool - YASTTT app
To create Splunk Response Actions to send to TheHive as alerts. Python3 friendly. 

Tested with:
- Thehive Version: 3.4.2
- Splunk 8.1.0

This project was largely inspired by:
- https://github.com/swiip81/create_thehive_alert
- https://github.com/daniel-gallagher/create_thehive_alert

These projects are however not supporting Python 3 or were not answering these simple needs:
- app needs to  

## Installation

```
# Go to your Splunk app folder
cd /opt/splunk/etc/apps/  # adapt if /opt is not where you are installing splunk
# Git clone the repo:
git clone  TODO
```

## Configuration

1/ In TheHive, create a dedicated user with an API key and no permission but: Allow alerts creation.

2/ In Splunk, go to "Manage Apps", click on the set up link for the app "Yet Another Splunk To TheHive Tool" and set:
- The URL of TheHive server (ex. https://thehive.domain.com) 
- TheHive API Key you just created
- the log level you want to use (default is INFO)

## How to use from Splunk

1/ Create an alert, in the Alert Action section, select action "YASTTT Alert Action"
2/ Set the mandatory parameters:
- the Title for the alert you want to create, 
- the base description, knowing that the all fields from the searcg will be automatically added to that description, 
- the severity
- the Alert type (Splunk, internal, Microsoft, etc)
- the TLP (Traffic Light Protocol) 
- (not required) any tags you'd like to appear
3/ Trigger the alert in Splunk
	
## Debug information

Logs are sent to: SPLUNK_HOME/var/log/splunk/yasttt.log. Don't forget to change the log level to DEBUG in the app configuration if needed.