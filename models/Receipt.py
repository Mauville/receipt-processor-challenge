import json
import uuid
from typing import List, Self, Optional

# We use decimal to store money, since it's the most secure way of dealing with floats and precision
from decimal import Decimal


class Item:
    def __init__(self, short_description: str, price: Decimal):
        self.shortDescription: str = short_description
        self.price: Decimal = price

    @classmethod
    def from_dict(cls, item_dict: dict) -> Self:
        return cls(
            item_dict["shortDescription"],
            Decimal(item_dict["price"]))


class Receipt:
    def __init__(self):
        self.oid: uuid.UUID
        self.retailer: str = ""
        self.items: List[Item] = []
        self.purchaseDate: str = ""
        self.purchaseTime: str = ""
        self.total: Decimal = Decimal(0.0)
        self.points: Optional[int] = None

    @classmethod
    def from_json(cls, receipt_json: json) -> Self:
        # NAMESPACE_OID is used for ObjectIDs
        cls.oid = uuid.uuid5(uuid.NAMESPACE_OID, str(receipt_json))
        cls.retailer = receipt_json["retailer"]
        cls.items = [Item.from_dict(item) for item in receipt_json["items"]]
        # In a future version, this should be refactored into a proper timestamp
        cls.purchaseDate = receipt_json["purchaseDate"]
        cls.purchaseTime = receipt_json["purchaseTime"]
        cls.total = Decimal(receipt_json["total"])
        return cls
