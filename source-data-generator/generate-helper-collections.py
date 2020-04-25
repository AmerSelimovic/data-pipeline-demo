from argparse import ArgumentParser
from pymongo import MongoClient
import requests
import datetime
import json
from random_words import RandomWords
import random

parser = ArgumentParser()
parser.add_argument("-u", "--user", help="User that will be used to authenticate to the database.", dest="user")
parser.add_argument("-p", "--password", help="Password that will be used to authenticate to the database.", dest="password")
parser.add_argument("-H", "--host", help="Database hostname.", dest="host")
parser.add_argument("-P", "--port", help="Database port.", dest="port")
parser.add_argument("-d", "--database", help="Database in which the data will be written.", dest="database")
parser.add_argument("-a", "--authenticationDatabase", help="Authentication database.", dest="authDb")
args = parser.parse_args()


class User:
    def __init__(self, first_name, last_name, email, gender, birth_date, country_code):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = first_name + " " + last_name
        self.email = email
        self.gender = gender
        self.birth_date = birth_date
        self.country_code = country_code

class ApiClient:
    def __init__(self):
        self.url = "https://randomuser.me/api/?results=1000&inc=gender,name,email,dob,nat"
    def getUsersList(self):
        response = requests.get(self.url)
        People = []
        for responseItem in response.json()["results"]:
            parsed = User(
                responseItem["name"]["first"], responseItem["name"]["last"], responseItem["email"], responseItem["gender"], responseItem["dob"]["date"], responseItem["nat"])
            People.append(parsed)
        return People

def getRandomPrice():
    greaterThan = float(1)
    lessThan = float(50)
    digits = int(2)
    rounded_number = round(random.uniform(greaterThan, lessThan), digits)
    return rounded_number

class MongoDBClient:
    def __init__(self):
        if args.user is not None and args.password is not None and args.authDb is not None:
            conn_url = "mongodb://" + args.user + ":" + args.password + "@" + args.host + ":" + args.port  + "/" + args.authDb
        else:
            conn_url = "mongodb://" + args.host  + ":" + args.port
        self.client = MongoClient(conn_url)
    def writeUsersData(self, usersList):
        db = self.client[args.database]
        coll = db["users"]
        for user in usersList:
            u = { "first_name": user.first_name, "last_name": user.last_name, "full_name": user.full_name, "email": user.email, "gender": user.gender, "birth_date": datetime.datetime.strptime(user.birth_date, "%Y-%m-%dT%H:%M:%S.%fZ"), "country_code": user.country_code }
            coll.insert_one(u)
    def writeCategoriesData(self, categoriesList):
        db = self.client[args.database]
        coll = db["categories"]
        for c in categoriesList:
            coll.insert_one(c)
    def writeProductsData(self, categoriesList):
        rw = RandomWords()
        productsList = []
        for i in range(500):
            product_name = rw.random_word()
            if(product_name not in productsList):
                category = random.choice(categoriesList)
                product = { "name": product_name, "price": getRandomPrice(), "category": category["name"], "category_id": category["_id"] }
                productsList.append(product)
        db = self.client[args.database]
        coll = db["products"]
        for p in productsList:
            coll.insert_one(p)

apiClient = ApiClient()
usersList = apiClient.getUsersList()
mongoClient = MongoDBClient()
mongoClient.writeUsersData(usersList)
with open("categories.json") as categories_json:
    categoriesList = json.load(categories_json)
mongoClient.writeCategoriesData(categoriesList)
mongoClient.writeProductsData(categoriesList)
print("Data generated.")
