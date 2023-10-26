import uuid
from typing import Dict

from models.Receipt import Receipt


class ReceiptRepository:
    """
    A Singleton so that we only have one source of truth.
    Stores receipts in a dictionary, keyed by their str(UUID)
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ReceiptRepository, cls).__new__(cls)
            cls._instance.receipts = {}
        return cls._instance

    def add_receipt(self, receipt: Receipt) -> None:
        self.receipts[str(receipt.oid)] = receipt

    def get_receipt(self, receipt_uuid: str) -> Receipt:
        return self.receipts.get(receipt_uuid, None)
