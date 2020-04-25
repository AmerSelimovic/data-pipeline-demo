# generate-helper-collections.py

Python script used to generate `categories`, `products` and `user` data and write it in MongoDB collections. It is mandatory to run this script before the `generate-orders` script as it is using these collections to create an order.

---

## Pre-requirements

- Installed `python 3` and `pip3`.
- Run `pip3 install -r requirements.txt` to install required packages.

---

## Parameters

Command line parameters required for starting the script can be seen with flag  `--help`

| Parameters | Type | Mandatory | Default | Description
| ----- | ----- | ----- | -----  | -----
| --host | string | Yes | - | Database hostname.
| --port | string | Yes | - | Database port.
| --user | string | No | - | User that will be used to authenticate to the database. Required only if authentication is enabled.
| --password | string | No | - | Password that will be used to authenticate to the database. Required only if authentication is enabled.
| --authenticationDatabase | string | No | - | MongoDB Auth DB. Required only if authentication is enabled.
| --database | string | Yes | - | Database in which the data will be written.


---

## Command Example

```
python3 generate-helper-collections.py --host localhost --port 27017 --database demoShop  --user admin --password admin -a admin

```

---

# generate-orders.py

Python script `orders` data and write it in MongoDB collections. Number of orders that will be created and the number of previous days for which the orders will be created is configurable.

---

## Pre-requirements

- Installed `python 3` and `pip3`.
- Run `pip3 install -r requirements.txt` to install required packages.

---

## Parameters

Command line parameters required for starting the script can be seen with flag  `--help`

| Parameters | Type | Mandatory | Default | Description
| ----- | ----- | ----- | -----  | -----
| --host | string | Yes | - | Database hostname.
| --port | string | Yes | - | Database port.
| --user | string | No | - | User that will be used to authenticate to the database. Required only if authentication is enabled.
| --password | string | No | - | Password that will be used to authenticate to the database. Required only if authentication is enabled.
| --authenticationDatabase | string | No | - | MongoDB Auth DB. Required only if authentication is enabled.
| --database | string | Yes | - | Database in which the data will be written.
| --number | string | Yes | - | Number of orders to create.
| --days | string | No | 7 | Number of previous days for which the orders will be created.

---

## Command Example

```
python3 generate-orders.py --host localhost --port 27017 --database demoShop  --user admin --password admin -a admin --number 100 --days 1
```
