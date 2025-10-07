// ============================================
// Example: DateTime Arithmetic
// Category: standard-library/datetime
// Demonstrates: addDays(), addHours(), addMinutes(), addSeconds()
// ============================================

import console;
import datetime;

console.log("=== DateTime Arithmetic ===\n");

// Start with a base datetime
base = datetime.create(2025, 10, 7, 12, 0, 0);
console.log("Base datetime: " + str(base.year()) + "-" + str(base.month()) + "-" + str(base.day()) + " " + str(base.hour()) + ":00");

// Add days
console.log("\n=== Adding Days ===");
tomorrow = base.addDays(1);
console.log("Tomorrow: Day " + str(tomorrow.day()));

nextWeek = base.addDays(7);
console.log("Next week: " + str(nextWeek.year()) + "-" + str(nextWeek.month()) + "-" + str(nextWeek.day()));

nextMonth = base.addDays(30);
console.log("30 days later: " + str(nextMonth.year()) + "-" + str(nextMonth.month()) + "-" + str(nextMonth.day()));

// Subtract days (negative values)
yesterday = base.addDays(-1);
console.log("\nYesterday: Day " + str(yesterday.day()));

lastWeek = base.addDays(-7);
console.log("Last week: " + str(lastWeek.year()) + "-" + str(lastWeek.month()) + "-" + str(lastWeek.day()));

// Add hours
console.log("\n=== Adding Hours ===");
later = base.addHours(3);
console.log("3 hours later: " + str(later.hour()) + ":00");

muchLater = base.addHours(24);
console.log("24 hours later: Day " + str(muchLater.day()) + ", " + str(muchLater.hour()) + ":00");

earlier = base.addHours(-2);
console.log("2 hours earlier: " + str(earlier.hour()) + ":00");

// Add minutes
console.log("\n=== Adding Minutes ===");
soon = base.addMinutes(30);
console.log("30 minutes later: " + str(soon.hour()) + ":" + str(soon.minute()));

muchSooner = base.addMinutes(-45);
hour = muchSooner.hour();
minute = muchSooner.minute();
console.log("45 minutes earlier: " + str(hour) + ":" + str(minute));

// Add seconds
console.log("\n=== Adding Seconds ===");
immediate = base.addSeconds(90);
console.log("90 seconds later: " + str(immediate.minute()) + " min " + str(immediate.second()) + " sec");

// Chain operations
console.log("\n=== Chaining Operations ===");
future = base.addDays(7).addHours(5).addMinutes(30);
console.log("One week, 5 hours, 30 minutes later:");
console.log("  Date: " + str(future.year()) + "-" + str(future.month()) + "-" + str(future.day()));
console.log("  Time: " + str(future.hour()) + ":" + str(future.minute()));

// Practical example: Calculate deadline
console.log("\n=== Deadline Calculator ===");
startDate = datetime.create(2025, 10, 1, 9, 0, 0);
workDays = 5;
deadline = startDate.addDays(workDays);

console.log("Project start: " + str(startDate.month()) + "/" + str(startDate.day()) + " at " + str(startDate.hour()) + ":00");
console.log("Deadline (5 days): " + str(deadline.month()) + "/" + str(deadline.day()) + " at " + str(deadline.hour()) + ":00");

// Time until deadline
hoursUntil = workDays * 24;
console.log("Hours until deadline: " + str(hoursUntil));

// Practical example: Meeting scheduler
console.log("\n=== Meeting Scheduler ===");
meetingStart = datetime.create(2025, 10, 7, 14, 0, 0);
meetingDuration = 90;  // minutes
meetingEnd = meetingStart.addMinutes(meetingDuration);

console.log("Meeting start: " + str(meetingStart.hour()) + ":" + (meetingStart.minute() < 10 ? "0" : "") + str(meetingStart.minute()));
console.log("Meeting end: " + str(meetingEnd.hour()) + ":" + (meetingEnd.minute() < 10 ? "0" : "") + str(meetingEnd.minute()));
console.log("Duration: " + str(meetingDuration) + " minutes");

console.log("\n=== DateTime Arithmetic Complete ===");
