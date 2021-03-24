# Food API

## Description

This is an API that is used to store Recipes and Ingredients,
it is part of a large platform of applications that exist to
create personal recipes.

The purpose of this application is to store recipes and ingredients.

## How to run this app

### Docker

To run this application in docker as if it were in production use the following instructions:

1. Create an .env file to run the application. It should have the following format:

    ```env
    DB_HOST="0.0.0.0"
    DB_PORT="5432"
    DB_NAME="food"
    DB_USER="root"
    DB_PASSWORD="password"
    DEBUG=false
    ```

2. Run `docker-compose up -d pg_db app`

### Local

To run this application locally use the following instructions:

1. `python -m venv env`
2. `source env/bin/activate
3. Use `env.example` to create an .env file to run the application. It should have the following format:

    ```env
    DB_HOST="0.0.0.0"
    DB_PORT="5432"
    DB_NAME="food"
    DB_USER="root"
    DB_PASSWORD="password"
    DEBUG=true
    ```

4. `docker-compose up -d pg_db`
5. `uvicorn app.main:app --reload --host 0.0.0.0 --port <your-port-number-here>`

## Running Tests

To run the application tests use the following instructions:

1. Create an .env file to run the application. It should have the following format:

    ```env
    DB_HOST="0.0.0.0"
    DB_PORT="5432"
    DB_NAME="food"
    DB_USER="root"
    DB_PASSWORD="password"
    DEBUG=false

2. 

## How to access Open API docs

To access Open API docs please go to the following route:

*http://localhost:3000/docs*
