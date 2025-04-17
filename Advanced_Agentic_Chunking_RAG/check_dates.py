import re
from datetime import datetime

def check_date_range(file_path):
    """Check the date range in the WhatsApp chat file."""
    pattern = r'(\d{2}/\d{2}/\d{4}, \d{2}:\d{2}) - ([^:]+): (.+)'
    
    dates = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(pattern, line.strip())
            if match:
                timestamp = match.group(1)
                try:
                    date = datetime.strptime(timestamp, '%d/%m/%Y, %H:%M')
                    dates.append(date)
                except ValueError:
                    pass
    
    if dates:
        min_date = min(dates)
        max_date = max(dates)
        print(f"Date range in chat file: from {min_date.strftime('%d/%m/%Y')} to {max_date.strftime('%d/%m/%Y')}")
        
        # Count messages by year and month
        year_month_counts = {}
        for date in dates:
            key = (date.year, date.month)
            year_month_counts[key] = year_month_counts.get(key, 0) + 1
        
        print("\nMessage counts by year and month:")
        for (year, month), count in sorted(year_month_counts.items()):
            print(f"{year}-{month:02d}: {count} messages")
    else:
        print("No valid dates found in the chat file")

if __name__ == "__main__":
    check_date_range('chat_group.txt') 