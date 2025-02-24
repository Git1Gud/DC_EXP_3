import pika
import sys
import os

OFFICER_ALERT_MAP = {
    "Alice": "low",
    "Bob": "medium",
    "Charlie": "high"
}

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    officer_name = ""
    while officer_name == "" or officer_name not in OFFICER_ALERT_MAP:
        officer_name = input("Enter the officer name (Alice, Bob, Charlie): ")

    queue_name = OFFICER_ALERT_MAP[officer_name]
    print(f" [*] {officer_name} is assigned to '{queue_name}' queue")

    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        print(f" [x] {officer_name} received: {body.decode()}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
