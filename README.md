# CCC Project

## Restful API

- `search/roadcondition`
- `search/accidents`
- `search/weather`
- `search/population`
- `search/accident_locations`
- `search/geoinfo`

### Run Test

```
python -m unittest tests.test_api.TestAPIEndpoints.<function_name>
```

## Setup

1. Connect to VPN
2.

```
source <path/to/openrc.sh>
```

3. ssh

```
ssh -i <path/to/.pem> -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')
```

4. ES

```
kubectl port-forward service/elasticsearch-master -n elastic 9200:9200
```

5. kibana

```
kubectl port-forward service/kibana-kibana -n elastic 5601:5601
```

6. Fission

```
kubectl port-forward service/router -n fission 9090:80
```

## ElasticSearch

### Operations

#### Search

```bash

curl -XGET -k "https://127.0.0.1:9200/accidents/_search"\
  --header 'Content-Type: application/json'\
  --data '{
  "query": {
    "nested": {
      "path": "nodes",
      "query": {
        "match_all": {}
      }
    }
  }
}'\
  --user 'elastic:elastic' | jq '.'
```

```bash
curl -XGET -k "https://127.0.0.1:9200/accident_locations/_search"\
  --header 'Content-Type: application/json'\
  --data '{
    "query": {
        "range": {
			"_id": {
			"gte": "140650",
			"lte": "140655",
			}
		}
	}
	}'\
  --user 'elastic:elastic' | jq '.'
```

```bash
curl -XGET -k "https://127.0.0.1:9200/accident_locations/_search"\
  --header 'Content-Type: application/json'\
  --data '{
    "query": {
        "match_all": {}
	}
	}'\
  --user 'elastic:elastic' | jq '.'
```

```bash
curl -XGET -k "https://127.0.0.1:9200/accident_locations/_count"\
  --header 'Content-Type: application/json'\
  --data '{
    "query": {
        "match_all": {}
	}
	}'\
  --user 'elastic:elastic' | jq '.'
```

```bash
curl -XGET -k "https://127.0.0.1:9200/accidents/_search" \
  --header 'Content-Type: application/json' \
  --user 'elastic:elastic' \
  --data '{
    "query": {
        "bool": {
            "must_not": [
                {
                    "exists": {
                        "field": "Date"
                    }
                }
            ]
        }
    }
  }' | jq '.'

```

#### Insert Doc

```bash
curl -XPOST -k "https://127.0.0.1:9200/test/_doc/"\
  --header 'Content-Type: application/json'\
  --data '{
        "a": "2",
        "b": "3",
        "c": "3"
    }'\
  --user 'elastic:elastic' | jq '.'
```

```bash
curl -XPUT -k "https://127.0.0.1:9200/test/_doc/_YX4M48Bx6f91pQDqVKV"\
  --header 'Content-Type: application/json'\
  --data '{
        "e": "10"
    }'\
  --user 'elastic:elastic' | jq '.'
```

#### Create Index

```bash
curl -XPUT -k 'https://127.0.0.1:9200/test' \
   --user 'elastic:elastic' \
   --header 'Content-Type: application/json' \
   --data '{
  "settings": {
    "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
  },
  "mappings": {
    "properties": {
      "a": {
        "type": "text"
      },
      "b": {
	      "type": "text"
      }
    }
  }
}'  | jq '.'
```

```bash
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
  "mappings": {
    "properties": {
    "relation_type": {
	    "type": "join",
	    "relations": {
		    "accident": "node"
		    }
		},
      "ACCIDENT_NO": {
        "type": "keyword"
      },
      "ACCIDENT_DATE": {
        "type": "date",
        "format": "yyyy-MM-dd"
      },
      "ACCIDENT_TYPE": {
        "type": "integer"
      },
      "ACCIDENT_TYPE_DESC": {
        "type": "text"
      },
      "DAY_OF_WEEK": {
	     "type": "integer"
	  },
      "NODE_ID": {
        "type": "integer"
      },
      "NO_OF_VEHICLES": {
        "type": "integer"
      },
      "NO_PERSONS_KILLED": {
        "type": "integer"
      },
      "NO_PERSONS_INJ_2": {
        "type": "integer"
      },
      "NO_PERSONS_INJ_3": {
        "type": "integer"
      },
      "NO_PERSONS_NOT_INJ": {
        "type": "integer"
      },
      "NO_PERSONS": {
        "type": "integer"
      },
      "ROAD_GEOMETRY": {
        "type": "integer"
      },
      "ROAD_GEOMETRY_DESC": {
        "type": "text"
      },
      "SEVERITY": {
        "type": "integer"
      },
      "SPEED_ZONE": {
        "type": "integer"
      }
    }
  }
}'  | jq '.'

```

