import unittest
from decimal import Decimal

from src.savings import rank_quotes


class RankQuotesTests(unittest.TestCase):
    def test_cheapest_quote_first(self):
        quotes = [{"name": "A", "payable": "18.50"}, {"name": "B", "payable": 12}, {"name": "C"}]
        result = rank_quotes(quotes, price_key="payable")
        self.assertEqual([item["name"] for item in result], ["B", "A"])

    def test_budget_options_sort_before_over_budget(self):
        quotes = [{"name": "A", "payable": 8}, {"name": "B", "payable": 18}, {"name": "C", "payable": 11}]
        result = rank_quotes(quotes, price_key="payable", budget=Decimal("12"))
        self.assertEqual([item["name"] for item in result], ["A", "C", "B"])
        self.assertTrue(result[1]["_within_budget"])
        self.assertFalse(result[2]["_within_budget"])

    def test_invalid_amounts_are_ignored(self):
        quotes = [{"name": "A", "payable": "unknown"}, {"name": "B", "payable": -1}, {"name": "C", "payable": 10}]
        result = rank_quotes(quotes, price_key="payable")
        self.assertEqual([item["name"] for item in result], ["C"])


if __name__ == "__main__":
    unittest.main()
