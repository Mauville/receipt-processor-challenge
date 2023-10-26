import json

from flask import jsonify, Response, abort

from models.Receipt import Receipt
from repositories.ReceiptRepository import ReceiptRepository
from services.point_counter import count_points


def home_response() -> str:
    return ("<h1>Hi there. My name's Oscar.</h1>"
            "<p>Regardless of the assignment, I'd love to hear what you think about this app!</p> "
            "How can I improve for next time? Send feedback <a href='https://linkedin.com/in/osvap' "
            "target='blank'>here.</a>"
            )


def process_receipt_response(request_json: json) -> Response:
    """
    Stores a receipt, and returns a JSON with its OID.
    """
    repository = ReceiptRepository()
    receipt = Receipt.from_json(request_json)
    repository.add_receipt(receipt)
    return jsonify({"id": receipt.oid})


def get_points_for_receipt_response(uuid_str: str) -> Response:
    """
    Returns the points that a receipt has.
    """
    repository = ReceiptRepository()
    receipt = repository.get_receipt(uuid_str)
    if not receipt:
        abort(404)
    # (Lazily) Memoize points for next time this is used.
    if not receipt.points:
        receipt.points = count_points(receipt)
    return jsonify({"points": receipt.points})