```
curl -XPUT -k 'https://127.0.0.1:9200/weather' \

--header 'Content-Type: application/json' \

--data '{

"settings": {

"index": {

"number_of_shards": 3,

"number_of_replicas": 1

}

},

"mappings": {

"properties": {

"Date": {"type": "date", "format": "yyyy-MM-d"},

"Minimum temperature (°C)": {"type": "float"},

"Maximum temperature (°C)": {"type": "float"},

"Rainfall (mm)": {"type": "float"}

}

}

}' \

--user 'elastic:elastic' | jq '.'
```

#### Delete Index

```
curl -XDELETE -k 'https://127.0.0.1:9200/accidents' --user 'elastic:elastic' | jq '.'
```

## Fission

### Function

```
fission function create --name weather --env python --code /Users/clarec/Documents/GitHub/CCC_group63_frontend/functions/weather.py

fission function create --name weathertest --env python --code /Users/clarec/Documents/GitHub/CCC_group63_frontend/weathertest.py


fission function update --name weather --code /Users/clarec/Documents/GitHub/CCC_group63_frontend/functions/weather.py

fission fn update --name weather --env python --mincpu 100 --maxcpu 500 --minmemory 100 --maxmemory 500

fission function test --name weather | jq '.'
fission function test --name weathertest | jq '.'

```

### Route

```
fission route create --url /weather --function weather --name weather --createingress

curl "http://127.0.0.1:9090/weather" | jq '.'
```

### Pkg

```
cd functions/addobservations
zip -r addobservations.zip .
mv addobservations.zip ../

cd ../..

fission package create --sourcearchive ./functions/addobservations.zip\
  --env python\
  --name addobservations\
  --buildcmd './build.sh'

fission fn create --name addobservations\
  --pkg addobservations\
  --env python\
  --entrypoint "addobservations.main"

fission route create --url /addobservations --function addobservations --name addobservations --createingress


curl "http://127.0.0.1:9090/addobservations" | jq '.'
```

### Creation of a RestFUL API with YAML specifications

A ReSTful API may look like:

```
/temperature/{date}
```

#### Route creation

We start by using the fission commands to create the YAML files defining the routes/HTTPTriggers:

```
fission route create --name avgtempday --function avgtemp \
    --method GET \
    --url '/temperature/days/{date:[0-9][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]}'

fission route create --name searchweatherdate --method GET --url "/searchweather/dates/{start_date}/{end_date}" --function searchweather


```

### crush 三件套

chmod +x build.sh

```
fission specs init
< after creation of env/pkg/fn/route>
fission spec validate
fission spec apply --specdir specs --wait
```

```
fission function delete --name weather
fission route delete --name weather
fission pkg list
fission pkg delete --name

fission function delete --name addobservations
fission route delete --name addobservations
fission pkg delete --name addobservations
```

#### getweather

- Create

```
cd functions/getweather
zip -r getweather.zip . -x "*.DS_Store"
mv getweather.zip ../

cd ../..

fission package create --spec --sourcearchive ./functions/getweather.zip\
  --env python\
  --name getweather\
  --buildcmd './build.sh'

fission fn create --spec --name getweather\
  --pkg getweather\
  --env python\
  --entrypoint "getweather.main"

fission route create --spec --url /getweather --function getweather --name getweather --createingress

fission spec apply --specdir specs --wait

curl "http://127.0.0.1:9090/getweather" | jq '.'
```

- Delete

```
fission function delete --name getweather
fission route delete --name getweather
fission pkg delete --name getweather
```

#### searchweather

- Create

