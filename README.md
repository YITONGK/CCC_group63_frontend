# CCC-project

## Report

[Analysis of Potential Factors-affected Car Accidents in Victoria](https://www.overleaf.com/4751181365djrvrfzzxqrt#c886a0)

## Confluence Page

[CCC_A2](https://felikskong.atlassian.net/wiki/spaces/CCCA2/overview?homepageId=295444)

## Data

- Population in Victoria
  [SUDO](https://sudo.eresearch.unimelb.edu.au/)
- Geographical information of Victoria
  [SUDO](https://sudo.eresearch.unimelb.edu.au/)
- Victoria Road Crash Data
  [Victorian Government Data Directory](https://vicroadsopendatastorehouse.vicroads.vic.gov.au/opendata/Road_Safety/RCIS%20Documents/Metadata%20-%20Victoria%20Road%20Crash%20data.pdf)
- Weather Conditions in Last Two Years
  [BOM](http://www.bom.gov.au/)

## Scenarios and figs (main.ipynb)

- **Analysis of LGA areas and the number/severity of accidents**

  - LGA & number of accidents & population (done)
  - LGA & number of accidents dot map (done)
    - Cluster of num accidents in geo
    - Subplot of LGA & number of accidents & population, [illustration](https://plotly.com/python/mixed-subplots/)

- **Analysis of population and the number of car accidents**

  - bar chart (population increase with LGA name) + line (num of accidents), [illustration](https://plotly.com/python/figurewidget/) (ing)

- **Analysis of rainfall & speed on the number of accidents**

- **Pie chart analysis of the severity of the car accident**

  - Full Severity Statistics for 2023

- **Analysis of road conditions and the number of car accidents**

## Restful API

```
To get the population for each local government area(LGA) in Victoria:
  ”http://127.0.0.1:9090/search/population”

To get all the accidents details from 2022 to 2023:
  ”http://127.0.0.1:9090/search/accidents”

To get all the coordinates and LGA name for all the accidents:
  ”http://127.0.0.1:9090/search/accident_locations”

To get geographic information of Victoria to establish an interactive map
  ”http://127.0.0.1:9090/search/geoinfo”

To get the information of accident road surface:
  ”http://127.0.0.1:9090/search/roadcondition”

To search the weather in a period of time, the date should be in format ”YYYYMMDD”:
  ”http://127.0.0.1:9090/searchweather/Startdate/Enddate”
```

## Functions for uploading by data streaming from open API

```
Scrape weather data of 2023 from BOM and insert into ES
curl -X PUT "http://127.0.0.1:9090/put/accidents"
inside the process, “extract“ function will be called to scrape accidents data
URL: "http://router.fission.svc.cluster.local/extract/accidents"

Scrape data of all the details about accidents happened in Victoria from 2022 to 2023 and upload
curl -X PUT "http://127.0.0.1:9090/put/weather"
inside the process, “extract“ function will be called to scrape weather data
URL: "http://router.fission.svc.cluster.local/extract/weather"
```

## Functions for static data upload

```
Insert accident locations, containing coordinates and LGA
curl -X PUT "http://127.0.0.1:9090/put/accident_locations" -H "Content-Type: application/json" -d @data/upload_location.json

Insert geographic information of Victoria for making an interactive map
curl -X PUT "http://127.0.0.1:9090/put/geoinfo" -H "Content-Type: application/json" -d @data/upload_geoinfo.json

Insert the population data for 80 LGA in Victoria
curl -X PUT "http://127.0.0.1:9090/put/population" -H "Content-Type: application/json" -d @data/upload_population.json

Insert the condition of road surface when accidents happened
curl -X PUT "http://127.0.0.1:9090/put/roadcondition" -H "Content-Type: application/json" -d @data/upload_road_condition.json

Insert the weather information for 2022, while weather for 2023 will be inserted by API streaming
curl -X PUT "http://127.0.0.1:9090/put/weather2022" -H "Content-Type: application/json" -d @data/upload_weather.json
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

### Search

```bash

curl -XGET -k "https://127.0.0.1:9200/${index_name}/_search"\
  --header 'Content-Type: application/json'\
  --data '{
    "query": {
      "match_all": {}
	}
  }'\
  --user 'elastic:elastic' | jq '.'
```

### Insert Doc

```bash
curl -XPOST -k "https://127.0.0.1:9200/${index_name}/_doc/"\
  --header 'Content-Type: application/json'\
  --data '{
    "attr1": "value1",
    "attr2": "value2",
    "attr3": "value3"
  }'\
  --user 'elastic:elastic' | jq '.'
```

### Create Index

```bash
curl -XPUT -k 'https://127.0.0.1:9200/${index_name}' \
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
      "attr1": {
        "type": "keyword"
      },
      "attr2": {
        "type": "${type}"
      }
    }
  }
}' | jq '.'
```

### Delete Index

```
curl -XDELETE -k 'https://127.0.0.1:9200/<index-name>' --user 'elastic:elastic' | jq '.'
```

## Fission

### Function

```
fission function create --name <function-name> --env python --code <path/to/py>

fission function update --name <function-name> --code <path/to/py>

fission function test --name <function-name> | jq '.'

```

### Route

```
fission route create --url /<route-name> --function <function-name> --name <route-name> --createingress

curl "http://127.0.0.1:9090/<route-name>" | jq '.'
```

### Pkg

```
cd functions/<name>
zip -r <name>.zip .
mv <name>.zip ../

cd ../..

fission package create --sourcearchive ./functions/<name>.zip\
  --env python\
  --name <name>\
  --buildcmd './build.sh'

fission fn create --name <name>\
  --pkg <name>\
  --env python\
  --entrypoint "<name>.main"

fission route create --url /<name> --function <name> --name <name> --createingress


curl "http://127.0.0.1:9090/<name>" | jq '.'
```

### Deployment

#### Frequent Commands

If something wrong with package creation, please run:
`chmod +x build.sh`

```
fission specs init
< after creation of env/pkg/fn/route>
fission spec validate
fission spec apply --specdir specs --wait
```

```
fission function delete --name <name>
fission route delete --name <name>
fission pkg list
fission pkg delete --name <name>

fission function delete --name <name>
fission route delete --name <name>
fission pkg delete --name <name>
```

#### searchweather

- Create

```bash
cd backend/searchweather
zip -r searchweather.zip . -x "*.DS_Store"
mv searchweather.zip ../

cd ../..

fission package create --spec --sourcearchive ./backend/searchweather.zip\
  --env python\
  --name searchweather\
  --buildcmd './build.sh'

fission fn create --spec --name searchweather\
  --pkg searchweather\
  --env python\
  --configmap shared-data\
  --entrypoint "searchweather.main"\

fission httptrigger create --spec --method GET \
    --url "/searchweather/{StartDate}/{EndDate}" --function searchweather --name searchweather

curl "http://127.0.0.1:9090/searchweather/2024-03-01/2024-03-11"
```

- Delete

```
fission function delete --name searchweather
fission pkg delete --name searchweather
fission route delete --name searchweather
```

#### search

```bash
cd backend/search
zip -r search.zip . -x "*.DS_Store"
mv search.zip ../

cd ../..

fission package create --spec --sourcearchive ./backend/search.zip\
  --env python\
  --name search\
  --buildcmd './build.sh'

fission fn create --spec --name search\
  --pkg search\
  --env python\
  --configmap shared-data\
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

#### extract

```bash
cd functions/extract
zip -r extracta.zip . -x "*.DS_Store"
mv extracta.zip ../

cd ../..

fission package create --spec --sourcearchive ./backend/extract.zip\
  --env python\
  --name extract\
  --buildcmd './build.sh'

fission fn create --spec --name extract\
	--code ./backend/extract/extract.py\
  --env python\

fission route create --spec --url /extract/{Indexname} --function extract --name extract --createingress

fission spec apply --specdir specs --wait

curl "http://127.0.0.1:9090/extract/weather"
```

- Delete

```
fission function delete --name extract
fission route delete --name extract
fission pkg delete --name extract
```

#### put

```bash
cd backend/put
zip -r put.zip . -x "*.DS_Store"
mv put.zip ../

cd ../..

fission package create --spec --sourcearchive ./backend/put.zip\
  --env python\
  --name put\
  --buildcmd './build.sh'

fission fn create --spec --name put\
  --pkg put\
  --env python\
  --configmap shared-data\
  --entrypoint "put.main"\

fission route create --spec --method PUT --url /put/{Indexname} --function put --name put --createingress

fission spec apply --specdir specs --wait

curl -XPUT "http://127.0.0.1:9090/put/weather"
```

- Delete

```
fission function delete --name put
fission route delete --name put
fission pkg delete --name put
```

## Testing

```bash
python -m unittest tests.test_api.TestAPIEndpoints.test_search_by_index
```
