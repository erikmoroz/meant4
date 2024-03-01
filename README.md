## Demo

This link contains a demo video of the project [Demo](https://drive.google.com/file/d/1JY-ngE5wVlzgrTuAnnFrqEfBGCsLnY4s/view?usp=sharing)

## What's Inside?

- **Django**: The backend application framework.
- **Celery**: An asynchronous task queue/job queue based on distributed message passing.
- **Redis**: The message broker for Celery.
- **PostgreSQL**: The primary database for storing application data.
- **MinIO**: A high-performance file storage service.

## Getting Started

### Running the Project

To get the project up and running, follow these steps from the root directory:

```shell
docker-compose -f docker-compose.yml up --build
```

This command sets up the project, runs the necessary services, creates the database, executes migrations, and loads initial fixtures, including a default admin user for the Django admin panel.

**Default admin user**:
```
username: meant4
password: meant4
```

## How to run tests

To run the automated tests for this project, follow these steps:

1. Start the services:
```
docker-compose -f docker-compose.yml up -d
```
2. Log in to the API container:
```
docker-compose -f docker-compose.yml exec api bash
```
3. Execute the tests:
```
python manage.py test
```

## Endpoints

List of available endpoints

### Upload image

- **URL**: {host}/image
- **Method**: `POST`
- **Headers**:
  - `content-type: multipart/form-data`
- **Body**:
  - `file` - image file

### Download marked image

- **URL**: {host}/image/{image_name}
- **Method**: `GET`

### WebSocket Endpoint for Notifications

- **Connection type**: `WebSocket`
- **URL**: {host}/faces

### Django Admin Panel

- **URL**: {host}/admin
- **Credentials**:
  - `username: meant4`
  - `password: meant4`

## File Structure
```
--|
  |-- .gitignore
  |-- .env (Configuration file with environment variables)
  |-- docker-compose.yaml
  |-- Dockerfile
  |-- entrypoint.sh
  |-- notes.md
  |-- README.md
  |-- api/
      |-- faces/ (API endpoints)
      |-- project/ (Django settings, WSGI, URL routing)
      |-- fixtures/ (Database fixtures)
      |-- manage.py (Django’s command-line utility for administrative tasks)
      |-- requirements.txt
  |-- demo/ (Demo files)
```