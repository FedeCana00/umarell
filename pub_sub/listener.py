# Pub/Sub libraries
import os
import json
from google.cloud import pubsub_v1
import sys

caps = []

def callback(message):
    print(f"[INFO] Received {message}")
    message.ack()

    try:
        data = json.loads(message.data.decode('utf-8'))
    except Exception as e:
        print(e)
        return None
    
    if data['cap'] in caps:
        print(f'Nuovo cantiere inserito --> {data}')
    

subscription_name = os.environ['SUBSCRIPTION_NAME'] if os.environ['SUBSCRIPTION_NAME'] else 'cantiere_sub'
project_id=os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'generalsac'

# read caps for command line
for arg in sys.argv:
    try:
        caps.append(int(arg))
    except:
        pass

print(f"Listening on sub_name={subscription_name}, project_id={project_id}, caps={caps}")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

pull = subscriber.subscribe(subscription_path, callback=callback)
try:
    pull.result()
except KeyboardInterrupt:
    pull.cancel()