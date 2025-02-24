import pika
from alert_level import get_alert_level

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

queues = ['low', 'medium', 'high']

for queue in queues:
    channel.queue_declare(queue=queue)
message=input('Enter the alert: ')
alert=get_alert_level(message)

messages = {
    alert: message
}

for queue, message in messages.items():
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message)
    print(f" [x] Sent '{message}' to {queue}")

connection.close()
