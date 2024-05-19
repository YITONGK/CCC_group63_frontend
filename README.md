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
  [Victorian Government Data Directory](https://discover.data.vic.gov.au/)
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
'population': "http://127.0.0.1:9090/search/population",
'accidents': "http://127.0.0.1:9090/search/accidents",
'accident_locations': "http://127.0.0.1:9090/search/accident_locations",
'geoinfo': "http://127.0.0.1:9090/search/geoinfo",
'roadcondition': "http://127.0.0.1:9090/search/roadcondition",
'searchweather': "http://127.0.0.1:9090/searchweather/{Startdate}/{Enddate}"
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
curl -XDELETE -k 'https://127.0.0.1:9200/accidents' --user 'elastic:elastic' | jq '.'
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
cd functions/test
zip -r test.zip .
mv test.zip ../

cd ../..

fission package create --sourcearchive ./functions/test.zip\
  --env python\
  --name test\
  --buildcmd './build.sh'

fission fn create --name test\
  --pkg test\
  --env python\
  --entrypoint "test.main"

fission route create --url /test --function test --name test --createingress


curl "http://127.0.0.1:9090/test" | jq '.'
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
fission function delete --name test
fission route delete --name test
fission pkg delete --name test
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
  --entrypoint "searchweather.main"

fission httptrigger create --spec --method GET \
    --url "/searchweather/{StartDate}/{EndDate}" --function searchweather --name searchweather

fission httptrigger create --spec --method GET \
    --url "/searchweather?sdate={StartDate}&edate={EndDate}" --function searchweather --name searchweather

curl "http://127.0.0.1:9090/searchweather/2024-03-01/2024-03-11" | jq '.'
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
