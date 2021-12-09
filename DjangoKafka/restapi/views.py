
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
import os
import requests

TOPICNAME="djangokafka"
CLIENTNAME="kafkaclient"

class manage_rest(APIView):
    def RunRestAPI():
        os.system('confluent local services kafka-rest start')
    def get(self, request):
        # make consumer
        headers = {
             'Content-Type': 'application/vnd.kafka.v2+json',
        }
        data = f'{"name": {CLIENTNAME}, "format": "json", "auto.offset.reset": "earliest"}'
        response = requests.post(f'http://localhost:8082/consumers/{CLIENTNAME}', headers=headers, data=data)
        # subscribe topic
        data = f'{"topics":[{TOPICNAME}]}'
        response = requests.post(f'http://localhost:8082/consumers/{CLIENTNAME}/instances/{CLIENTNAME}/subscription', headers=headers, data=data)
        data = '{ "partitions": [{"topic":'+TOPICNAME+',"partition":0}]}'
        response = requests.post(f'http://localhost:8082/consumers/{CLIENTNAME}/instances/{CLIENTNAME}/positions/beginning', headers=headers, data=data)
        result = [d['value'] for d in response]
        



# curl -X POST \
#      -H "Content-Type: application/vnd.kafka.json.v2+json" \
#      -H "Accept: application/vnd.kafka.v2+json" \
#      --data '{"records":[{"key":"jsmith","value":{"name":"alarm clock","title":"cal"}},{"key":"htanaka","value":{"title":"batteries","name":"cal"}},{"key":"awalther","value":{"title":"bookshelves","name":"cal"}}]}' \
#      "http://localhost:8082/topics/goodboy"
# curl -X POST \
#      -H "Content-Type: application/vnd.kafka.v2+json" \
#      --data '{"name": "goodgirl", "format": "json", "auto.offset.reset": "earliest"}' \
#      http://localhost:8082/consumers/goodgirl

# curl -X POST \
#      -H "Content-Type: application/vnd.kafka.v2+json" \
#      --data '{"topics":["goodboy"]}' \
#      http://localhost:8082/consumers/goodgirl/instances/goodgirl/subscription 

# curl -X GET \
#      -H "Accept: application/vnd.kafka.json.v2+json" \
#      http://localhost:8082/consumers/goodgirl/instances/goodgirl/records 