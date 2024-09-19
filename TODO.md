# MODULES

# [MAJORS](#major)
[Back-end Django](#django)
[User management](#user-management)
[Log Management](#log-management)
[Micro services](#micro-services)
# [MINORS](#minor)
[PostGreSQL](#postgree)
[Game Stats](#game-stats)
[Monitoring System](#monitoring)


# Major
## Django 

[Back End API](./Backend_API.md)

## User management
Login  ✅
Logout ✅
Tournaments Name ❌
Update Information ❌
Upload avatar ❌
Friends with status ❌
Profiles stats ❌
Match History ❌
Save one username_og and username_internal(lowercase) for verifications ❌




## Log Management

Deploy Elasticsearch to efficiently store and index log data, making it easily
searchable and accessible.  ✅

Configure Logstash to collect, process, and transform log data from various
sources and send it to Elasticsearch. ✅

Set up Kibana for visualizing log data, creating dashboards, and generating
insights from log events. Needs better dashboards ❌

Define data retention and archiving policies to manage the storage of log data
effectively.  ❌

Implement security measures to protect log data and access to the ELK stack
components. Password? ❌

## Micro services

All back end is done through docker and different containers with minimal dependencies  ✅
Comunication is done through API requests or DB interactions  ✅


# Minor

## Postgree

All services are connecting to DB container ✅

## Game stats

Create user-friendly dashboards that provide users with insights into their own gaming statistics. ❌

Develop a separate dashboard for game sessions, showing detailed statistics, outcomes, and historical data for each match. ❌

Implement data visualization techniques, such as charts and graphs, to present statistics in a clear and visually appealing manner ❌

##  Monitoring

Deploy Prometheus as the monitoring and alerting toolkit to collect metrics 
and monitor the health and performance of various system components. ✅

Configure data exporters and integrations to capture metrics from different
services, databases, and infrastructure components. Needs better stats capture ❌

Create custom dashboards and visualizations using Grafana to provide realtime insights into system metrics and performance. Needs better dashboards❌

Set up alerting rules in Prometheus to proactively detect and respond to
critical issues and anomalies. Needs better alerts ❌

Ensure proper data retention and storage strategies for historical metrics data. ❌

Implement secure authentication and access control mechanisms for Grafana
to protect sensitive monitoring data. Password?  ❌

