# Casting Agency Full Stack

# Full Stack Nano Degree - Capstone Project | Udacity

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The system tries to simplify and streamline the process.

Users are allowed to perform limited tasks only based on the following roles.
	1.Casting Assistant
	2.Casting Director
	3.Executive Produce

Casting Assistant
	- can view the list of all the movies and actors, and related details.

Casting Director
	- has all the permissions of a Casting Assistant
	- can add and delete the actors
	- can modify actor, movie details

Executive Producer
	- has all the permissions of a Casting Director
	- can add and delete the movies

## More Details

There are also separate READMEs for frontend and backend in:
1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)


## About the Stack

### Backend

The `./backend` directory contains a Flask server with a SQLAlchemy module to simplify the database operations.
Auth0 have been used for the authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete React.js frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)
