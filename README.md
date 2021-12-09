# django-kafka-by-db
use kafka like database in django toy project

```
python3 -m venv env
. env/bin/activate
pip install django djangorestframework request
django-admin startproject DjangoKafka
cd DjangoKafka
python manage.py startapp restapi

````

you have to install confluent-cli   
[https://docs.confluent.io/platform/current/kafka-rest/quickstart.html](https://docs.confluent.io/platform/current/kafka-rest/quickstart.html)

and start confluent rest-api
```$ confluent local services kafka-rest start```
