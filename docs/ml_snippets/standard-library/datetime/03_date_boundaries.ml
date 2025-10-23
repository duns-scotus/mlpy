// ============================================
// Example: Date Boundaries
// Category: standard-library/datetime
// Demonstrates: startOfDay(), endOfDay(), startOfMonth(), endOfMonth()
// ============================================

import console;
import datetime;

console.log("=== Date Boundaries ===\n");

// Current datetime with specific time
now = datetime.create(2025, 10, 15, 14, 35, 47);
console.log("Current datetime: " + str(now.year()) + "-" + str(now.month()) + "-" + str(now.day()) + " " + str(now.hour()) + ":" + str(now.minute()) + ":" + str(now.second()));

// Start of day
console.log("\n=== Start of Day ===");
dayStart = now.startOfDay();
console.log("Start of day: " + str(dayStart.hour()) + ":" + str(dayStart.minute()) + ":" + str(dayStart.second()));
console.log("Timestamp: " + str(dayStart.timestamp()));

// End of day
console.log("\n=== End of Day ===");
dayEnd = now.endOfDay();
console.log("End of day: " + str(dayEnd.hour()) + ":" + str(dayEnd.minute()) + ":" + str(dayEnd.second()));
console.log("Timestamp: " + str(dayEnd.timestamp()));

// Calculate seconds in a day
secondsInDay = dayEnd.timestamp() - dayStart.timestamp();
console.log("Seconds in this day: " + str(secondsInDay));

// Start of month
console.log("\n=== Start of Month ===");
monthStart = now.startOfMonth();
console.log("Start of month:");
console.log("  Date: " + str(monthStart.year()) + "-" + str(monthStart.month()) + "-" + str(monthStart.day()));
console.log("  Time: " + str(monthStart.hour()) + ":" + str(monthStart.minute()) + ":" + str(monthStart.second()));

// End of month
console.log("\n=== End of Month ===");
monthEnd = now.endOfMonth();
console.log("End of month:");
console.log("  Date: " + str(monthEnd.year()) + "-" + str(monthEnd.month()) + "-" + str(monthEnd.day()));
console.log("  Time: " + str(monthEnd.hour()) + ":" + str(monthEnd.minute()) + ":" + str(monthEnd.second()));

// Days in month
daysInMonth = monthEnd.day();
console.log("Days in this month: " + str(daysInMonth));

// Practical example: Daily report time range
console.log("\n=== Daily Report Time Range ===");
reportDate = datetime.create(2025, 10, 7, 0, 0, 0);
reportStart = reportDate.startOfDay();
reportEnd = reportDate.endOfDay();

console.log("Report for: " + str(reportDate.year()) + "-" + str(reportDate.month()) + "-" + str(reportDate.day()));
console.log("Start timestamp: " + str(reportStart.timestamp()));
console.log("End timestamp: " + str(reportEnd.timestamp()));

// Practical example: Monthly billing period
console.log("\n=== Monthly Billing Period ===");
billingDate = datetime.create(2025, 10, 1, 0, 0, 0);
billingStart = billingDate.startOfMonth();
billingEnd = billingDate.endOfMonth();

console.log("Billing period:");
console.log("  Start: " + str(billingStart.year()) + "-" + str(billingStart.month()) + "-" + str(billingStart.day()));
console.log("  End: " + str(billingEnd.year()) + "-" + str(billingEnd.month()) + "-" + str(billingEnd.day()));
console.log("  Days: " + str(billingEnd.day()));

// Practical example: Check if datetime is start/end of day
console.log("\n=== Check Boundaries ===");
testTime1 = datetime.create(2025, 10, 7, 0, 0, 0);
testTime2 = datetime.create(2025, 10, 7, 14, 30, 0);

isStartOfDay = testTime1.hour() == 0 && testTime1.minute() == 0 && testTime1.second() == 0;
console.log("Is " + str(testTime1.hour()) + ":00 start of day? " + str(isStartOfDay));

isMidday = testTime2.hour() == 14;
console.log("Is " + str(testTime2.hour()) + ":30 in afternoon? " + str(isMidday));

// Working hours boundaries
console.log("\n=== Working Hours ===");
workDay = datetime.create(2025, 10, 7, 12, 0, 0);
workStart = workDay.startOfDay().addHours(9);  // 9 AM
workEnd = workDay.startOfDay().addHours(17);   // 5 PM

console.log("Work hours:");
console.log("  Start: " + str(workStart.hour()) + ":00");
console.log("  End: " + str(workEnd.hour()) + ":00");

// Check if time is within working hours
currentTime = datetime.create(2025, 10, 7, 14, 30, 0);
currentHour = currentTime.hour();
isWorkingHours = currentHour >= 9 && currentHour < 17;
console.log("\nIs " + str(currentHour) + ":30 within working hours? " + str(isWorkingHours));

console.log("\n=== Date Boundaries Complete ===");
