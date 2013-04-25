# WIP
Planning on putting some simple REST API endpoints up for educational purposes. Now, where are those "under construction" animated gifs from the 90's.... oh, and midi music. Ghatta have midi music.

## Guides followed
* https://devcenter.heroku.com/articles/django#prerequisites
* https://docs.djangoproject.com/en/1.5/intro/tutorial01/

## Setup
Currently hard coded to use postgres with user 'seth', no password, and database name 'seth' for local development. If deployed to Heroku, set the DATABASE URL to your postgres instance.

### Endpoints
Current endpoints:
* /lists/getlist/{{sender}} - gets all emails in sender's list
* /lists/getlist/{{sender}}/subscribes - gets all subscribed emails
* /lists/getlist/{{sender}}/unsubscribes - gets all unsubscribed emails
* /lists/getlist/{{sender}}/add/{{email}} - adds email to sender's list (automatically appends @example.com)
* /lists/getlist/{{sender}}/delete/{{email}} - deletes email from sender's list (automatically appends @example.com)
* /lists/getlist/{{sender}}/update_subscription/{{email}}/{{yes|no}} - changes the subscription status
* /lists/getlist/{{sender}}/update_subscription/{{email}}/ - if missing yes|no, it will show that email's subscription status on the given list

### Seed data
$ python manage.py help populate;
Usage: manage.py populate [options] drop

$ python manage.py populate;
Populates database with seed data of Senders A, B, C, D, and E. Populates 200 email addresses spread between them with some addresses shared and some unsubscribed.

$ python manage.py populate drop;
drops data from the database prior to populating the database as normal
