curl -XPUT -k 'https://127.0.0.1:9200/accidents' \
   --user 'elastic:elastic' \
   --header 'Content-Type: application/json' \
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": { "properties": { "_id": { "type": "integer" }, "ACCIDENT_NO": { "type": "keyword" }, "ACCIDENT_DATE": { "type": "date", "format": "yyyy-MM-dd" }, "ACCIDENT_TIME": { "type": "text" }, "ACCIDENT_TYPE": { "type": "keyword" }, "ACCIDENT_TYPE_DESC": { "type": "text" }, "DAY_OF_WEEK": { "type": "keyword" }, "DAY_WEEK_DESC": { "type": "text" }, "DCA_CODE": { "type": "keyword" }, "DCA_DESC": { "type": "text" }, "LIGHT_CONDITION": { "type": "keyword" }, "NODE_ID": { "type": "keyword" }, "NO_OF_VEHICLES": { "type": "integer" }, "NO_PERSONS_KILLED": { "type": "integer" }, "NO_PERSONS_INJ_2": { "type": "integer" }, "NO_PERSONS_INJ_3": { "type": "integer" }, "NO_PERSONS_NOT_INJ": { "type": "integer" }, "NO_PERSONS": { "type": "integer" }, "POLICE_ATTEND": { "type": "keyword" }, "ROAD_GEOMETRY": { "type": "keyword" }, "ROAD_GEOMETRY_DESC": { "type": "text" }, "SEVERITY": { "type": "keyword" }, "SPEED_ZONE": { "type": "keyword" }, "RMA": { "type": "text" } }
}'  | jq '.'