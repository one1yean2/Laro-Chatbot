import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

def noti_produce(user_id):
    # Send a message to the 'notification' topic
    producer.send('notification', json.dumps({'USER_ID': user_id}).encode('utf-8'))
    producer.flush()
