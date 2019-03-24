# 2IMM15

use python 3.X.X (python 2 won't work)

### Packages
```
pip install nltk
pip install --upgrade google-api-python-client
pip install psycopg2
```

### Configuration
create config.ini file in the folder where config.py is located and add the following content (update accordingly):

```
[postgresql]
host=[host]
database=youtube (otherwise the Schema.sql has to be updated as well)
user=[username]
password=[password]

[youtube]
developerKey=[key from youtube]
youtube_api_service_name=youtube
youtube_api_version=v3
```

example for calling the youtube api to get data:
```
python getdata.py --q="computer science tutorials" --location="38.61048,-121.44730" --location-radius="1000km"
```

example for indexing: 
```
python index.py (--download : use first time in order to download nltk packages)
```


example for query processing:
```
python query.py --q "app"
```
