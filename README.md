# SMSService

This is an SMS Service to process inbound and outbound SMS requests
It is developed using Django Rest Framework with MySQL DataBase.
It is developed with Python 3.6.5 and Django 2.0.6.
It uses Basic Authentication for both the APIs

## Prerequisites
The requirements.txt file contains all the necessary packages that is needed for this application. The packages can be installed using the following command:
```
pip install -r requirements.txt
```
Install MySQL and create a DataBase named 'sms_service'

## Deployment on Local Machine
Once all the packages are installed, run the following commands sequentially:
```
python manage.py makemigrations
```
This command creates migration files from the models in Django ORM which are defined in /SMS/models.py

```
python manage.py migrate
```
This command creates the necessary tables in the DataBase with the table schema from the migration files that are created.

```
python manage.py collectstatic
```
This command packages all the HTML, CSS and JS files in static folder

```
python manage.py createsuperuser
```
This command creates a superuser profile to access the admin page(http://localhost:8000/admin/)

```
python manage.py runserver
```
This command is used to start the server

## API Docs
Both of the APIs are authenticated using Basic Authentication

### For Inbound SMS
```
POST http://13.232.95.21/inbound/sms/
```
#### Sample Request
```
{
	"from": "919876543210",
	"to": "919123456780",
	"text": "Hello Plivo"
}
```
#### Sample Response
```
{
    "message": "inbound sms is ok",
    "error": ""
}
```

### For Outbound SMS
```
POST http://13.232.95.21/outbound/sms/
```
#### Sample Request
```
{
	"from": "919876543210",
	"to": "919123456780",
	"text": "Hello Plivo"
}
```
#### Sample Response
```
{
    "message": "outbound sms is ok",
    "error": ""
}
```

## Testcases
Testcases have been added in SMS/tests/ folder.
Run the following command to run all the testcases:
```
python manage.py test SMS/tests
```
