# netguru-movies

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

* Your goal is to implement REST API in Django, however you're free to use any third-party libraries and database of your choice - sharing your reasoning behind choosing them is welcome!
* At least basic tests of endpoints and their functionality are obligatory. Their exact scope and form is left up to you.
* The application's code should be kept in a public repository so that we can read it, pull it and build it ourselves. Remember to include README file or at least basic notes on application requirements and setup - we should be able to easily and quickly get it running.
* Written application must be hosted and publicly available for us online - we recommend Heroku.

## About 
As mentioned in assigment section above application provides simple rest api for issuing comments/reviews
of movies from external database. 

Solution is based on django-rest framework which is extending django capabilities with many 
rest friendly modules. For more information check project [website](http://www.django-rest-framework.org/). 

Note:
- For sake of simplicity and due to non production character of this application, 
debug mode in django is not diabled on production environment. 

### For the reviewer
- For your convenience I left source branches for pull requests without squash so you can check 
what problems I was struggling with. 

## Setup 

### New setup
As it was requested application is prepared to use with heroku services. 

1. Follow [heroku](https://devcenter.heroku.com/articles/getting-started-with-python) manual to setup your account 
2. Create new application as it's descirbed in [manual](https://devcenter.heroku.com/articles/getting-started-with-python)
3. Deploy application: 
    ```bash
    $> git push heroku master 
    ```
4. Run migration scripts: 
    ```bash
    $> heroku run python manage.py migrate
    ```
5. Now you can visit deployed application
    ```bash
    $> heroku open
    ```
    
Note:
- postgresDb would be added automatically, if not add it manually 

### Existing setup
Apllication is already configured to deploy to domain: `sratatata-movies.herokuapp.com`
automatically after push to `master` branch so you can visit it on mentioned url. 

If changes needed just issue pull request to master branch, after changes accepted, they would 
go live after passing tests. 

### Additional Configuration

#### OMDB Database
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

## Usage


- To get description of available methods please refer main page with interactive [api-browser](https://sratatata-movies.herokuapp.com/). 
    ```
    https://sratatata-movies.herokuapp.com/
    ```