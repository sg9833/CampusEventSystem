from datetime import datetime


def fmt_dt(value, fallback='TBD'):
    """Format ISO datetime strings like 2025-10-20T09:00:00 as '20 Oct 2025, 09:00'."""
    if not value:
        return fallback
    try:
        return datetime.fromisoformat(str(value).replace('Z', '')).strftime('%d %b %Y, %H:%M')
    except ValueError:
        return str(value)


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"
