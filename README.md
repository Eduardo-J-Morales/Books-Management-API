# Books Management API

A RESTful API for managing books, built with Flask, Flask-RESTful, SQLAlchemy, and secured with HTTP Basic Authentication.

> ⚡ **Note:** There is an explanation to install this API below for developers, however you don't need to install anything to try this API!  
> An online demo is available here: [Live API Deployment](https://books-management-api-production.up.railway.app)
> (See below for usage instructions and example requests.)

## Features 

- CRUD operations for book records
- Data validation for integrity
- Basic authentication for all endpoints
- Dockerized for easy deployment

## Technology Stack

- ![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
- ![Flask](https://img.shields.io/badge/Flask-2.x-green?logo=flask)
- ![Flask-RESTful](https://img.shields.io/badge/Flask--RESTful-API-lightgrey)
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=sqlalchemy)
- ![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
- ![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker)
- ![HTTP Basic Auth](https://img.shields.io/badge/Auth-Basic-lightgrey)

## Getting Started

### ❗ **Important:**  All endpoints require HTTP Basic Auth:

**Here is the default username and password for the authentication if you want to change this look for the "users" object in the app.py file.**

- **Username**: `admin`
- **Password**: `password123`

### API Endpoints

| Method | Endpoint             | Description          |
|--------|----------------------|----------------------|
| GET    | `/books`             | List all books       |
| POST   | `/books`             | Add a new book       |
| GET    | `/books/<book_id>`   | Get a specific book  |
| PUT    | `/books/<book_id>`   | Update a book        |
| DELETE | `/books/<book_id>`   | Delete a book        |

### Examples

1. #### GET (List all books)
    ```sh
    curl -u admin:password123 http://localhost:5000
    ```

2. #### POST (Add a new book)
    ```sh
    curl -u admin:password123 -X POST http://localhost:500 \
    -H "Content-Type: application/json" \
    -d '{
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "published_year": 1999,
        "isbn": "9780201616224"
      }'
    ```

3. #### GET (Get a specific book)
    ```sh
    curl -u admin:password123 http://localhost:5000/books/<book_id>
    ```

4. #### PUT (Update a book)
    ```sh
    curl -u admin:password123 -X PUT http://localhost:5000/books/<book_id> \
      -H "Content-Type: application/json" \
      -d '{
        "title": "The Pragmatic Programmer (Updated)",
        "author": "Andrew Hunt",
        "published_year": 1999,
        "isbn": "9780201616224"
      }'
    ```

5. #### DELETE (Delete a book)
   ```sh
   curl -u admin:password123 -X DELETE http://localhost:5000/books/<book_id>
   ```

## Installation

1. ### Clone the repo:
    ```sh
    git clone https://github.com/Eduardo-J-Morales/Books-Management-System.git
    cd Books-Management-System
     ```
    
2. ### Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
    
3. ### Run the app:
    ```sh
    python app.py
    ```
