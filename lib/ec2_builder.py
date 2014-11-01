import logging
import json
from boto.ec2.connection import EC2Connection
from boto.exception import EC2ResponseError


class EC2_Builder(object):

    def __init__(self, config, publisher, job_manager):
        self._publisher = publisher
        self._job_manager = job_manager
        # default connect to us-east-1 region
        self._ec2 = EC2Connection(config["AWS_accessKeyId"], config["AWS_secretAccessKey"])
        logging.info("AWS connected with %s", self._ec2)

    def create_instance(self, node_info):
        node_info = json.loads(node_info)
        if (node_info["name"] and node_info["key_name"] and node_info["security_groups"] and
                node_info["instance_type"] and node_info["image_id"] and node_info["id"]):
            try:
                reservation = self._ec2.run_instances(image_id=node_info["image_id"],
                                                      key_name=node_info["key_name"],
                                                      security_groups=node_info["security_groups"],
                                                      instance_type=node_info["instance_type"])
                instance = reservation.instances[0]

                message = {'id': node_info['id'], 'instance_id': instance.id, 'state': instance.state}
                self.__publish("node.info", message)
                logging.info("instance %s created" % instance.id)

                self.__tag(instance.id, {"Name": node_info["name"]})
                self._job_manager.add_job(self.__pull_state, 5, "state-" + instance.id, instance, node_info['id'])
                self._job_manager.add_job(self.__pull_info, 5, "info-" + instance.id, instance, node_info['id'])

            except EC2ResponseError as e:
                message = {'error': e.reason, 'message': e.message}
                logging.error(message)
                #todo add an "error topic to build_cb Q, and send the error message

    def __publish(self, topic, message):
        self._publisher.publish(topic,  message)

    def __tag(self, inst_id, tags):
            print "setting tags %s" % tags
            self._ec2.create_tags(inst_id, tags)

    def __pull_state(self, instance, id):
        instance.update()
        if instance.state == 'running':
            message = {'id': id, 'state': instance.state}
            self.__publish("node.info", message)
            self._job_manager.remove_job("state-" + instance.id)

    def __pull_info(self, instance, id):
        instance.update()
        if instance.ip_address and instance.private_ip_address and instance.private_dns_name:
            message = {'id': id, 'ip_address': instance.ip_address, 'private_ip_address': instance.private_ip_address,
                       'public_dns_name': instance.public_dns_name}
            self.__publish("node.info", message)
            self._job_manager.remove_job("info-" + instance.id)






