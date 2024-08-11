# Train Station API

Train Station API is a Django REST Framework project that provides an API for managing train station data, including trains, routes, stations, crew, tickets, and journeys.


## Features

- JWT Authentication
- Admin panel
- Documentation
- Managing Train Station(creating, retrieving and updating all the models)
- Search and ordering
- Adding images for trains at **/api/train-station/trains/{int: pk}/upload-image/**


## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)

## Prerequisites

- Python 3.9
- Docker
- Docker Compose
- PostgreSQL

## Setup

1. **Create a `.env` file:**

   Create a `.env` file in the root directory of the project and add your environment variables. Example:

    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DB_NAME=train_station_db
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=db
    DB_PORT=5432
    ```

2. **Ensure Docker Compose configuration:**

   Your `docker-compose.yml` should be configured to connect to the PostgreSQL database and handle media files. Verify that your `docker-compose.yml` file includes the necessary configurations.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Yuruch/train-station-api.git
    cd train-station-api
    ```

2. **Build and start the Docker containers:**

    ```bash
    docker-compose up --build
    ```

   This command will build the Docker images and start the containers for the Django application and PostgreSQL database.

3. **Create a superuser:**

    ```bash
    docker-compose exec app python manage.py createsuperuser
    ```
4. **Load data**
    ```bash
    docker-compose exec app python manage.py loaddata fixtures.json
    ```


## Usage

1. **Start the development server:**

    ```bash
    docker-compose up --build
    ```

2. **Access the API:**

   The API will be available at `http://127.0.0.1:8001/`. You can use tools like Postman or curl to interact with the API.

3. **Access the Django Admin Interface:**

   The admin interface will be available at `http://127.0.0.1:8001/admin/`.
4. **To obtain JWT tokens you should go to /user/token/**

    You can obtain access to all the pages using access token just add it to headers
5. You can also register new account using POST request to /user/register/



## API Documentation

- **OpenAPI Schema:**
  - `GET /api/schema/`

- **Swagger UI:**
  - `GET /api/schema/swagger-ui/`

- **ReDoc:**
  - `GET /api/schema/redoc/`

These endpoints provide interactive documentation and schema definitions for the API.
## Testing

To run tests, use the following command:

```bash
docker-compose exec app python manage.py test
