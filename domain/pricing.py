from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    unit_price: float


class PricingStrategy(ABC):
    @abstractmethod
    def apply(self, subtotal:float, items:List[LineItem])->float:
        pass


class NoDiscount(PricingStrategy):
    def apply(self, subtotal, items):
        return subtotal


class PercentageDiscount(PricingStrategy):
    def __init__(self, percent: float) -> None:
        assert 0<= percent <= 100
        self.percent = percent

    # TODO: Implement the main calculation method that reduces the input by a percentage
    def apply(self, subtotal, items):
        total = subtotal * (1 - self.percent / 100) 
        return round(total, 2)

class BulkItemDiscount(PricingStrategy):
    """If any single item's quantity >= threshold, apply a per-item discount for that SKU."""
    def __init__(self, sku: str, threshold: int, per_item_off: float) -> None:
        # TODO: Store the parameters needed to identify items and calculate reductions
        self.sku = sku
        self.threshold = threshold
        self.per_item_off = per_item_off

    # TODO: Implement logic to iterate through items and apply reductions based on quantity thresholds
    def apply(self, subtotal, items):
        for item in items:
            if (item.sku == self.sku) and item.qty >= (self.threshold):
                subtotal -= item.qty * self.per_item_off
        return subtotal
            


class CompositeStrategy(PricingStrategy):
    """Compose multiple strategies; apply in order."""
    def __init__(self, strategies: List[PricingStrategy]) -> None:
        # TODO: Store the collection of strategies to be applied sequentially
        self.strategies = strategies

    # TODO: Implement method that applies each strategy in sequence, using the output of one as input to the next
    def apply(self, subtotal, items):
        for strategy in self.strategies:
            subtotal = strategy.apply(subtotal, items)
        return subtotal

def compute_subtotal(items: list[LineItem]) -> float:
    return round(sum(it.unit_price * it.qty for it in items), 2)
