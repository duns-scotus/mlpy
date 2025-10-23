// ============================================
// Example: Basic DateTime Operations
// Category: standard-library/datetime
// Demonstrates: now(), create(), timestamp(), date/time components
// ============================================

import console;
import datetime;

console.log("=== Basic DateTime Operations ===\n");

// Get current datetime
now = datetime.now();
console.log("Current datetime:");
console.log("  Year: " + str(now.year()));
console.log("  Month: " + str(now.month()));
console.log("  Day: " + str(now.day()));
console.log("  Hour: " + str(now.hour()));
console.log("  Minute: " + str(now.minute()));
console.log("  Second: " + str(now.second()));
console.log("  Weekday: " + str(now.weekday()) + " (0=Monday, 6=Sunday)");

// Get Unix timestamp
timestamp = now.timestamp();
console.log("\nUnix timestamp: " + str(timestamp));

// Create specific datetime
console.log("\n=== Creating Specific DateTime ===");
birthday = datetime.create(1990, 5, 15, 14, 30, 0);
console.log("Birthday datetime created:");
console.log("  Date: " + str(birthday.year()) + "-" + str(birthday.month()) + "-" + str(birthday.day()));
console.log("  Time: " + str(birthday.hour()) + ":" + str(birthday.minute()) + ":" + str(birthday.second()));

// Format datetime components
console.log("\n=== Formatting DateTime ===");
year = str(now.year());
month = str(now.month());
day = str(now.day());
hour = str(now.hour());
minute = str(now.minute());

// Add leading zeros for formatting
if (now.month() < 10) {
    month = "0" + month;
}
if (now.day() < 10) {
    day = "0" + day;
}
if (now.hour() < 10) {
    hour = "0" + hour;
}
if (now.minute() < 10) {
    minute = "0" + minute;
}

formatted = year + "-" + month + "-" + day + " " + hour + ":" + minute;
console.log("Formatted: " + formatted);

// Weekday names
console.log("\n=== Weekday Names ===");
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
todayIndex = now.weekday();
todayName = weekdays[todayIndex];
console.log("Today is: " + todayName);

// Compare timestamps
console.log("\n=== Timestamp Comparison ===");
earlier = datetime.create(2020, 1, 1, 0, 0, 0);
later = datetime.create(2025, 1, 1, 0, 0, 0);

earlierTs = earlier.timestamp();
laterTs = later.timestamp();

console.log("2020-01-01 timestamp: " + str(earlierTs));
console.log("2025-01-01 timestamp: " + str(laterTs));
console.log("2025 is later: " + str(laterTs > earlierTs));

console.log("\n=== Basic DateTime Complete ===");
