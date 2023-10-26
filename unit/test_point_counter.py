import json
from unittest import TestCase

from models.Receipt import Receipt
from services.point_counter import count_points


class TestPointCounter(TestCase):
    def test_simple_count_points(self):
        test_json: json = json.loads(""" {
          "retailer": "Target",
          "purchaseDate": "2022-01-01",
          "purchaseTime": "13:01",
          "items": [
            {
              "shortDescription": "Mountain Dew 12PK",
              "price": "6.49"
            },{
              "shortDescription": "Emils Cheese Pizza",
              "price": "12.25"
            },{
              "shortDescription": "Knorr Creamy Chicken",
              "price": "1.26"
            },{
              "shortDescription": "Doritos Nacho Cheese",
              "price": "3.35"
            },{
              "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
              "price": "12.00"
            }
          ],
          "total": "35.35"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 28)

    def test_complex_count_points(self):
        test_json: json = json.loads(""" {
          "retailer": "M&M Corner Market",
          "purchaseDate": "2022-03-20",
          "purchaseTime": "14:33",
          "items": [
            {
              "shortDescription": "Gatorade",
              "price": "2.25"
            },{
              "shortDescription": "Gatorade",
              "price": "2.25"
            },{
              "shortDescription": "Gatorade",
              "price": "2.25"
            },{
              "shortDescription": "Gatorade",
              "price": "2.25"
            }
          ],
          "total": "9.00"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 109)

    def test_empty_json(self):
        test_json: json = json.loads(""" {
          "retailer": "#&",
          "purchaseDate": "2022-03-20",
          "purchaseTime": "13:33",
          "items": [
            {
              "shortDescription": "Less",
              "price": "2.25"
            }
          ],
          "total": "9.99"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 0)

    def test_count_alphanumeric(self):
        test_json: json = json.loads(""" {
          "retailer": "ABC123&^%$",
          "purchaseDate": "2022-01-02",
          "purchaseTime": "12:00",
          "items": [],
          "total": "1.82"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 6)

    def test_count_is_round_amount(self):
        test_json: json = json.loads(""" {
          "retailer": "#&",
          "purchaseDate": "2022-01-02",
          "purchaseTime": "12:00",
          "items": [],
          "total": "5.00"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 75)

    def test_count_is_quartile(self):
        test_json: json = json.loads(""" {
          "retailer": "%^&",
          "purchaseDate": "2022-01-02",
          "purchaseTime": "12:00",
          "items": [],
          "total": "2.75"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 25)

    def test_count_even_items(self):
        test_json: json = json.loads(""" {
          "retailer": "%^&*",
          "purchaseDate": "2022-01-02",
          "purchaseTime": "12:00",
          "items": [{"shortDescription": "Item1", "price": "1.00"},
                    {"shortDescription": "Item2", "price": "1.00"}],
          "total": "2.01"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 5)

    def test_count_odd_day(self):
        test_json: json = json.loads(""" {
          "retailer": "^&*(",
          "purchaseDate": "2022-01-03",
          "purchaseTime": "12:00",
          "items": [],
          "total": "1.01"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 6)

    def test_count_even_day(self):
        test_json: json = json.loads(""" {
          "retailer": "^&*(",
          "purchaseDate": "2022-01-02",
          "purchaseTime": "12:00",
          "items": [],
          "total": "1.01"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 0)

    def test_count_afternoon_purchase(self):
        test_json: json = json.loads(""" {
          "retailer": "%^&*(",
          "purchaseDate": "2022-01-02",
          "purchaseTime": "15:59",
          "items": [],
          "total": "1.23"
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(count_points(receipt), 10)

