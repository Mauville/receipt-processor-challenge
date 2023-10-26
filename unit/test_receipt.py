import json
from unittest import TestCase

from decimal import Decimal

from models.Receipt import Receipt, Item


class TestItem(TestCase):
    def test_from_dict(self):
        test_dict: dict = {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
        item = Item.from_dict(test_dict)
        self.assertEqual(item.shortDescription, "Pepsi - 12-oz")
        self.assertEqual(item.price, Decimal(1.25))


class TestReceipt(TestCase):
    def test_from_json(self):
        test_json: json = json.loads("""
        {
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        }""")
        receipt = Receipt.from_json(test_json)
        self.assertEqual(receipt.retailer, "Target")
        self.assertEqual(receipt.purchaseDate, "2022-01-02")
        self.assertEqual(receipt.purchaseTime, "13:13")
        self.assertEqual(receipt.total, Decimal(1.25))
        self.assertEqual(len(receipt.items), 1)
