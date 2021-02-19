# yasttt event settings

action.yasttt = [0|1]
* Enable thehive_create_alert notification

action.yasttt.param.title = <string>
* Alert Title to use in TheHive.
* (required)

action.yasttt.param.description = <string>
* The description of the alert to send to TheHive.
* (required)

action.yasttt.param.severity = [0|1|2|3]
* The severity of the new alert. 1 = low, 2 = medium, 3 = high
* Default is "1" (low)
* (required)

action.yasttt.param.alert_type = <string>
* The type of the new alert. 
* (required)

action.yasttt.param.alert_source = <string>
* The source of the new alert. 
* (required)

action.yasttt.param.tlp = [-1|0|1|2|3]
* Traffic Light Protocol for this case. 0 = White, 1 = Green, 2 = Amber, 3 = Red
* TLP affects releasability of information. Some analyzers will not be available on higher TLP settings.
* Defaults to "2" (Amber)
* (required)

action.yasttt.param.tags = <string>
* The tags to put on the alert. Use a single, comma-separated string (ex. "badIP,spam").
* (optional)
