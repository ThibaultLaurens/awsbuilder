awsbuilder
==========

build aws components on demand - talk with me through the amqp protocol



### Start the worker

- install python, pip & rabbitmq
- pip install -r requirements.txt
- run rabbitmq-server


### Push to heroku

- update config.ex.yaml -> config.yaml
- add a Procfile
- heroku config:set PY_ENV=production
- git add .
- git commit -m "commit-message"
- git push heroku master


### Requirements

- boto -> talk to aws
- pika -> talk to rabbit
- APScheduler -> task scheduler


### Concepts

- worker.py:
    - load the configuration file
    - setup the logger
    - create the build_router

- lib/build_router.py:
    - create a publisher exchange and bind queues and topics
    - create a job manager
    - create builders and give them the publisher exchange and the job manager
    - create a consumer exchange, listen for messages and call builders "create" methods depending on topics received

- lib/*_builder.py:
    - build what they have to build
    - pull aws for info with the job manager
    - send info to rabbit with the publisher exchange
