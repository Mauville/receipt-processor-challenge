# I saw no point in creating a class for this, since state is not needed right now.
# A refactor into a class for inheritance could be justified, if we ever needed to do
# different types of calculations depending on the receipt type i.e.
import decimal
from typing import List

from models.Receipt import Receipt, Item


def _count_alphanumeric(retailer: str) -> int:
    """
    Count 1 point for every alphanumeric character in the retailer name.
    """
    return sum(1 for char in retailer if char.isalnum())


def _count_is_round_amount(total: decimal.Decimal) -> int:
    """
    Count 50 points if the total is a round dollar amount with no cents.
    """
    return 50 if int(total) == total else 0


def _count_is_quartile(total: decimal.Decimal) -> int:
    """
    Count 25 points if the total is a multiple of 0.25.
    """
    return 25 if total % decimal.Decimal(0.25) == 0 else 0


def _count_even_items(item_count: int) -> int:
    """
    Count 5 points for every two items on the receipt.
    """
    if item_count < 2:
        return 0

    return 0 if item_count < 2 else 5 * item_count // 2


def _count_description_length(items: List[Item]) -> int:
    """
    If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    """

    total = 0
    for item in items:
        if len(item.shortDescription.strip()) % 3 == 0:
            total += round(item.price * decimal.Decimal(0.2))
    return total


def _count_odd_day(date: str) -> int:
    """
    Count 6 points if the day in the purchase date is odd.
    """

    return 6 if int(date[-1]) % 2 == 1 else 0


def _count_afternoon_purchase(time: str) -> int:
    """
    Count 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    """

    return 10 if 16 > int(time[:2]) >= 14 else 0


def count_points(receipt: Receipt) -> int:
    """
    Count reward points for a receipt.
    :param receipt: The receipt to count the points for.
    :return: The number of points a receipt is worth.
    """
    total = 0
    total += _count_alphanumeric(receipt.retailer)
    total += _count_is_round_amount(receipt.total)
    total += _count_is_quartile(receipt.total)
    total += _count_even_items(len(receipt.items))
    total += _count_description_length(receipt.items)
    total += _count_odd_day(receipt.purchaseDate)
    total += _count_afternoon_purchase(receipt.purchaseTime)
    return total
