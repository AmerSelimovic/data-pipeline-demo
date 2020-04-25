from argparse import ArgumentParser
from pymongo import MongoClient
import requests
import random
import time
import datetime

parser = ArgumentParser()
parser.add_argument(
    "-u", "--user", help="User that will be used to authenticate to the database.", dest="user")
parser.add_argument("-p", "--password",
                    help="Password that will be used to authenticate to the database.", dest="password")
parser.add_argument("-H", "--host", help="Database hostname.", dest="host")
parser.add_argument("-P", "--port", help="Database port.", dest="port")
parser.add_argument("-d", "--database",
                    help="Database in which the data will be written.", dest="database")
parser.add_argument("-a", "--authenticationDatabase",
                    help="Authentication database.", dest="authDb")
parser.add_argument(
    "-n", "--number", help="Number of orders to create.", dest="numberOfOrders")
parser.add_argument(
    "-D", "--days", help="Number of previous days for which the orders will be created.", dest="numberOfDays", default=7)
args = parser.parse_args()


def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%dT%H:%M:%S", prop)


class Product:
    def __init__(self, id, name, category, quantity, price):
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price


class User:
    def __init__(self, id, first_name, last_name, email):
        self.id = id
        self.full_name = first_name + " " + last_name
        self.email = email


class Order:
    def __init__(self, user, products_list, price, ts):
        self.user = user
        self.products_list = products_list
        self.price = price
        self.ts = ts


class MongoDBClient:
    def __init__(self):
        if args.user is not None and args.password is not None and args.authDb is not None:
            conn_url = "mongodb://" + args.user + ":" + args.password + \
                "@" + args.host + ":" + args.port + "/" + args.authDb
        else:
            conn_url = "mongodb://" + args.host + ":" + args.port
        self.client = MongoClient(conn_url)

    def createOrdersList(self):
        db = self.client[args.database]
        productsColl = db["products"]
        usersColl = db["users"]
        orders = []
        endDate = (datetime.datetime.now()).strftime("%Y-%m-%dT%H:%M:%S")
        startDate = (datetime.date.today() -
                     datetime.timedelta(days=int(args.numberOfDays))).strftime("%Y-%m-%dT%H:%M:%S")

        productsList = list(productsColl.find({}))
        usersList = list(usersColl.find({}))

        for i in range(int(args.numberOfOrders)):
            randomUser = random.choice(usersList)
            user = User(randomUser['_id'], randomUser['first_name'],
                        randomUser['last_name'], randomUser['email'])
            products = []
            randomProducts = random.sample(productsList, random.randint(1, 5))
            sumPrice = 0
            for rp in randomProducts:
                products.append(Product(
                    rp['_id'], rp['name'], rp['category'], random.randint(1, 5), rp['price']))
                sumPrice = sumPrice + rp['price']
            orderDate = datetime.datetime.strptime(random_date(
                startDate, endDate, random.random()) + '.0Z', "%Y-%m-%dT%H:%M:%S.%fZ")
            orders.append(Order(user, products, sumPrice, orderDate))
        return orders

    def writeOrdersData(self, ordersList):
        db = self.client[args.database]
        coll = db["orders"]
        for order in ordersList:
            o = {"user": {"id": order.user.id, "full_name": order.user.full_name,
                          "email": order.user.email}, "products": [],  "price": order.price, "ts": order.ts}
            for p in order.products_list:
                o['products'].append(
                    {"id": p.id, "name": p.name, "category": p.category, "quantity": p.quantity, "price": p.price})
            coll.insert_one(o)
            print("Inserted order " + str(o['_id']))
            time.sleep(0.2)
        print("-----------------------------------------------")
        print("Inserted " + str(len(ordersList)) + " order/s")


mongoClient = MongoDBClient()
ordersList = mongoClient.createOrdersList()
mongoClient.writeOrdersData(ordersList)
