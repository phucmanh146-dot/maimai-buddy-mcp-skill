import unittest

from src.maimai_buddy import MenuItem, find_budget_combinations


class BudgetCombinationTests(unittest.TestCase):
    def test_returns_only_combinations_within_budget(self):
        items = [
            MenuItem("A", 12.0),
            MenuItem("B", 8.0),
            MenuItem("C", 15.0),
        ]
        results = find_budget_combinations(items, budget=20.0, max_items=2)
        self.assertTrue(results)
        self.assertTrue(all(result.total_price <= 20.0 for result in results))
        self.assertEqual(results[0].total_price, 20.0)
        self.assertEqual(results[0].budget_remaining, 0.0)

    def test_empty_items_returns_empty_list(self):
        self.assertEqual(find_budget_combinations([], budget=10.0), [])

    def test_rejects_invalid_price(self):
        with self.assertRaises(ValueError):
            MenuItem("invalid", -1.0)

    def test_rejects_invalid_budget(self):
        with self.assertRaises(ValueError):
            find_budget_combinations([], budget=-1.0)


if __name__ == "__main__":
    unittest.main()
