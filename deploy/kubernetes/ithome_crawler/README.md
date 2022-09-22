```
helm install ithome_crawler . \
    --set schedule="* * * * *" \
    --set env.mongo.host=mongodb://localhost:27017 \
    --set env.mongo.db=ithome_ironman
```