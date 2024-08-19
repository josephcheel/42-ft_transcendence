#!/bin/bash
#it only replaces the value inside the json file if it creates a new datasource

#create datasource
datasource_id=$(curl -s -u "admin:newadmin" -H 'Content-Type: application/json' grafana:3000/api/datasources -d '{
  "name":"prometheus",
  "type":"prometheus",
  "url":"http://prometheus:9090",
  "access":"proxy",
  "basicAuth":false
}' | grep '"uid":' | awk -F'"' '{print $8}')


# Contact point creation

if [ $(curl -s -X GET -u "admin:newadmin" http://grafana:3000/api/v1/provisioning/contact-points | grep -q "Transcendence Slack"; echo $?) -eq 1 ]; then
echo "Creating contact point"
curl -s -X POST \
  -H "Content-Type: application/json" \
  -u "admin:newadmin" \
  -d @- \
  http://grafana:3000/api/v1/provisioning/contact-points <<EOF
{
  "name": "Transcendence Slack",
  "type": "slack",
  "settings": {
    "url": "${SLACK_HOOK}",
    "recipient": "#alerts",
    "username": "Grafana Alert",
    "icon_emoji": ":grafana:"
  }
}
EOF
fi


# create folder
folder_id=$(curl -s -X POST    -H "Content-Type: application/json"   -u "admin:newadmin"   -d '{
  "uid": null,
  "title": "Transcendence",
  "parentUid": null
}'  http://grafana:3000/api/folders | grep "uid" | awk -F'"' '{print $6}')


export FOLDER_ID="${folder_id}"
export DATASOURCE_ID="${datasource_id}"

echo folder id $FOLDER_ID

echo data source id $DATASOURCE_ID

if [[ -n "$DATASOURCE_ID" && $(grep -q '"uid": "replace"' /gateway_dashboard.json; echo $?) -eq 0 ]]; then
    curl -s -H "Content-Type: application/json" -u "admin:newadmin" grafana:3000/api/dashboards/db -d @/gateway_dashboard.json 
fi

if [ -n "$FOLDER_ID" ] && [ -n "$DATASOURCE_ID" ]; then
curl -s -X POST \
  http://grafana:3000/api/v1/provisioning/alert-rules \
  -H "Content-Type: application/json" \
  -u "admin:newadmin" \
  -d "$(cat <<EOF
{
  "id": null,
  "uid": null,
  "orgID": 1,
  "folderUID": "${FOLDER_ID}",
  "ruleGroup": "Alerts 1m",
  "title": "Alerta2",
  "condition": "C",
  "data": [
    {
      "refId": "A",
      "queryType": "",
      "relativeTimeRange": {
        "from": 600,
        "to": 0
      },
      "datasourceUid": "${DATASOURCE_ID}",
      "model": {
        "disableTextWrap": false,
        "editorMode": "builder",
        "expr": "rate(gateway_django_http_requests_latency_seconds_by_view_method_sum[\$__rate_interval])",
        "fullMetaSearch": false,
        "includeNullMetadata": false,
        "instant": true,
        "intervalMs": 1000,
        "legendFormat": "__auto",
        "maxDataPoints": 43200,
        "range": false,
        "refId": "A",
        "useBackend": false
      }
    },
    {
      "refId": "C",
      "queryType": "",
      "relativeTimeRange": {
        "from": 600,
        "to": 0
      },
      "datasourceUid": "__expr__",
      "model": {
        "conditions": [
          {
            "evaluator": {
              "params": [
                0.00001
              ],
              "type": "gt"
            },
            "operator": {
              "type": "and"
            },
            "query": {
              "params": [
                "C"
              ]
            },
            "reducer": {
              "params": [],
              "type": "last"
            },
            "type": "query"
          }
        ],
        "datasource": {
          "type": "__expr__",
          "uid": "__expr__"
        },
        "expression": "A",
        "intervalMs": 1000,
        "maxDataPoints": 43200,
        "refId": "C",
        "type": "threshold"
      }
    }
  ],
  "updated": "2024-08-02T08:10:20Z",
  "noDataState": "NoData",
  "execErrState": "Error",
  "for": "1m",
  "isPaused": false,
  "notification_settings": {
    "receiver": "Transcendence Slack"
  },
  "record": null
}
EOF
)"
fi