// ============================================
// Comprehensive Example: Event Management System
// Category: standard-library/datetime
// Demonstrates: Complete datetime module capabilities
// ============================================

import console;
import datetime;

console.log("=== Event Management System ===\n");

// ============================================
// Event Creation and Scheduling
// ============================================

console.log("=== Creating Events ===");

// Define events
events = [
    {
        name: "Team Meeting",
        start: datetime.create(2025, 10, 7, 10, 0, 0),
        duration: 60
    },
    {
        name: "Lunch Break",
        start: datetime.create(2025, 10, 7, 12, 0, 0),
        duration: 60
    },
    {
        name: "Project Review",
        start: datetime.create(2025, 10, 7, 14, 30, 0),
        duration: 90
    },
    {
        name: "Client Call",
        start: datetime.create(2025, 10, 7, 16, 30, 0),
        duration: 30
    }
];

// Display events with end times
i = 0;
while (i < len(events)) {
    event = events[i];
    start = event.start;
    endTime = start.addMinutes(event.duration);

    startHour = start.hour();
    startMin = start.minute();
    endHour = endTime.hour();
    endMin = endTime.minute();

    // Format times with leading zeros
    startFormatted = str(startHour) + ":" + (startMin < 10 ? "0" : "") + str(startMin);
    endFormatted = str(endHour) + ":" + (endMin < 10 ? "0" : "") + str(endMin);

    console.log(event.name + ": " + startFormatted + " - " + endFormatted + " (" + str(event.duration) + " min)");
    i = i + 1;
}

// ============================================
// Time Availability Checker
// ============================================

console.log("\n=== Checking Availability ===");

function isTimeSlotAvailable(proposedStart, proposedDuration, existingEvents) {
    proposedEnd = proposedStart.addMinutes(proposedDuration);
    proposedStartTs = proposedStart.timestamp();
    proposedEndTs = proposedEnd.timestamp();

    i = 0;
    while (i < len(existingEvents)) {
        event = existingEvents[i];
        eventStart = event.start;
        eventEnd = eventStart.addMinutes(event.duration);

        eventStartTs = eventStart.timestamp();
        eventEndTs = eventEnd.timestamp();

        // Check for overlap
        if (proposedStartTs < eventEndTs && proposedEndTs > eventStartTs) {
            return {available: false, conflict: event.name};
        }

        i = i + 1;
    }

    return {available: true, conflict: null};
}

// Try to schedule new meeting
newMeetingStart = datetime.create(2025, 10, 7, 11, 0, 0);
newMeetingDuration = 30;

result = isTimeSlotAvailable(newMeetingStart, newMeetingDuration, events);
console.log("Can schedule 11:00 meeting? " + str(result.available));
if (!result.available) {
    console.log("  Conflict with: " + result.conflict);
}

// Try another time slot
newMeetingStart2 = datetime.create(2025, 10, 7, 13, 0, 0);
result2 = isTimeSlotAvailable(newMeetingStart2, newMeetingDuration, events);
console.log("Can schedule 13:00 meeting? " + str(result2.available));

// ============================================
// Daily Schedule Summary
// ============================================

console.log("\n=== Daily Schedule Summary ===");

// Get day boundaries
firstEvent = events[0].start;
dayStart = firstEvent.startOfDay().addHours(9);   // Workday 9 AM
dayEnd = firstEvent.startOfDay().addHours(17);    // Workday 5 PM

console.log("Workday: " + str(dayStart.hour()) + ":00 - " + str(dayEnd.hour()) + ":00");

// Calculate total scheduled time
totalScheduledMinutes = 0;
i = 0;
while (i < len(events)) {
    totalScheduledMinutes = totalScheduledMinutes + events[i].duration;
    i = i + 1;
}

totalScheduledHours = totalScheduledMinutes / 60;
workdayMinutes = 8 * 60;  // 8 hour workday
freeMinutes = workdayMinutes - totalScheduledMinutes;

console.log("Total scheduled: " + str(round(totalScheduledHours, 1)) + " hours");
console.log("Free time: " + str(freeMinutes) + " minutes");

