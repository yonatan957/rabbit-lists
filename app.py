import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="input_queue")

channel.queue_declare(queue='output_queue')

def expand_list(list_of_nums):
        """
        Expands the input list of numbers up to length 12 by adding alternating 1s and 2s.
        If the last number is 1,it adds 2 to the next list.

        :param list_of_nums: (list of int) The original list of numbers.

        :returns: list of int: The extended list with length 12.
        """
        return list_of_nums

def callback(ch, method, properties, body):
        """
        the callback for the input queue's cousume
        :param ch: the chanel where the message came from
        :param method: object with information about the message and her context
        :param properties: object with extra info that the producer can add to the message like tags or id
        :param body: the content of the message
        :return: none
        """
        message_str = body.decode()

        numbers_str = message_str.split(',')

        numbers = list(map(int, numbers_str))

        # I will implement this function soon, Ben.
        expanded_list = expand_list(numbers)

        new_message = ','.join(map(str, expanded_list))

        channel.basic_publish(exchange='',
                              routing_key='output_queue',
                              body=new_message)

        ch.basic_ack(delivery_tag=method.delivry_tag)

channel.basic_consume(queue='input_queue', on_message_callback=callback)

channel.start_consuming()