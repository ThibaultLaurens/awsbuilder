import pika
import yaml


if __name__ == '__main__':

    config = yaml.load(open('../config.yaml').read())
    config = config["development"]
    queue = config["RABBIT_QUEUES"]["CONSUME"]
    url = config["RABBIT_RX_URL"]

    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)

    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)
    message = '{ "security_groups": ["sparta"], "instance_type": "m1.xlarge", ' \
              '"key_name": "ops_tom", "image_id": "ami-56009e3f", "name": "spartadp-test" }'
    channel.basic_publish(exchange='', routing_key=queue, body=message)

    print "message published to %s queue" % queue