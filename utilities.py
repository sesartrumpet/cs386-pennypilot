# Formats a numeric amount into a currency string with commas and two decimal places.
# Example: 1234.5 → "$1,234.50"
def format_currency(amount):
    return f"${amount:,.2f}"
