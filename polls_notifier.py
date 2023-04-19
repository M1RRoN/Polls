from django.core.management.base import BaseCommand
import pika
from django.conf import settings
import json


class Command(BaseCommand):
    help = 'Starts the poll notifier'

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST,
                                                                       port=settings.RABBITMQ_PORT,
                                                                       credentials=pika.PlainCredentials(
                                                                           username=settings.RABBITMQ_USERNAME,
                                                                           password=settings.RABBITMQ_PASSWORD)))
        channel = connection.channel()
        channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME)

        def callback(ch, method, properties, body):
            poll_id = int(body.decode('utf-8'))
            print(f'Poll {poll_id} has been updated')

        channel.basic_consume(queue=settings.RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=True)

        print('Poll notifier has started')
        channel.start_consuming()
