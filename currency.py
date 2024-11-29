# Conversion rates (example values)
currency_conversion = {
    "SEK": 1.0,   # Base currency
    "USD": 0.11,  # SEK to USD
    "EUR": 0.095, # SEK to EUR
    "GBP": 0.085, # SEK to GBP
    "CAD": 0.13   # SEK to CAD
}

def convert_price(price_sek, currency):
    """Convert price from SEK to the selected currency."""
    return round(price_sek * currency_conversion.get(currency, 1.0), 2)
