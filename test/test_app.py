from unittest import TestCase

from main import app
from repositories.ReceiptRepository import ReceiptRepository


class TestApp(TestCase):
    """
    Simple integration testing cases.
    We're going to be borrowing the Flask app from our main code, and calling the in-built methods.
    This will make our code have fewer dependencies and will serve as enough validation for this exercise.
    This class ideally would set up a mock server and query that directly.
    """

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self) -> None:
        # Flush repository, just in case, to avoid test pollution.
        repo = ReceiptRepository()
        repo.receipts = {}

    def test_home_route(self):
        # Basic route sanity check
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_process_receipt(self):
        receipt_json = """
            {
                "retailer": "Walgreens",
                "purchaseDate": "2022-01-02",
                "purchaseTime": "08:13",
                "total": "2.65",
                "items": [
                    {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                    {"shortDescription": "Dasani", "price": "1.40"}
                ]
            }"""
        response = self.client.post("/receipts/process",
                                    data=receipt_json,
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 200)
        received_data = response.get_json()
        self.assertIn("id", received_data.keys())

    def test_get_points(self):
        receipt_json = """ {
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
        }"""
        # Upload
        response = self.client.post("/receipts/process",
                                    data=receipt_json,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        receipt_uuid = response.get_json()["id"]
        # Check the points
        final_response = self.client.get(
            f"/receipts/{receipt_uuid}/points",
        )
        self.assertEqual(final_response.status_code, 200)
        self.assertEqual(final_response.get_json(), {"points": 109})