```bash
cd functions/searchweather
zip -r searchweather.zip . -x "*.DS_Store"
mv searchweather.zip ../

cd ../..

fission package create --spec --sourcearchive ./functions/searchweather.zip\
  --env python\
  --name searchweather\
  --buildcmd './build.sh'

fission fn create --spec --name searchweather\
  --pkg searchweather\
  --env python\
  --entrypoint "searchweather.main"

fission httptrigger create --spec --method GET \
    --url "/searchweather/{StartDate}/{EndDate}" --function searchweather --name searchweather

fission httptrigger create --spec --method GET \
    --url "/searchweather?sdate={StartDate}&edate={EndDate}" --function searchweather --name searchweather

curl "http://127.0.0.1:9090/searchweather/2024-03-01/2024-03-11" | jq '.'
```

fission route create --url /searchweather --function searchweather --name searchweather --createingress

curl "http://127.0.0.1:9090/searchweather" | jq '.'

fission route create --name searchweatherdate --method GET --url "/searchweather/{start_date}/{end_date}" --function searchweather

- Delete

```
fission function delete --name searchweather
fission pkg delete --name searchweather
fission route delete --name searchweather
```

#### getaccidents

- Create

```bash
cd functions/getaccidents
zip -r getaccidents.zip . -x "*.DS_Store"
mv getaccidents.zip ../

cd ../..

fission package create --spec --sourcearchive ./functions/getaccidents.zip\
  --env python\
  --name getaccidents\
  --buildcmd './build.sh'

fission fn create --spec --name getaccidents\
  --pkg getaccidents\
  --env python\
  --entrypoint "getaccidents.main"

fission route create --spec --url /getaccidents --function getaccidents --name getaccidents --createingress

curl "http://127.0.0.1:9090/getaccidents" | jq '.'
```

- Delete

```bash
fission function delete --name getaccidents
fission route delete --name getaccidents
fission pkg delete --name getaccidents
```

#### storeweather

```bash
cd functions/storeweather
zip -r storeweather.zip . -x "*.DS_Store"
mv storeweather.zip ../

cd ../..

fission package create --spec --sourcearchive ./functions/storeweather.zip\
  --env python\
  --name storeweather\
  --buildcmd './build.sh'

fission fn create --spec --name storeweather\
  --pkg storeweather\
  --env python\
  --entrypoint "storeweather.main"

fission route create --spec --url /storeweather --function storeweather --name storeweather --createingress


curl "http://127.0.0.1:9090/storeweather"
```

- Delete

```
fission function delete --name storeweather
fission route delete --name storeweather
fission pkg delete --name storeweather
```

#### getlocations

```
cd functions/getlocations
zip -r getlocations.zip . -x "*.DS_Store"
mv getlocations.zip ../

cd ../..

fission package create --spec --sourcearchive ./functions/getlocations.zip\
  --env python\
  --name getlocations\
  --buildcmd './build.sh'

fission fn create --spec --name getlocations\
  --pkg getlocations\
  --env python\
  --entrypoint "getlocations.main"\

fission route create --spec --url /getlocations --function getlocations --name getlocations --createingress


curl "http://127.0.0.1:9090/getlocations"
```

- Delete

```
fission function delete --name getlocations
fission route delete --name getlocations
fission pkg delete --name getlocations
```

#### getroadcondition

```bash
cd functions/getroadcondition
zip -r getroadcondition.zip . -x "*.DS_Store"
mv getroadcondition.zip ../

cd ../..

fission package create --spec --sourcearchive ./functions/getroadcondition.zip\
  --env python\
  --name getroadcondition\
  --buildcmd './build.sh'

fission fn create --spec --name getroadcondition\
  --pkg getroadcondition\
  --env python\
  --entrypoint "getroadcondition.main"\

fission route create --spec --url /getroadcondition --function getroadcondition --name getroadcondition --createingress

fission spec apply --specdir specs --wait

curl "http://127.0.0.1:9090/getroadcondition"
```

- Delete

```
fission function delete --name getroadcondition
fission route delete --name getroadcondition
fission pkg delete --name getroadcondition
```

#### search

```bash
cd functions/search
zip -r search.zip . -x "*.DS_Store"
mv search.zip ../

cd ../..

fission package create --spec --sourcearchive ./functions/search.zip\
  --env python\
  --name search\
  --buildcmd './build.sh'

fission fn create --spec --name search\
  --pkg search\
  --env python\
  --entrypoint "search.main"\

fission route create --spec --url /search/{Indexname} --function search --name search --createingress

fission spec apply --specdir specs --wait

curl "http://127.0.0.1:9090/search/accidents"
```

- Delete

```
fission function delete --name search
fission route delete --name search
fission pkg delete --name search
```
