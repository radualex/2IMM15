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


### API

An API exposing 1 endpoint has been added as well.
 
Start the server (http://localhost:3000)
```
python server.py 
```

Make GET request to http://localhost:3000/query/[query] to get a list of video ids according to the query.

Example of a request:
```
GET http://localhost:3000/query/"app or facebook" 
```

### Main
The Schema.sql file from 'Crawler' folder has to be imported in postgreSQL first as this is the schema we use for the system.

In the 'Crawler' folder, a main.py file exists. This can be used to perform the crawling and indexing as these functionalities are not present in the frontend. Therefore,

```
python main.py --q=<search query for youtube> --location=<geolocation> --location-radius=<radius in km> --i
```

will retrieve the raw data based on the query and will create the indexer.

After that, the server.py in 'Crawler' folder can be called to start the backend and the server.py in 'client' folder can be called to start the frontend.
