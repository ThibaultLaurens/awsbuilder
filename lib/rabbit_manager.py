import logging
import pika
import json

#todo connection.on 'ready', 'error', 'close'

class Rabbit(object):

    def __init__(self, url, exchange):
        self._exchange = exchange
        self._channel = self.__connect(url)
        self._channel.exchange_declare(exchange=exchange, type='topic', durable=True)
        logging.info("rabbit exchange %s open" % exchange)

    def add_topics(self, queue, topics):
        queue = self._channel.queue_declare(queue=queue, durable=True)
        self._queue = queue.method.queue
        for topic in topics:
            self._channel.queue_bind(queue=self._queue, exchange=self._exchange, routing_key=topic)
        logging.info("rabbit %s queue binded to %s exchange", self._queue, self._exchange)

    def publish(self, topic, message):
        self._channel.basic_publish(exchange=self._exchange, routing_key=topic, body=json.dumps(message),
                                    properties=pika.BasicProperties(content_type='application/json', delivery_mode=2))

    def receive(self, callback):
        self._channel.basic_consume(callback, queue=self._queue, no_ack=True)
        self._channel.start_consuming()


    def __connect(self, url):
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        logging.info("rabbit connected to %s" % url)
        return channel








