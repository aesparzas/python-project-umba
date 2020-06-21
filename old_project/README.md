# Umba Backend Homework Assignment


## Introduction

Umba is building out a banking platform for the 2 billion people in the world that do not have a
bank account. More and more of these customers are getting smartphones, so our mission is to
use the disruptive force of pocket computing to deliver better and cheaper services to our
customers.

In this assignment you are expected and encouraged to use Google and Stack Overflow - because we all do in real life 😃

The assignment consists of the the creation of a money transfer service where users can
send money to other Umba users.

## Bootstrapped project

To save time on setting up a project we have provided this project that already has User creation, tests and local environment set up. This is done using Docker, Python, Flask and Postgres.

You do not have to use this project but it will likely save you a lot of time. If you do not use this project please ensure it is as easy to run your project locally. 

## Requirements

- Python is preferred, but you can also write this in any one of these supported languages: Ruby, JS or Go.
- This project should be able to run with a one line command (i.e. make up, docker run etc - whatever works for you) without required knowledge if the internal dependencies
- You should use persistence
- Tests are required
- Authentication is optional

## Assignment

Create a REST API that can perform these functions:

- Create a user with a phone number and name
- Retrieve a user
- Retrieve all users
- Create a transaction with amount, currency, the user who sent it and the user who received it
- Retrieve a users transactions
- Retrieve a feed of all transactions


## API Definition
GET a single user
/users/<id>

### Error Responses

- No user with that ID - Http Status 404

### Successful response

```
{
    "id": 1,
    "phone_number": "+19344367546",
    "name": "Dave Simpson"
}
```

## Bonus

- What way would you extend this service?
    - Can you think of more interesting features this service can have?
- There will be a UI built to show this feed, what else would you return in the feed objects to assist the front end engineer building this service?
- Do you have any scaling concerns with this service

## Installation
- Ensure Docker is installed on your machine
- Clone this project
- Run `make up`
- Run `make run_migrations`
- Visit [this link](http://localhost:5000/api/v1/test) and you should see "Project setup successfully!" in your default browser


### Running tests 
- Run `make tests`

### Developing
- `make create_new_migration` - this adds a new migration file (in migrations/versions) based on changes to the model file
- `make run_migrations` - this will execute any migrations that have not been run before (Alembic stores the last migration ID that was ranin the DB)
- `make restart_app` - this restarts the App running inside the container 
- `make api_shell` - this gives you a shell inside the API container (if needed)
- `make postgres_shell` - this gives you a shell inside the Postgres container 

