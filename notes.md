### The project is built using the following technologies:
- **Django/Django REST Framework**: The main backend app.
- **Celery**: An asynchronous task queue/job queue to process long-running tasks in the background, such as detecting faces on images and drawing bounding boxes. Such kind things could take time and regular HTTP request could be blocked.
- **Redis**: The message broker for Celery.
- **PostgreSQL**: The main database.
- **MinIO**: A file storage service.

### Postgres 
I prefer PostgreSQL for its features, but it's not strictly necessary for this project. SQLite could suffice as an alternative.
#### DB structure
The database includes a model to store both the original and processed images, along with the status of the image processing. The original images are saved in the database, and a tag field has been introduced to manage image serving instead of exposing their media folder paths.

### Celery
As previously mentioned, Celery is ideal for executing long-running tasks. Given the complexity of face recognition, Celery ensures robust and reliable task processing.

### MinIO
MinIO is chosen for its simplicity and efficiency as a file storage solution, offering a viable alternative to AWS S3. Its use facilitates future project scalability, such as allowing multiple services to share access to the same storage resources.

### Face recognition
I've used the OpenCV package, since it's open source and comes with pre-trained models for face detection.

### Docker
I've used general tag of docker images, but it's better to use the image with sha256 hash to be able to reproduce bugs and errors