
INDX=bce3c459-aceb-4b2c-a650-6d1212b08319
DASHBOARD_ID=a3ebeba0-4fe4-11ef-a74c-6de6710340ab
echo ${INDX}
echo ${DASHBOARD_ID}

json_payload=$(cat <<EOF
{
    "changes": {
        "buildNum": {
            "userValue": 61224
        },
        "isDefaultIndexMigrated": {
            "userValue": true
        },
        "defaultIndex": {
            "userValue": "${INDX}"
        },
        "defaultRoute": {
            "userValue": "/app/dashboards#/view/${DASHBOARD_ID}"
        }
    }
}
EOF
)

if [ ! -z "$DASHBOARD_ID" ]; then
    echo exporting settings
    curl -X POST  -H "kbn-xsrf: true" \
    "http://localhost:5601/api/kibana/settings"\
    -H "Content-Type: application/json"\
    -u "elastic:changeme" \
    -d "${json_payload}"

else
    echo Not exporting
fi

curl --user elastic:changeme -X POST "localhost:5601/api/saved_objects/config-global/" -H "kbn-xsrf: true" -H "Content-Type: application/json" -d '{"attributes": {"defaultRoute": "/app/dashboards#/view/a3ebeba0-4fe4-11ef-a74c-6de6710340ab"}}'

curl --user elastic:changeme -X POST "localhost:5601/api/saved_objects/_export" -H "kbn-xsrf: true" -H "Content-Type: application/json" -d '{
    "type": "config",
    "id": "02fecb80-6462-11ef-9942-e1c6a500eb09",
    "attributes": {
        "defaultRoute": "/app/dashboards#/view/a3ebeba0-4fe4-11ef-a74c-6de6710340ab"
    },
    "references": [],
    "migrationVersion": {
        "config": "8.7.0"
    },
    "coreMigrationVersion": "8.7.1",
    "updated_at": "2024-08-27T10:49:19.161Z",
    "created_at": "2024-08-27T10:49:19.161Z",
    "version": "WzM2OSwxXQ==",
    "namespaces": [
        "default"
    ]
}'



curl --user elastic:changeme -X POST "localhost:5601/api/saved_objects/_export" -H "kbn-xsrf: true" -H "Content-Type: application/json" -d '{
  "objects": [
    {
      "id": "4b82ea00-6465-11ef-9942-e1c6a500eb09",
      "type": "config-global"
    }
  ],
  "excludeExportDetails": true,
  "includeReferencesDeep": false
}'

curl \
  --user elastic:changeme \
 -X PUT localhost:5601/api/saved_objects/config/8.7.1 \
 -H "Content-Type: application/json; Elastic-Api-Version=2023-10-31" \
 -H "kbn-xsrf: string"\
 -d '{"attributes": {"defaultRoute": "/app/dashboards#/view/a3ebeba0-4fe4-11ef-a74c-6de6710340ab"}}'

curl \
 -X PUT https://localhost:5601/api/saved_objects/{type}/{id} \
 -H "Content-Type: application/json; Elastic-Api-Version=2023-10-31" \
 -H "kbn-xsrf: string"

8.7.1
curl --user elastic:changeme -X GET "localhost:5601/api/saved_objects/_find?type=config-global" -H "kbn-xsrf: true" -H "Content-Type: application/json" 


    curl \
    --user elastic:changeme \
    -X PUT http://localhost:5601/api/saved_objects/config/8.7.1 \
    -H "Content-Type: application/json; Elastic-Api-Version=2023-10-31" \
    -H "kbn-xsrf: true"\
    -d "{\"attributes\": {\"defaultRoute\": \"/app/dashboards#/view/a3ebeba0-4fe4-11ef-a74c-6de6710340ab\"}}"