def format_price_and_volume(price, volume=None):
    formatted_price = f"${price:.2f} USDT"
    # Форматируем объем в миллиардах с двумя знаками после запятой, если он не None
    if volume is not None:
        volume_in_billions = volume / 1_000_000_000
        formatted_volume = f"{volume_in_billions:.2f}B"
    else:
        formatted_volume = "N/A"
    return formatted_price, formatted_volume
