# consumer-producer-extract-array
Configurable application used to extract array items to a new message each, while keeping the other fields and adding a prefix to them. For example, as in this demo, if we want to extract products from an order so that the info about every product is a new message.

## Configuration:

Application is configured using environment variables.

| Parameter | Description | Example | Default |
| -----  | ----- | ----- | ----- |
| BOOTSTRAP_SERVERS | List of Kafka brokers we are connecting to | broker:9092 | |
| SCHEMA_REGISTRY_URL | Url of the Schema registry from which the avro schemas will be fetched | http://schema_registry:8081 | |
| INPUT_TOPIC_NAME | Name of the topic we are reading from | demoShop.demoShop.orders | |
| OUTPUT_TOPIC_NAME | Name of the topic we are writing to | demoShop.demoShop.orderProducts | |
| GROUP_ID | ID of the consumer group | cpe_consumer_1 | |
| AUTO_OFFSET_RESET | | earliest | latest |
| ARRAY_NAME | Name of the array we are extracting new messages from | products | |
| DOCUMENT_FIELD_PREFIX | Prefix that will be added to the names of the fields in the root document | orders_ |  |
| CONSUMER_BATCH_SIZE | Max batch size of our consumer | 100 | 100 |


## Build:

Provided Dockerfile file can be used to build a Docker image.
"docker build -t demo/cp_extract_array:0.0.1 ."

## Usage:

Provided docker-compose.yaml file can be used to configure and deploy the application.


## Example:

This is an example of the input and output message in this demo.

Input message:
```json
{
    "user": {
        "id": "5ea42c302eabe5323464ce09",
        "full_name": "Hailey Anderson",
        "email": "hailey.anderson@example.com"
    },
    "products": [
        {
            "id": "5ea42c322eabe5323464d364",
            "name": "rebounds",
            "category": "Accessories",
            "quantity": 3,
            "price": 33.95
        },
        {
            "id": "5ea42c322eabe5323464d284",
            "name": "hook",
            "category": "Household",
            "quantity": 1,
            "price": 28.65
        },
        {
            "id": "5ea42c322eabe5323464d208",
            "name": "manner",
            "category": "Household",
            "quantity": 3,
            "price": 5.55
        }
    ],
    "price": 68.15,
    "ts": 1587798644000,
    "id": "5ea4357d42c9dad9572f682c"
}
```

Output message:
```json
{
    "key": {
        "id": "5ea4357d42c9dad9572f682c-5ea42c322eabe5323464d364"
    },
    "value": {
        "order_user": {
            "id": "5ea42c302eabe5323464ce09",
            "full_name": "Hailey Anderson",
            "email": "hailey.anderson@example.com"
        },
        "order_price": 68.15,
        "order_ts": 1587798644000,
        "order_id": "5ea4357d42c9dad9572f682c",
        "id": "5ea42c322eabe5323464d364",
        "name": "rebounds",
        "category": "Accessories",
        "quantity": 3,
        "price": 33.95
    }
}
```
