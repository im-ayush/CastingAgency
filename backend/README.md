# Casting Agency API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Its recommend to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

	```bash
	pip install -r requirements.txt
	```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
	With Postgres running, restore a database using the casting_agency.psql file provided. From the backend folder in terminal run:
	```bash
	psql -U postgres casting_agency > casting_agency.psql
	```

## Running the server

	From within the `backend` directory first ensure you are working using your created virtual environment.

	To run the server, execute:

	```bash
	export FLASK_APP=app.py
	export FLASK_ENV=development
	flask run
	```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

## Testing
	To run the tests, run
	```
	dropdb casting_agency_test
	createdb casting_agency_test
	python test.py
	```

## Documentation
```
Casting Agency API Backend
	The users are able to perform limited tasks only based on the different roles.
	1.Role : Casting Assistant
		- can view the list of all the movies and actors, and related details.

	2.Role : Casting Director
		- has all the permissions of a Casting Assistant
		- can add and delete the actors
		- can modify actor, movie details

	3.Role : Executive Producer
		- has all the permissions of a Casting Director
		- can add and delete the movies

## Getting Started
	Prerequisites & Installation
		Developers using this project should already have Python3, pip and node installed on their local machines.

	Backend
		The requirements.txt file in backend/ folder contains all the packages required by this project. To install those packages run 'pip install requirements.txt' from the backend/ folder.

		To get the application running run the following commands:
			For bash:
				export FLASK_APP=app.py
				export FLASK_ENV=development
				flask run

			For command prompt:
				set FLASK_APP=app.py
				set FLASK_ENV=development
				flask run

		These commands put the application in development and directs the application to use the app.py file in backend/ folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.

		The application runs on http://127.0.0.1:5000/ by default.

## Note:
All the endpoints except '/', require a bearer token containing the corresponding permissions required for each endpoint.

## API Reference
	Endpoints
		GET '/'
			- Fetches a JSON object with key success, just to be sure that whether API is up and running.


		GET '/actors'
			- Request Arguments: page (Optional)
				- actor list is paginated and are displayed 10 results per page
				- value of page argument value can be used to more results
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- actors : list of actors details as a JSON object
				- total_actors : integer value representing count of actors in the database

			-	Request: curl -H "Authorization: Bearer <Auth0_Token>" http://127.0.0.1:5000/actors
			-	Response: {
									  "actors": [
									    {
									      "age": "14",
									      "gender": "M",
									      "id": 5,
									      "name": "Devashish"
									    },
									    {
									      "age": "55",
									      "gender": "M",
									      "id": 19,
									      "name": "Ayush"
									    },
									    {
									      "age": "45",
									      "gender": "M",
									      "id": 22,
									      "name": "Abhay"
									    }
									  ],
									  "success": true,
									  "total_actors": 3
									}


		GET '/actors/<actor_id>'
			- Request Arguments:
					- URL parameter : actor_id
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- actor : details as an actor with id=actor_id as a JSON object
				- movies : list of movies of which actor has been a part of
				- total_movies : integer value representing count of movies of which actors has been a part of

			-	Request: curl -H "Authorization: Bearer <Auth0_Token>" http://127.0.0.1:5000/actors/19
			-	Response: {
									  "actor": {
									    "age": "55",
									    "gender": "M",
									    "id": 19,
									    "name": "ayush"
									  },
									  "movies": [
									    {
									      "id": 4,
									      "release_date": "22 June, 2022",
									      "title": "WWW"
									    }
									  ],
									  "success": true,
									  "total_movies": 1
									}


		POST '/actors'
			- Creates an actor
			- Request Arguments:
					- A JSON object with keys
						- name : string value for actor name
						- age : string value for actor age
						- gender : string value for actor's gender
						- movies (Optional) : string value containing comma separated movie ids
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- total_actors : integer value representing count of actors in the database

				Request: curl -H "Authorization: Bearer <Auth0_Token>" -H "Content-Type: application/json" -d "{\"name\":\"Name 1\", \"age\":\"28\", \"gender\":\"M\"}" -X "POST" http://127.0.0.1:5000/actors
				Response: {
									  "success": true,
									  "total_actors": 14
									}


		PATCH '/actors/<actor_id>'
			- Update an actor details
			- Request Arguments:
				- URL parameter : actor_id
				- A JSON object with keys (All Optional)
					- name : string value for actor name
					- age : string value for actor age
					- gender : string value for actor's gender
					- movies (Optional) : string value containing comma separated movie ids
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- updated : integer value representing the id of actor whose details have been updated

				Request: curl -H "Authorization: Bearer <Auth0_Token>" -H "Content-Type: application/json" -d "{\"age\":\"28\"}" -X "POST" http://127.0.0.1:5000/actors/40
				Response: {
									  "success": true,
									  "updated": 40
									}


		DELETE '/actors/<actor_id>'
			- Deletes an actor
			- Request Arguments:
				- URL parameter : actor_id
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- deleted : integer value representing the id of actor which have been deleted
				- total_actors : integer value representing count of actors in the database

				Request: curl -H "Authorization: Bearer <Auth0_Token>" -X "DELETE" http://127.0.0.1:5000/actors/35
				Response: {
									  "deleted": 35,
									  "success": true,
									  "total_actors": 13
									}


		GET '/movies'
			- Request Arguments: page (Optional)
				- movies list is paginated and are displayed 10 results per page
				- value of page argument value can be used to more results
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- movies : list of movies details as a JSON object
				- total_movies : integer value representing count of movies in the database

			-	Request: curl -H "Authorization: Bearer <Auth0_Token>" http://127.0.0.1:5000/movies
			-	Response: {
									  "movies": [
									    {
									      "id": 4,
									      "release_date": "22 June, 2022",
									      "title": "WWW"
									    },
									    {
									      "id": 5,
									      "release_date": "22 June, 2022",
									      "title": "WWE"
									    },
									    {
									      "id": 2,
									      "release_date": "22 June, 2021",
									      "title": "ABC"
									    }
									  ],
									  "success": true,
									  "total_movies": 3
									}


		GET '/movies/<movie_id>'
			- Request Arguments:
					- URL parameter : movie_id
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- movie : details as an actor with id=movie_id as a JSON object
				- actors : list of actors casted in the movie
				- total_actors : integer value representing count of actors casted in the movie

			-	Request: curl -H "Authorization: Bearer <Auth0_Token>" http://127.0.0.1:5000/movies/2
			-	Response: {
									  "actors": [
									    {
									      "age": "14",
									      "gender": "M",
									      "id": 5,
									      "name": "Devashish"
									    }
									  ],
									  "movie": {
									    "id": 2,
									    "release_date": "22 June, 2021",
									    "title": "ABC"
									  },
									  "success": true,
									  "total_actors": 1
									}


		POST '/movies'
			- Creates an movie
			- Request Arguments:
					- A JSON object with keys
						- title : string value for movie title
						- release_date : release date of movie (YYYY-MM-DD)
						- actors (Optional) : string value containing comma separated actor ids
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- total_movies : integer value representing count of movies in the database

				Request: curl -H "Authorization: Bearer <Auth0_Token>" -H "Content-Type: application/json" -d "{\"title\":\"Movie 1\", \"release_date\":\"2022-02-24\"}" -X "POST" http://127.0.0.1:5000/movies
				Response: {
									  "success": true,
									  "total_movies": 12
									}


		PATCH '/movies/<movie_id>'
			- Update an movie details
			- Request Arguments:
				- URL parameter : actor_id
				- A JSON object with keys (All Optional)
					- title : string value for movie title
					- release_date : release date of movie (YYYY-MM-DD)
					- actors (Optional) : string value containing comma separated actor ids
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- updated : integer value representing the id of movie whose details have been updated

				Request: curl -H "Authorization: Bearer <Auth0_Token>" -H "Content-Type: application/json" -d "{\"release_date\":\"2023-08-20\"}" -X "PATCH" http://127.0.0.1:5000/movies/23
				Response: {
									  "success": true,
									  "updated": 23
									}


		DELETE '/movies/<movie_id>'
			- Deletes an movie
			- Request Arguments:
				- URL parameter : movie_id
			- Returns a JSON object with keys-
				- success : a boolean value representing the success/failure of the request
				- deleted : integer value representing the id of movie which have been deleted
				- total_movies : integer value representing count of movies in the database

				Request: curl -H "Authorization: Bearer <Auth0_Token>" -X "DELETE" http://127.0.0.1:5000/movies/17
				Response: {
									  "deleted": 17,
									  "success": true,
									  "total_movies": 11
									}
