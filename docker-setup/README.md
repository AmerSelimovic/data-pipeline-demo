# Docker setup
Docker compose setup that will deploy all the components needed for this demo.

- Kafka:

  Kafka is a highly scalable and configurable streaming platform. In our case it is used as a temporary data storage between the data source and the data sink. The data will be written in it from MongoDB, transformed and then written to Elasticsearch. We are running single instance of Kafka broker with a minimum configuration. -

  Recommended to read: [Kafka as a Messaging System](https://kafka.apache.org/documentation/#kafka_mq)

- Zookeeper:

  Single instance of Zookeeper who is responsible to orchestrate the Kafka cluster.

  Recommended to read: [ CloudKarafka - What is Zookeeper and why is it needed for Apache Kafka?](https://www.cloudkarafka.com/blog/2018-07-04-cloudkarafka_what_is_zookeeper.html)
- Schema registry:

  Kafka doesn't care about the message structure as it stores them just as array of bytes. To ensure that the data in our topics is consistent we are using Avro schemas, the Schema registry is added as a central place for them.

  Recommended to read: [Confluent - Why Avro for Kafka Data?](https://www.confluent.io/blog/avro-kafka-data/)
- Kafka Connect:

  Kafka Connect is a framework for connecting Kafka with external systems such as databases, key-value stores, search indexes, and file systems. Using it you can write so called `connectors` which make it easy to integrate data sources and data sinks. A lot of already created connectors can be found on the [Confluent Hub](https://www.confluent.io/hub/).

  Recommended to read: [Confluent - Kafka Connect](https://docs.confluent.io/current/connect/index.html)
- MongoDB:

  MongoDB is a document database designed for ease of development and scaling. We will use it as a data source in this demo.

  Recommended to read: [Introduction to MongoDB](https://docs.mongodb.com/manual/introduction/)
- Elasticsearch

  Elasticsearch is a distributed, open source search and analytics engine for all types of data, including textual, numerical, geospatial, structured, and unstructured. We will use it as a data sink in this demo.

  Recommended to read: [What is Elasticsearch](https://www.elastic.co/what-is/elasticsearch)
- Kibana:

  Kibana is a data search and visualization tool for data that is stored in Elasticsearch. We will use it for near real time dashboards.

  Recommended to read: [What is Kibana?](https://www.elastic.co/what-is/kibana)
- Lenses Schema registry UI:

  Used for an easier overview and management of Avro schemas.

  Repo: [lensesio/schema-registry-ui](https://github.com/lensesio/schema-registry-ui)
- Yahoo Kafka Manager:

  Used for an easier overview and management of Kafka clusters and topics. It is now known under name `CMAK`.

  Repo: [yahoo/CMAK](https://github.com/yahoo/CMAK)
- Lenses Kafka Connect UI:

  Used for an easier overview and management of Kafka connectors.

  Repo: [lensesio/schema-registry-ui](https://github.com/lensesio/kafka-connect-ui)

## Usage:

Start the provided docker-compose.yaml file. All used images are public and pulled from the Docker Hub.

Note: Network demo_network needs to be created before as it is being used in all docker-compose files in the demo.

`docker network create demo_network`

  The applications are exposed on following ports:
  - MongoDB: localhost:27017
  - Kafka Broker: localhost:9092
  - Zookeeper: localhost:2181
  - Schema Registry: localhost:8081
  - Kafka Connect: localhost:8083
  - Schema Registry UI : localhost:8001
  - Kafka Connect UI: localhost:8082
  - Kafka Manager: localhost:8003
  - Kibana: localhost:5601
  - Elasticsearch: localhost:9200 and localhost:9300
