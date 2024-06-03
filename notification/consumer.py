from kafka import KafkaConsumer
import time
import threading
from datetime import datetime
import requests
import json
import schedule
import time
import subprocess

LINE_ACCESS_TOKEN = "2FiR3KE3mT5uHuaSkv7GDqB+Vxgq4QEYK7vG6aLpfyY91cCwDTGiKl7vKBJMUhVvzx5QUCjP1OHV7aVQVe4rQ9jPLHNtShWyIhSqsroEVxVBqXGhdgSA6D5Or3kUwvejEQc1VqIhgxTfhWlHLKrxRQdB04t89/1O/w1cDnyilFU="
# user_id = ""

LINE_API_URL = "https://api.line.me/v2/bot/message/push"


# def send_message(user_id):
def send_message(user_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN,
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": "คุณลูกค้าหายไป 15 นาทีแล้วนะครับ"
            }
        ]
    }

    print("Sending message to user:", user_id)
    response = requests.post(LINE_API_URL, headers=headers, json=payload)
    print("Message sent. Response Status Code:", response.status_code)
    return schedule.CancelJob

def process_message(message):
    print("Received message:", message)
    message_value = message.value.decode('utf-8')

    try:
        data = json.loads(message_value)
        user_id = data['USER_ID']
        print("User ID:", user_id)
        schedule.clear(user_id)
        # Schedule message sending function to run every 15 seconds
        schedule.every(15).minutes.do(send_message, user_id).tag(user_id)

    except Exception as e:
        print(f"Error processing message: {e}")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep to avoid high CPU usage

# Initialize Kafka consumer
consumer = KafkaConsumer('notification', bootstrap_servers='localhost:9092')

# Start the scheduler in a separate thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

# Consume messages from Kafka
for message in consumer:
    # Process message in a separate function
    process_message(message)