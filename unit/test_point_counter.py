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
