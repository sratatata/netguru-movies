# simple-movies-database

## Assigment

### Movie database
We’d like you to build simple REST API for us - a basic movie database interacting with external API. Here’s full specification of endpoints that we’d like it to have:

* POST /movies:
    * Request body should contain only movie title, and its presence should be validated.
    * Based on passed title, other movie details should be fetched from http://www.omdbapi.com/ (or other similar, public movie database) - and saved to application database.
    * Request response should include full movie object, along with all data fetched from external API.
* GET /movies:
    * Should fetch list of all movies already present in application database.
    * Additional filtering, sorting is fully optional - but some implementation is a bonus.
* POST /comments:
    * Request body should contain ID of movie already present in database, and comment text body.
    * Comment should be saved to application database and returned in request response.
* GET /comments:
    * Should fetch list of all comments present in application database.
    * Should allow filtering comments by associated movie, by passing its ID. 

### Rules & hints​

* Plan a list of todos/tasks in before coding
* use github, comments should be understanable and done often
* use node.js and express.js
* use mysql as database in docker container (please find https://betterprogramming.pub/how-to-use-mysql-with-node-js-and-docker-7dfc10860e7c) - for convinience not for learning purpose.
* don't use console.log for debuging, use only VSC built in debugger
* Basic tests of endpoints and their functionality are optional. Their exact scope and form is left up to you.

## About 
Fill out

### For the reviewer
- For your convenience I left source branches for pull requests without squash so you can check 
what problems I was struggling with. 

## Setup 

### New setup
Fill out

### Additional Configuration
Fill out if needed
#### OMDB Database
Fill out (example for python below).

See [www.omdbapi.com](http://www.omdbapi.com) for more details

By default `settings.py` is looking for environment variable OMDB_SECRET with OMDB api-key set.
Please set mentioned variable: 
```
set OMDB_SECRET=<your_api_key>
``` 
or insert it into `settings.py` directly.
```
# Custom secret necessary to access to OMDB database
# See http://www.omdbapi.com/apikey.aspx
# OMDB_SECRET = os.environ.get('OMDB_SECRET')
OMDB_SECRET = <your_api_key>
```

Api key could be obtained here on [omdb website](http://www.omdbapi.com/apikey.aspx)

## Usage (Example)
Fill out your own
### Listing movies:
```
# using httpie
$> http GET https://localhost/movies
```

Query Parameters:
* (optional) title:string - filter movies with title `LIKE` value
* (optional) year:int - filter movies with year exact equal value
* (optional) sort_by:string - choose single column to generic_sort by (default order is `asc`)
* (optional) order:string - choose `asc` or  `desc`  

> Please notice that unknown parameters would disable all filtering
> Filters could be used together

Example output: 
```
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Connection: keep-alive
Content-Length: 105
Content-Type: application/json
Date: Mon, 30 Jul 2018 21:21:02 GMT
Server: gunicorn/19.9.0
Vary: Accept, Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

[
    {
        "title": "Inception", 
        "year": "2010"
    }, 
    {
        "title": "Matrix", 
        "year": "1993–"
    }
]
```

Example with filters: 
```
# using httpie
$> http GET https://localhost/movies?year=2010
```

Outputs:

```
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Connection: keep-alive
Content-Length: 105
Content-Type: application/json
Date: Mon, 30 Jul 2018 21:21:02 GMT
Server: gunicorn/19.9.0
Vary: Accept, Cookie
Via: 1.1 vegur
X-Frame-Options: SAMEORIGIN

[
    {
        "title": "Inception", 
        "year": "2010"
    }
]
```

Statuses:
* 200 - ok - List of movies was returned

### Posting movies:
```
# using httpie
$> http POST https://localhost title="Psy"
```
Json body:
```
   { "title":"Psy" }
```

Example output: 

```
HTTP 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "title": "Psy",
    "year": "1989"
}
```

Statuses  
* 201 - created : movie was successfully added to database 
* 400 - bad request : title was empty or fetching data from external database was unsuccessful

### Listing comments:
```
# using httpie
$> http GET localhost/comments
```

Query Parameters:
* (optional) movie:int - enable comment filtering by movie id

> Please note that filtering is enabled by query parameter because requested 
> in the assignment resource url is not nested (`GET: /comments`).  
> Alternately could be done `GET: /movies/<id:int>/comments`

Example output: 
```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 2,
        "movie": 4,
        "body": "Amazing!"
    },
    {
        "id": 3,
        "movie": 4,
        "body": "Sink!"
    }
]
```

Statuses:
* 200 - ok - List of comments was returned

### Posting comments:
```
# using httpie
$> http POST https://localhost/comments movie=4 body="Amazing!"
```

Json body:
```
   { "movie":4, body:"Amazing!" }
```

Example output

```
HTTP 201 Created
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 2,
    "movie": 4,
    "body": "Amazing!"
}
```

Statuses  
* 201 - created : comment was added to database
* 400 - bad request : movie was not found or comment body was empty
