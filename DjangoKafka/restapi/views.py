import os
import json
import requests

from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.


TOPICNAME="djangokafka"
CLIENTNAME="kafkaclient"
class manage_rest(APIView):
    def RunRestAPI(self):
        os.system('confluent local services kafka-rest start')
    def get(self, request):
        self.RunRestAPI()
        # make consumer
        headers = {
             'Content-Type': 'application/vnd.kafka.v2+json',
        }
        data = '{"name": "'+CLIENTNAME+'", "format": "json", "auto.offset.reset": "earliest"}'
        response = requests.post(f'http://localhost:8082/consumers/{CLIENTNAME}', headers=headers, data=data)
        
        # subscribe topic
        data = '{"topics":["'+TOPICNAME+'"]}'
        response = requests.post(f'http://localhost:8082/consumers/{CLIENTNAME}/instances/{CLIENTNAME}/subscription', headers=headers, data=data)
       
        # offset rest
        data = '{ "partitions": [{"topic":"'+TOPICNAME+'","partition":0}]}'
        response = requests.post(f'http://localhost:8082/consumers/{CLIENTNAME}/instances/{CLIENTNAME}/positions/beginning', headers=headers, data=data)
        
        # get data in topic
        headers = {
             'Content-Type': 'application/vnd.kafka.json.v2+json',
             'Accept': 'application/vnd.kafka.json.v2+json'
        }
        response = requests.get(f'http://localhost:8082/consumers/{CLIENTNAME}/instances/{CLIENTNAME}/records', headers=headers)
        
        result = [d['value'] for d in response.json()]
        return Response(result, status=200)
    def post(self, request):
        self.RunRestAPI()
        requests_data = json.loads(request.body)
        headers = {
            'Content-Type': 'application/vnd.kafka.json.v2+json',
            'Accept': 'application/vnd.kafka.v2+json',
        }
        print(f"requests_data {requests_data}")
        data = {"records":[{"key":requests_data['name'],"value":str(requests_data)}]}
        response = requests.post(f'http://localhost:8082/topics/{TOPICNAME}', headers=headers, data=str(json.dumps(data)))
        return Response(response,status=200)   


# curl -X POST \
#      -H "Content-Type: application/vnd.kafka.v2+json" \
#      --data '{"name": "kafkaclient", "format": "json", "auto.offset.reset": "earliest"}' \
#      http://localhost:8082/consumers/djangokafka

# curl -X POST \
#      -H "Content-Type: application/vnd.kafka.v2+json" \
#      --data '{"topics":["djangokafka"]}' \
#      http://localhost:8082/consumers/kafkaclient/instances/kafkaclient/subscription

# curl -X GET \
#      -H "Accept: application/vnd.kafka.json.v2+json" \
#      http://localhost:8082/consumers/kafkaclient/instances/kafkaclient/records 

# curl -X POST -H "Content-Type: application/vnd.kafka.v2+json" \
# --data '{ "partitions": [{"topic":"djangokafka","partition":0}]}' http://localhost:8082/consumers/kafkaclient/instances/kafkaclient/positions/beginning