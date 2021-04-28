#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import math
from locust import HttpUser, TaskSet, between, stats, task
from locust import LoadTestShape
from locust.contrib.fasthttp import FastHttpUser


stats.CSV_STATS_INTERVAL_SEC = 5 # default is 1 second

class UserBehavior(TaskSet):

    #def on_start(self):
    #    index(self)

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def setCurrency(self):
        currencies = ['EUR', 'USD', 'JPY', 'CAD']
        self.client.post("/setCurrency",
            {'currency_code': random.choice(currencies)})

    @task(10)
    def browseProduct(self):
        products = [
            '0PUK6V6EV0',
            '1YMWWN1N4O',
            '2ZYFJ3GM2N',
            '66VCHSJNUP',
            '6E92ZMYYFZ',
            '9SIQT8TOJO',
            'L9ECAV7KIM',
            'LS4PSXUNUM',
            'OLJCESPC7Z']

        self.client.get("/product/" + random.choice(products))


    @task(3)
    def viewCart(self):
        self.client.get("/cart")

    @task(2)
    def addToCart(self):
        products = [
            '0PUK6V6EV0',
            '1YMWWN1N4O',
            '2ZYFJ3GM2N',
            '66VCHSJNUP',
            '6E92ZMYYFZ',
            '9SIQT8TOJO',
            'L9ECAV7KIM',
            'LS4PSXUNUM',
            'OLJCESPC7Z']

        product = random.choice(products)
        self.client.get("/product/" + product)

        self.client.post("/cart", {
            'product_id': product,
            'quantity': random.choice([1,2,3,4,5,10])})


    @task(1)
    def checkout(self):
        products = [
            '0PUK6V6EV0',
            '1YMWWN1N4O',
            '2ZYFJ3GM2N',
            '66VCHSJNUP',
            '6E92ZMYYFZ',
            '9SIQT8TOJO',
            'L9ECAV7KIM',
            'LS4PSXUNUM',
            'OLJCESPC7Z']

        product = random.choice(products)
        self.client.get("/product/" + product)

        
        self.client.post("/cart", {
            'product_id': product,
            'quantity': random.choice([1,2,3,4,5,10])})

        self.client.post("/cart/checkout", {
            'email': 'someone@example.com',
            'street_address': '1600 Amphitheatre Parkway',
            'zip_code': '94043',
            'city': 'Mountain View',
            'state': 'CA',
            'country': 'United States',
            'credit_card_number': '4432-8015-6152-0454',
            'credit_card_expiration_month': '1',
            'credit_card_expiration_year': '2039',
            'credit_card_cvv': '672',
        })
            


class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 10)

    connection_timeout = 5.0
    network_timeout = 5.0

class CustomLoadShape(LoadTestShape):

    time_increase = 1000
    time_constant = 1600
    time_second_increase = 2600
    time_second_constant = 3200
    time_decrease = 4200
    time_limit = 4800

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.time_increase:
            return (math.floor(run_time), 1)

        if run_time < self.time_constant:
            return (1000, 1)

        if run_time < self.time_second_increase:
            return (1000 + math.floor(run_time - self.time_constant), 1)

        if run_time < self.time_second_constant:
            return (2000, 1)

        if run_time < self.time_decrease:
            return (2000 - math.floor(run_time - self.time_second_constant), 1)
        
        if run_time < self.time_limit:
            return (1000, 1)

        return None