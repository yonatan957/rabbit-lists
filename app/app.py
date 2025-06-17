import pika
import os
from app.stream_adapter import StreamAdapter
from typing import List

INPUT_QUEUE_NAME = os.getenv("INPUT_QUEUE_NAME", "input_queue")
OUTPUT_QUEUE_NAME = os.getenv("OUTPUT_QUEUE_NAME", "output_queue")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "exercise_exchange")
PIKA_HOST = os.getenv("PIKA_HOST", 'localhost')
CHUNK_SIZE = os.getenv("CHUNK_SIZE", 12)

def make_call_back(channel_to_rabbit):
        def handle_messages(
                ch: pika.channel.Channel,
                method: pika.spec.Basic.Deliver,
                properties: pika.spec.BasicProperties,
                body: bytes) ->  None:
                """
                the handle_messages for the input queue's cousume
                :param ch: the chanel where the message came from
                :param method: object with information about the message and her context
                :param properties: object with extra info that the producer can add to the message like tags or id
                :param body: the content of the message
                :return: none
                """
                stream_adapter = StreamAdapter(CHUNK_SIZE)

                message_str = body.decode()

                numbers_str = message_str.split(',')

                numbers = list(map(int, numbers_str))

                expanded_chunks = stream_adapter.GetStreamChunks(numbers)

                for chunk in expanded_chunks:
                        message = ','.join(map(str, chunk))

                        channel_to_rabbit.basic_publish(
                                exchange=EXCHANGE_NAME,
                                routing_key=OUTPUT_QUEUE_NAME,
                                body=message
                        )

                ch.basic_ack(delivery_tag=method.delivery_tag)
        return handle_messages

if __name__ == '__main__':
        connection = pika.BlockingConnection(pika.ConnectionParameters(PIKA_HOST))
        channel = connection.channel()

        channel.queue_declare(queue=INPUT_QUEUE_NAME)
        channel.queue_declare(queue=OUTPUT_QUEUE_NAME)
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')

        channel.queue_bind(queue=INPUT_QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key=INPUT_QUEUE_NAME)
        channel.queue_bind(queue=OUTPUT_QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key=OUTPUT_QUEUE_NAME)

        handle_messages_fn = make_call_back(channel)
        channel.basic_consume(queue=INPUT_QUEUE_NAME, on_message_callback=handle_messages_fn)
        channel.start_consuming()