// ============================================
// Week Planning
// ============================================

console.log("\n=== Week Planning ===");

weekStart = datetime.create(2025, 10, 6, 0, 0, 0).startOfDay();  // Monday
console.log("Week starting: " + str(weekStart.year()) + "-" + str(weekStart.month()) + "-" + str(weekStart.day()));

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

// Show next 7 days
day = 0;
while (day < 7) {
    currentDay = weekStart.addDays(day);
    dayName = weekdays[currentDay.weekday()];
    dateStr = str(currentDay.month()) + "/" + str(currentDay.day());

    console.log("  " + dayName + " " + dateStr);
    day = day + 1;
}

// ============================================
// Deadline Tracking
// ============================================

console.log("\n=== Deadline Tracking ===");

now = datetime.create(2025, 10, 7, 14, 0, 0);
deadlines = [
    {task: "Project proposal", due: datetime.create(2025, 10, 10, 17, 0, 0)},
    {task: "Code review", due: datetime.create(2025, 10, 8, 12, 0, 0)},
    {task: "Documentation", due: datetime.create(2025, 10, 15, 9, 0, 0)}
];

console.log("Current time: " + str(now.month()) + "/" + str(now.day()) + " " + str(now.hour()) + ":00");
console.log("\nUpcoming deadlines:");

i = 0;
while (i < len(deadlines)) {
    deadline = deadlines[i];
    due = deadline.due;

    // Calculate hours until deadline
    nowTs = now.timestamp();
    dueTs = due.timestamp();
    secondsUntil = dueTs - nowTs;
    hoursUntil = secondsUntil / 3600;
    daysUntil = hoursUntil / 24;

    status = "OK";
    if (hoursUntil < 24) {
        status = "URGENT";
    } elif (daysUntil < 3) {
        status = "SOON";
    }

    console.log("  " + deadline.task + ": " + str(round(daysUntil, 1)) + " days - " + status);
    i = i + 1;
}

// ============================================
// Time Zone Awareness (Basic)
// ============================================

console.log("\n=== Time Zone Basics ===");

// Create UTC midnight
utcMidnight = datetime.create(2025, 10, 7, 0, 0, 0);
console.log("UTC midnight timestamp: " + str(utcMidnight.timestamp()));

// Convert to different zones (simplified - hours offset)
estOffset = -5;  // EST is UTC-5
pstOffset = -8;  // PST is UTC-8

estTime = utcMidnight.addHours(estOffset);
pstTime = utcMidnight.addHours(pstOffset);

console.log("EST: " + str(estTime.hour()) + ":00 (" + str(estTime.day()) + "th)");
console.log("PST: " + str(pstTime.hour()) + ":00 (" + str(pstTime.day()) + "th)");

// ============================================
// Age Calculator
// ============================================

console.log("\n=== Age Calculator ===");

birthdate = datetime.create(1990, 5, 15, 0, 0, 0);
today = datetime.create(2025, 10, 7, 0, 0, 0);

// Simple age calculation (years)
birthYear = birthdate.year();
currentYear = today.year();
birthMonth = birthdate.month();
currentMonth = today.month();

age = currentYear - birthYear;
if (currentMonth < birthMonth) {
    age = age - 1;
}

console.log("Birthdate: " + str(birthYear) + "-" + str(birthMonth) + "-" + str(birthdate.day()));
console.log("Age: " + str(age) + " years");

// Days until next birthday
nextBirthday = datetime.create(currentYear, birthMonth, birthdate.day(), 0, 0, 0);
if (currentMonth > birthMonth || (currentMonth == birthMonth && today.day() > birthdate.day())) {
    nextBirthday = datetime.create(currentYear + 1, birthMonth, birthdate.day(), 0, 0, 0);
}

daysUntilBirthday = (nextBirthday.timestamp() - today.timestamp()) / 86400;
console.log("Days until next birthday: " + str(round(daysUntilBirthday)));

console.log("\n=== Event Management Complete ===");
