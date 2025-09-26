from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class LineItem:
    sku: str
    qty: int
    unit_price: float


class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, items: list[LineItem], current_total: float = None) -> float:
        """
        Calculate the price after applying the strategy.
        :param items: List of LineItem objects.
        :param current_total: Optional current total to apply further discounts.
        :return: Discounted price as float.
        """
        pass
    
    def apply(self, subtotal: float, items: list[LineItem]) -> float:
        """
        Apply the strategy - wrapper for calculate method for backwards compatibility.
        :param subtotal: The subtotal to apply the strategy to.
        :param items: List of LineItem objects.
        :return: Final price after applying the strategy.
        """
        return self.calculate(items, subtotal)


class NoDiscount(PricingStrategy):
    def calculate(self, items: list[LineItem], current_total: float = None) -> float:
        # Returns the original subtotal without any discount
        if current_total is not None:
            return round(current_total, 2)
        return compute_subtotal(items)


class PercentageDiscount(PricingStrategy):
    def __init__(self, percent: float) -> None:
        if not (0 <= percent <= 100):
            raise ValueError("Discount percent must be between 0 and 100.")
        self.percent = percent

    def calculate(self, items: list[LineItem], current_total: float = None) -> float:
        # Applies percentage discount to the subtotal or current_total
        base = current_total if current_total is not None else compute_subtotal(items)
        discount = base * (self.percent / 100)
        return round(base - discount, 2)


class BulkItemDiscount(PricingStrategy):
    """If any single item's quantity >= threshold, apply a per-item discount for that SKU."""
    def __init__(self, sku: str, threshold: int, per_item_off: float) -> None:
        self.sku = sku
        self.threshold = threshold
        self.per_item_off = per_item_off

    def calculate(self, items: list[LineItem], current_total: float = None) -> float:
        # Applies bulk discount for the specified SKU if quantity threshold is met
        subtotal = current_total if current_total is not None else compute_subtotal(items)
        for item in items:
            if item.sku == self.sku and item.qty >= self.threshold:
                discount = item.qty * self.per_item_off
                subtotal -= discount
        return round(subtotal, 2)


class CompositeStrategy(PricingStrategy):
    """Compose multiple strategies; apply in order."""
    def __init__(self, strategies: list[PricingStrategy]) -> None:
        self.strategies = strategies

    def calculate(self, items: list[LineItem], current_total: float = None) -> float:
        # Applies each strategy in sequence, passing the result to the next
        total = current_total if current_total is not None else compute_subtotal(items)
        for strategy in self.strategies:
            total = strategy.calculate(items, total)
        return round(total, 2)


def compute_subtotal(items: list[LineItem]) -> float:
    return round(sum(it.unit_price * it.qty for it in items), 2)
