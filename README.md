# CCC_group63_frontend

#### getweather

- Create
```
cd functions/getweather
zip -r getweather.zip .
mv getweather.zip ../

cd ../..

fission package create --sourcearchive ./functions/getweather.zip\
  --env python\
  --name getweather\
  --buildcmd './build.sh'
  
fission fn create --name getweather\
  --pkg getweather\
  --env python\
  --entrypoint "getweather.main"
  
fission route create --url /getweather --function getweather --name getweather --createingress


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
```
cd functions/searchweather
zip -r searchweather.zip .
mv searchweather.zip ../

cd ../..

fission package create --sourcearchive ./functions/searchweather.zip\
  --env python\
  --name searchweather\
  --buildcmd './build.sh'
  
fission fn create --name searchweather\
  --pkg searchweather\
  --env python\
  --entrypoint "searchweather.main"
  
fission route create --url /searchweather --function searchweather --name searchweather --createingress


curl "http://127.0.0.1:9090/searchweather" | jq '.'
```
- Delete
```
fission function delete --name searchweather
fission route delete --name searchweather
fission pkg delete --name searchweather
```

