from flask import Blueprint, request

from controllers.api_controller import home_response, process_receipt_response, get_points_for_receipt_response

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route("/")
def home():
    return home_response()


@api_blueprint.route("/receipts/process", methods=["POST"])
def process_receipt():
    """
    This endpoint stores a receipt, and returns a json with its OID.
    """
    return process_receipt_response(request.json)


@api_blueprint.route("/receipts/<uuid>/points", methods=["GET"])
def get_points_for_receipt(uuid):
    """
    This endpoint returns the points that a receipt has.
    """
    return get_points_for_receipt_response(uuid)
