# Simple Notification Service
A scalable notification app.

## Description

This is a Python-Flask based web app that sends periodic weekly and daily notifications using Celery.

(Given my experience with Django, it's almost certain that I could have written this app better and faster in Django.
However, since the objective is to create a 'Simple' service, I opted for Flask which is definitely lighter weight.)

## Stack
* Docker
* Postgresql
* Python 3.7
* Flask
* Celery/Redis

## To run this app locally
Run
```commandline
docker-compose up
```
Note: To apply the migrations to database, run 
```commandline
docker-compose run --rm web flask db upgrade
```

Load the page on your browser: http://127.0.0.1:8000/

## Key assumptions
* Notifications are only sent when they are due.
* Daily notifications are sent 24 hours after creation date or the last delivery date.
* Weekly notifications are sent 24 * 7 hours after creation date or the last delivery date.
* Notifications don't need to be sent at the "exact" planned delivery time.
   The celery scheduler runs every minute to identify and send the notifications that have become due.

## What this app doesn't do
* The app does not implement a robust html form validation for adding the notifications to the database.
* The app does not support CRUD operations for the notifications. At the moment users can only "add" notifications.
* The app does not really send any notifications. There is just a print statement to indicate where the code for a
specific implementation should be added.
* This app does not support "users". This would be a more realistic implementation but this one focuses more on
handling the queued tasks appropriately.
* Kubernetes not implemented.

## Key scalability features
* The web (flask) and celery worker are executed in separate containers for more flexible scalability.
* The celery beat scheduler works in a separate container.
* Celery tasks are created for each individual notification sent.

### Issues
* Tests cannot be run at the moment. To fix this, I need to change the file structure, but I ran out of time for a proper implementation.

