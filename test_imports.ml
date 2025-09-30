// Test datetime module imports
import datetime;

now = datetime.now();
formatted = datetime.format_date(now, "%Y-%m-%d");
print("Current date: " + formatted);

// Test timestamp
ts = datetime.timestamp(now);
print("Timestamp: " + str(ts));
