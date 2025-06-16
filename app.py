import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="input_queue")

channel.queue_declare(queue='output_queue')

channel.exchange_declare(exchange='exercise_exchange', exchange_type='direct')
channel.queue_bind(queue='input_queue', exchange='exercise_exchange', routing_key='input_queue')
channel.queue_bind(queue='output_queue', exchange='exercise_exchange', routing_key='output_queue')


class StreamAdapter:
        def __init__(self):
                self.last_added = 2
        def GetStreamChunks(self, list_of_nums):
                """
                Expands the input list of numbers up to length 12 by adding alternating 1s and 2s.
                If the last number is 1,it adds 2 to the next list.

                :param list_of_nums: (list of int) The original list of numbers.

                :return: list[list[int]] - List of 12-length number chunks
                """

                chunks = [list_of_nums[i:i + 12] for i in range(0, len(list_of_nums), 12)]

                if chunks:
                        last_chunk = chunks[-1]
                        needed = 12 - len(last_chunk)

                        if needed > 0:
                                if self.last_added == 1:
                                        last_chunk.insert(0, 2)
                                        needed -= 1
                                        self.last_added = 2

                                next_num = 1
                                for _ in range(needed):
                                        last_chunk.append(next_num)
                                        next_num = 1 if next_num == 2 else 2

                                self.last_added = 1 if next_num == 2 else 2
                                chunks[-1] = last_chunk

                return chunks


def callback(ch, method, properties, body):
        """
        the callback for the input queue's cousume
        :param ch: the chanel where the message came from
        :param method: object with information about the message and her context
        :param properties: object with extra info that the producer can add to the message like tags or id
        :param body: the content of the message
        :return: none
        """
        stream_adapter = StreamAdapter()

        message_str = body.decode()

        numbers_str = message_str.split(',')

        numbers = list(map(int, numbers_str))

        expanded_chunks = stream_adapter.GetStreamChunks(numbers)

        for chunk in expanded_chunks:
                message = ','.join(map(str, chunk))

                channel.basic_publish(
                        exchange='exercise_exchange',
                        routing_key='output_queue',
                        body=message
                )

        ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='input_queue', on_message_callback=callback)

channel.start_consuming()