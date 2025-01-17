from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")