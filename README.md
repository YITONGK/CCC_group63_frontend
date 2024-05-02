# CCC-Project

## ElasticSearch

### Accessing the ElasticSearch API and the Kibana User Interface

- Prequisite:
  - Before accessing Kubernetes services, an SSH tunnel to the bastion node has to be opened in a different shell and kept open. In addition, the `openrc` file has to be source and the kubeconfig file put under the `~/.kube` directory (see the READM in the `installation` folder for more details).

To access services on the cluster, one has to use the `port-forward` command of `kubectl` in a new terminal window.

```
kubectl port-forward service/elasticsearch-master -n elastic 9200:9200
```

To access the Kibana user interface, one has to use the `port-forward` command of `kubectl` (another terminal window):

```
kubectl port-forward service/kibana-kibana -n elastic 5601:5601
```

Test the ElasticSearch API:

```
curl -k 'https://127.0.0.1:9200/_cluster/health' --user 'elastic:elastic' | jq '.'
```

Test the Kibana user interface by pointing the browser to: `http://127.0.0.1:5601/` (the default credentials are `elastic:elastic`).

### Operations

#### Search

#### Create Index
##### accidents
```commandline
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
      "ACCIDENT_NO": {
        "type": "keyword"
      },
      "ACCIDENT_DATE": {
        "type": "date",
        "format": "yyyy-MM-dd"
      },
      "ACCIDENT_TIME": {
        "type": "text"
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

#### Delete Index

```
curl -XDELETE -k 'https://127.0.0.1:9200/accidents' --user 'elastic:elastic' | jq '.'
```

##### Road Surface
#### Create
```commandline
curl -XPUT -k 'https://127.0.0.1:9200/roadcondition' \
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
      "ACCIDENT_NO": {
        "type": "keyword"
      },
      "SURFACE_COND":{
        "type": "integer"
      },
      "SURFACE_COND_DESC":{
        "type": "text"
      },
      "SURFACE_COND_SEQ":{
        "type": "integer"
      }
    }
  }
}'  | jq '.'
```
#### Delete Index

```
curl -XDELETE -k 'https://127.0.0.1:9200/roadcondition' --user 'elastic:elastic' | jq '.'
```
## Fission
#### extractdata

- Create

```
cd functions/extractdata
zip -r extractdata.zip .
mv extractdata.zip ../

cd ../..

fission package create --sourcearchive ./functions/extractdata.zip\
  --env python\
  --name extractdata\
  --buildcmd './build.sh'

fission fn create --name extractdata\
  --pkg extractdata\
  --env python\
  --entrypoint "extractdata.main"

fission route create --url /extractdata --function extractdata --name extractdata --createingress


curl "http://127.0.0.1:9090/extractdata" | jq '.'
```

- Delete

```
fission function delete --name extractdata
fission route delete --name extractdata
fission pkg delete --name extractdata
```

#### combo

```
cd functions/combo
zip -r combo.zip .
mv combo.zip ../

cd ../..

fission package create --sourcearchive ./functions/combo.zip\
  --env python\
  --name combo\
  --buildcmd './build.sh'

fission fn create --name combo\
  --pkg combo\
  --env python\
  --entrypoint "combo.main"

fission route create --url /combo --function combo --name combo --createingress


curl "http://127.0.0.1:9090/combo" | jq '.'
```

- Delete

```
fission function delete --name combo
fission route delete --name combo
fission pkg delete --name combo
```
