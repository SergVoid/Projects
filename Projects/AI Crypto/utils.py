def format_price_and_volume(price, volume=None):
    formatted_price = f"${price:.2f} USDT"
    formatted_volume = f"{volume:.2f}" if volume is not None else "N/A"
    return formatted_price, formatted_volume
