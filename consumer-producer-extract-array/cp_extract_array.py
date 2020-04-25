from argparse import ArgumentParser
from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
import os
import requests
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer, CachedSchemaRegistryClient
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer as AvroSerde

import logging
logging.basicConfig(level=logging.INFO)


BOOTSTRAP_SERVERS = ""
INPUT_TOPIC_NAME = ""
OUTPUT_TOPIC_NAME = ""
SCHEMA_REGISTRY_URL = ""
AUTO_OFFSET_RESET = ""
GROUP_ID = ""
ARRAY_NAME = ""
DOCUMENT_FIELD_PREFIX = ""
CONSUMER_BATCH_SIZE = ""


def checkEnvVariables():
    if "BOOTSTRAP_SERVERS" in os.environ:
        global BOOTSTRAP_SERVERS
        BOOTSTRAP_SERVERS = os.environ['BOOTSTRAP_SERVERS']
    else:
        raise Exception("Invalid env variable: BOOTSTRAP_SERVERS")
    if "INPUT_TOPIC_NAME" in os.environ:
        global INPUT_TOPIC_NAME
        INPUT_TOPIC_NAME = os.environ['INPUT_TOPIC_NAME']
    else:
        raise Exception("Invalid env variable: INPUT_TOPIC_NAME")
    if "OUTPUT_TOPIC_NAME" in os.environ:
        global OUTPUT_TOPIC_NAME
        OUTPUT_TOPIC_NAME = os.environ['OUTPUT_TOPIC_NAME']
    else:
        raise Exception("Invalid env variable: OUTPUT_TOPIC_NAME")
    if "SCHEMA_REGISTRY_URL" in os.environ:
        global SCHEMA_REGISTRY_URL
        SCHEMA_REGISTRY_URL = os.environ['SCHEMA_REGISTRY_URL']
    else:
        raise Exception("Invalid env variable: SCHEMA_REGISTRY_URL")
    if "GROUP_ID" in os.environ:
        global GROUP_ID
        GROUP_ID = os.environ['GROUP_ID']
    else:
        raise Exception("Invalid env variable: GROUP_ID")
    if "AUTO_OFFSET_RESET" in os.environ:
        global AUTO_OFFSET_RESET
        AUTO_OFFSET_RESET = os.environ['AUTO_OFFSET_RESET']
    else:
        AUTO_OFFSET_RESET = 'latest'
    if "ARRAY_NAME" in os.environ:
        global ARRAY_NAME
        ARRAY_NAME = os.environ['ARRAY_NAME']
    else:
        raise Exception("Invalid env variable: ARRAY_NAME")
    if "DOCUMENT_FIELD_PREFIX" in os.environ:
        global DOCUMENT_FIELD_PREFIX
        DOCUMENT_FIELD_PREFIX = os.environ['DOCUMENT_FIELD_PREFIX']
    else:
        raise Exception("Invalid env variable: DOCUMENT_FIELD_PREFIX")
    if "CONSUMER_BATCH_SIZE" in os.environ:
        global CONSUMER_BATCH_SIZE
        CONSUMER_BATCH_SIZE = int(os.environ['CONSUMER_BATCH_SIZE'])
    else:
        CONSUMER_BATCH_SIZE = 100


class ConsumerProducer():
    def __init__(self):
        try:
            self.outputKeySchema = avro.loads(
                self.fetchSchema(OUTPUT_TOPIC_NAME, True)['schema'])
            self.outputValueSchema = avro.loads(
                self.fetchSchema(OUTPUT_TOPIC_NAME, False)['schema'])
        except Exception as e:
            logging.error(
                "Connection error: {}. Application will exit.".format(e))
            exit()

    def fetchSchema(self, topic_name, isKey):
        if isKey:
            type = 'key'
        else:
            type = 'value'
        schema = requests.get(
            SCHEMA_REGISTRY_URL + "/subjects/" + topic_name + "-" + type + "/versions/latest").json()
        return schema

    def printAndProduceMessages(self):
        consumer = AvroConsumer({
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'group.id': GROUP_ID,
            'auto.offset.reset': AUTO_OFFSET_RESET,
            'enable.auto.commit': False,
            'schema.registry.url': SCHEMA_REGISTRY_URL})
        schema_registry = CachedSchemaRegistryClient(
            os.environ.get('SCHEMA_REGISTRY', SCHEMA_REGISTRY_URL))
        avro_serde = AvroSerde(schema_registry)

        consumer.subscribe([INPUT_TOPIC_NAME])

        while True:
            try:
                consumedMessages = consumer.consume(
                    num_messages=CONSUMER_BATCH_SIZE, timeout = 1)
            except Exception as e:
                logging.error(
                    "Message pool failed: {}".format(e))
                break

            messages = []
            for consumedMessage in consumedMessages:
                consumedMessageValue = avro_serde.decode_message(
                    consumedMessage.value())
                message = {}
                message["key"] = {}
                message["value"] = {}

                for attr, value in consumedMessageValue.items():
                    if attr != ARRAY_NAME:
                        message["value"][DOCUMENT_FIELD_PREFIX + attr] = value

                for arrayItem in consumedMessageValue[ARRAY_NAME]:
                    message["key"]["id"] = consumedMessageValue["id"] + \
                        "-" + arrayItem["id"]
                    for attr, value in arrayItem.items():
                        message["value"][attr] = value
                    messages.append(message)

            self.produceMessages(messages)
            consumer.commit()
        consumer.close()

    def produceMessages(self, messages):
        avroProducer = AvroProducer({
            'bootstrap.servers': BOOTSTRAP_SERVERS,
            'schema.registry.url': SCHEMA_REGISTRY_URL
        }, default_key_schema=self.outputKeySchema, default_value_schema=self.outputValueSchema)

        for message in messages:
            avroProducer.produce(
                topic=OUTPUT_TOPIC_NAME, key=message["key"], value=message["value"])

        avroProducer.flush()
        logging.info("Produced " + str(len(messages)) +
                     " message/s to topic " + OUTPUT_TOPIC_NAME)


checkEnvVariables()

consumerProducer = ConsumerProducer()
consumerProducer.printAndProduceMessages()
