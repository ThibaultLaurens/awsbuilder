from rabbit_manager import Rabbit
from ec2_builder import EC2_Builder
from job_manager import Job_Manager


class Build_Router(object):

    def __init__(self, config):
        self._config = config
        self._queues = config["RABBIT_QUEUES"]
        self._job_manager = Job_Manager(self._config)

    def __on_message(self, channel, basic_deliver, properties, body):
        if basic_deliver.routing_key == "node.build":
            self._ec2.create_instance(body)

    def build(self):

        publisher = Rabbit(self._config["RABBIT_TX_URL"], "worker.publisher")
        publisher.add_topics(self._queues["PUBLISH"], ["node.info"])

        self._ec2 = EC2_Builder(self._config, publisher, self._job_manager)

        consumer = Rabbit(self._config["RABBIT_RX_URL"], "worker.consumer")
        consumer.add_topics(self._queues["CONSUME"], ["node.build"])
        consumer.receive(self.__on_message)
