"""Deterministic comparison helpers for quotes returned by MCP tools."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Iterable


def rank_quotes(
    quotes: Iterable[dict[str, Any]],
    *,
    price_key: str,
    budget: Decimal | str | int | float | None = None,
) -> list[dict[str, Any]]:
    """Return quotes with a valid numeric price, cheapest first.

    `price_key` must match the actual field returned by the MCP tool; no field
    names are guessed. Quotes are copied and annotated with comparison fields.
    Within-budget options sort ahead of over-budget options when a budget is set.
    """
    limit = Decimal(str(budget)) if budget is not None else None
    ranked: list[dict[str, Any]] = []
    for quote in quotes:
        if price_key not in quote or quote[price_key] is None:
            continue
        try:
            amount = Decimal(str(quote[price_key]))
        except (InvalidOperation, ValueError):
            continue
        if not amount.is_finite() or amount < 0:
            continue
        item = dict(quote)
        item["_comparison_amount"] = str(amount)
        item["_within_budget"] = limit is None or amount <= limit
        ranked.append(item)
    return sorted(ranked, key=lambda item: (not item["_within_budget"], Decimal(item["_comparison_amount"])))
