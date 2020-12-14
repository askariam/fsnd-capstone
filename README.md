# Full Stack Capstone API Project - Casting Agency

This project is to build an API for Casting Agency that allows 3 different types of users to view and manage movies and actors. The project package contains of API applications that is deployed online and also can be tested locally. There are 3 roles for this API: Casting Assistant, Casting Director, and Executive Producer. The different functionalities offered by the API are:

1. Display all movies - All roles
2. Display all actors - All roles
3. Update an actor - Producer and Director
4. Update a movie - Producer and Director
5. Post a new actor - Producer and Director
6. Post a new movie - Producer Only
7. Delete an actor - Producer and Director
8. Delete a movie - Producer Only

## Getting Started

### Installing Dependencies

Once you have your virtual environment setup and running, install dependencies by running the command:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql capstone < capstone-test.pgsql
```
Or just use the manage.py file to migrate the database.

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### Running the server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
export FLASK_APP=app
flask run --reload
``` 

## Testing
Make sure the test database environment variable is set:
Uncomment the below line in the setup.sh:
export DATABASE_URL='postgres://localhost:5432/capstone_test' #comment this line if not using test_app.py
and run again:
```
source setup.sh
```


To run the tests, run
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < capstone-test.pgsql
python test_app.py
```

## API Reference

### Introduction

- Base URL: currently the API is published online on: `https://fsnd-askari.herokuapp.com/` [https://fsnd-askari.herokuapp.com/](https://fsnd-askari.herokuapp.com/)
and can be used locally only on `http://localhost:5000/` [http://localhost:5000/](http://localhost:5000/)
- Currently the API requires authentication. The tokens are in the attached posman collections and also provided in the env variables.

### Endpoints

#### GET /movies
- General: returns movies
- Sample: `curl --location --request GET 'localhost:5000/movies'`


#### GET /actors
- General: returns all actors
- Sample: `curl --location --request GET 'localhost:5000/actors'`

#### POST /movies
- General: add a new movie
- Sample: 
```
curl --location --request POST 'localhost:5000/movies' \
--data-raw '{
    "title": "Udacity Film",
    "release_date": "2020-11-11"
}'
```

#### POST /actors
- General: add a new actor
- Sample: 
```
curl --location --request POST 'localhost:5000/actors' \
--data-raw '{
    "name": "Udacity Test Actor",
    "age": 26,
    "gender": "male"
}'
```

#### DELETE /movies/<int:id>
- General: delete a movie
- Sample: `curl --location --request DELETE 'localhost:5000/movies/2'`


#### DELETE /actors/<int:id>
- General: delete an actor
- Sample: `curl --location --request DELETE 'localhost:5000/actors/2`


#### PATCH /movies/<int:id>
- General: update a movie
- Sample: 
```
curl --location --request PATCH 'localhost:5000/movies/1' \
--data-raw '{
    "title": "Udacity Test Film - Changed",
    "release_date": "2020-12-12"
}'
```

#### PATCH /actors/<int:id>
- General: update an actor
- Sample: 
```
curl --location --request PATCH 'localhost:5000/actors/1' \
--data-raw '{
    "name": "Udacity Actor - Changed",
    "age": 26,
    "gender": "male"
}'
```

### Error Handling
- The application returns 5 different types of errors: 400, 404, 405, 401 and 422

```

