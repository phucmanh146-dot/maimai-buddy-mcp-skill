"""Budget-first menu combination helper.

This module is deliberately offline: callers must pass menu items obtained from
a trusted source (for example, a successful official MCP response). It does not
fetch menus, invent discounts, or place orders.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import isfinite
from typing import Iterable


@dataclass(frozen=True)
class MenuItem:
    name: str
    price: float
    quantity: int = 1
    source: str = "official MCP result"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Menu item name must not be empty")
        if not isfinite(self.price) or self.price < 0:
            raise ValueError("Price must be a finite non-negative number")
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1")


@dataclass(frozen=True)
class Combination:
    items: tuple[MenuItem, ...]
    total_price: float
    budget_remaining: float


def find_budget_combinations(
    items: Iterable[MenuItem],
    budget: float,
    max_items: int = 3,
    limit: int = 10,
) -> list[Combination]:
    """Return unique candidate combinations within budget, best-fit first.

    Price is the per-unit price and quantity is the requested quantity for
    that line. The function only sums supplied values. It ranks combinations
    by budget utilization, then fewer lines; it is not a nutrition optimizer.
    """
    if not isfinite(budget) or budget < 0:
        raise ValueError("Budget must be a finite non-negative number")
    if max_items < 1:
        raise ValueError("max_items must be at least 1")
    if limit < 1:
        raise ValueError("limit must be at least 1")

    valid = list(items)
    found: dict[tuple[tuple[str, float, int], ...], Combination] = {}
    for size in range(1, min(max_items, len(valid)) + 1):
        for group in combinations(valid, size):
            total = round(sum(item.price * item.quantity for item in group), 2)
            if total <= budget:
                key = tuple(sorted((i.name, i.price, i.quantity) for i in group))
                found[key] = Combination(
                    items=tuple(group),
                    total_price=total,
                    budget_remaining=round(budget - total, 2),
                )

    return sorted(
        found.values(),
        key=lambda result: (
            -result.total_price,
            len(result.items),
            tuple(item.name for item in result.items),
        ),
    )[:limit]
