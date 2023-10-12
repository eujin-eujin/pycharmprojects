def clean_subscribers(subscriber_count: str) -> float:
    """
    Clean the subscribers text by removing 'M' and 'K' suffixes and convert to appropriate numbers.

    Parameters:
        subscriber_count (str): A string representing the subscriber count with 'M' or 'K' suffixes.

    Returns:
        float: The cleaned subscriber count as a floating-point number.

    Example:
        >>> clean_subscribers('1.2M subscribers')
        1200000.0
        >>> clean_subscribers('500K subscribers')
        500000.0
        >>> clean_subscribers('1000 subscribers')
        1000.0
    """
    suffix_multiplier = {
        'M': 1000000,
        'K': 1000,
        'k':1000,
        'm':1000000,
    }
    for suffix, multiplier in suffix_multiplier.items():
        print(suffix,multiplier)
        if suffix in subscriber_count:
            subscriber_count = subscriber_count.replace(suffix, '')
            return float(subscriber_count) * multiplier

    return float(subscriber_count)
print(clean_subscribers('123k'))