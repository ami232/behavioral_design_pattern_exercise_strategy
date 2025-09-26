from __future__ import annotations
from domain.pricing import PricingStrategy, NoDiscount, PercentageDiscount, BulkItemDiscount, CompositeStrategy


def choose_strategy(kind: str, **kwargs) -> PricingStrategy:
    # TODO: Implement strategy selection logic based on the 'kind' parameter
    # Should support: "none", "percent", "bulk", "composite"
    # Each strategy type needs different parameters from **kwargs
    # Return the appropriate strategy instance or raise an error for unknown types
    if kind == "none":
        return NoDiscount()
    elif kind == "percent":
        percent = kwargs.get("percent", 0.0)
        return PercentageDiscount(percent)
    elif kind == "bulk":
        sku = kwargs.get("sku", "")
        threshold = kwargs.get("threshold", 0)
        per_item_off = kwargs.get("per_item_off", 0.0)
        return BulkItemDiscount(sku, threshold, per_item_off)
    elif kind == "composite":
        percent = kwargs.get("percent", 0.0)
        sku = kwargs.get("sku", "")
        threshold = kwargs.get("threshold", 0)
        per_item_off = kwargs.get("per_item_off", 0.0)
        percent_strategy = PercentageDiscount(percent)
        bulk_strategy = BulkItemDiscount(sku, threshold, per_item_off)
        return CompositeStrategy([percent_strategy, bulk_strategy])
    else:
        raise ValueError(f"Unknown strategy kind: {kind}")
