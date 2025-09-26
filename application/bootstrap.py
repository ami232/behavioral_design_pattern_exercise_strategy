from domain.pricing import BulkItemDiscount, CompositeStrategy, NoDiscount, PercentageDiscount, PricingStrategy


def choose_strategy(kind: str, **kwargs) -> PricingStrategy:
    if kind == "none":
        return NoDiscount()
    elif kind == "percent":
        percent = kwargs.get("percent")
        if percent is None:
            raise ValueError("Missing 'percent' argument for PercentageDiscount")
        return PercentageDiscount(percent)
    elif kind == "bulk":
        sku = kwargs.get("sku")
        threshold = kwargs.get("threshold")
        per_item_off = kwargs.get("per_item_off")
        if sku is None or threshold is None or per_item_off is None:
            raise ValueError("Missing 'sku', 'threshold' or 'per_item_off' argument for BulkItemDiscount")
        return BulkItemDiscount(sku, threshold, per_item_off)
    elif kind == "composite":
        # For composite strategy, create a list from the provided parameters
        strategies = []
        percent = kwargs.get("percent")
        sku = kwargs.get("sku")
        threshold = kwargs.get("threshold")
        per_item_off = kwargs.get("per_item_off")
        
        if percent is not None and percent > 0:
            strategies.append(PercentageDiscount(percent))
        
        if sku and threshold is not None and per_item_off is not None:
            strategies.append(BulkItemDiscount(sku, threshold, per_item_off))
        
        if not strategies:
            raise ValueError("No valid strategies provided for CompositeStrategy")
        
        return CompositeStrategy(strategies)
    else:
        raise ValueError(f"Unknown strategy kind: {kind}")
