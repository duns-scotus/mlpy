// ML Analytics - Async business logic for FastAPI
// This demonstrates ML functions used with async execution

import datetime;
import math;

// Process incoming event
function process_event(event) {

    // Validate event structure
    if (event.type == null) {
        return {
            success: false,
            error: "Event type is required"
        };
    }

    // Enrich event with metadata
    processed = {
        id: event.id,
        type: event.type,
        timestamp: datetime.now(),
        user_id: event.user_id,
        data: event.data,
        processed: true
    };

    // Add event-specific processing
    if (event.type == "page_view") {
        processed.category = "engagement";
        processed.priority = 1;
    } elif (event.type == "purchase") {
        processed.category = "conversion";
        processed.priority = 3;
    } elif (event.type == "error") {
        processed.category = "technical";
        processed.priority = 5;
    } else {
        processed.category = "other";
        processed.priority = 2;
    }

    return {
        success: true,
        event: processed
    };
}

// Calculate real-time metrics
function calculate_metrics(events) {
    if (len(events) == 0) {
        return {
            total_events: 0,
            by_type: {},
            by_category: {},
            high_priority: 0
        };
    }

    // Initialize counters
    by_type = {};
    by_category = {};
    high_priority_count = 0;

    i = 0;
    while (i < len(events)) {
        event = events[i];

        // Count by type
        event_type = event.type;
        if (by_type[event_type] == null) {
            by_type[event_type] = 0;
        }
        by_type[event_type] = by_type[event_type] + 1;

        // Count by category
        category = event.category;
        if (by_category[category] == null) {
            by_category[category] = 0;
        }
        by_category[category] = by_category[category] + 1;

        // Count high priority events
        if (event.priority >= 4) {
            high_priority_count = high_priority_count + 1;
        }

        i = i + 1;
    }

    return {
        total_events: len(events),
        by_type: by_type,
        by_category: by_category,
        high_priority: high_priority_count
    };
}

// Detect anomalies in event stream
function detect_anomalies(events, threshold) {
    anomalies = [];

    // Group events by user
    user_events = {};
    i = 0;
    while (i < len(events)) {
        event = events[i];
        user_id = event.user_id;

        if (user_events[user_id] == null) {
            user_events[user_id] = [];
        }

        user_events[user_id] = user_events[user_id] + [event];
        i = i + 1;
    }

    // Check each user's activity
    // Note: In ML, we can't iterate directly over object keys yet
    // So we'll check if specific patterns exist in the event stream

    // Detect rapid-fire events (possible bot)
    i = 1;
    while (i < len(events)) {
        prev_event = events[i - 1];
        curr_event = events[i];

        // Same user, rapid succession
        if (prev_event.user_id == curr_event.user_id) {
            if (prev_event.user_id != null) {
                anomalies = anomalies + [{
                    type: "rapid_events",
                    user_id: curr_event.user_id,
                    severity: "medium"
                }];
            }
        }

        i = i + 1;
    }

    // Detect error spikes
    error_count = 0;
    i = 0;
    while (i < len(events)) {
        if (events[i].type == "error") {
            error_count = error_count + 1;
        }
        i = i + 1;
    }

    error_rate = (error_count / len(events)) * 100;
    if (error_rate > threshold) {
        anomalies = anomalies + [{
            type: "error_spike",
            error_rate: error_rate,
            threshold: threshold,
            severity: "high"
        }];
    }

    return {
        anomaly_count: len(anomalies),
        anomalies: anomalies,
        clean: len(anomalies) == 0
    };
}

// Generate dashboard summary
function generate_dashboard(events, time_range) {
    metrics = calculate_metrics(events);
    anomalies = detect_anomalies(events, 10.0);

    // Calculate engagement score
    engagement_score = 0;
    if (metrics.by_category["engagement"] != null) {
        engagement_score = (metrics.by_category["engagement"] / metrics.total_events) * 100;
    }

    // Calculate conversion rate
    conversion_rate = 0;
    if (metrics.by_category["conversion"] != null) {
        conversion_rate = (metrics.by_category["conversion"] / metrics.total_events) * 100;
    }

    // Health status
    health_status = "healthy";
    if (anomalies.anomaly_count > 5) {
        health_status = "critical";
    } elif (anomalies.anomaly_count > 2) {
        health_status = "warning";
    }

    return {
        time_range: time_range,
        total_events: metrics.total_events,
        health_status: health_status,
        engagement_score: engagement_score,
        conversion_rate: conversion_rate,
        metrics: metrics,
        anomalies: anomalies,
        high_priority_alerts: metrics.high_priority
    };
}

// Filter events by criteria
function filter_events(events, filters) {
    results = [];
    i = 0;

    while (i < len(events)) {
        event = events[i];
        match = true;

        // Filter by type
        if (filters.type != null) {
            if (event.type != filters.type) {
                match = false;
            }
        }

        // Filter by category
        if (filters.category != null) {
            if (event.category != filters.category) {
                match = false;
            }
        }

        // Filter by user
        if (filters.user_id != null) {
            if (event.user_id != filters.user_id) {
                match = false;
            }
        }

        // Filter by priority
        if (filters.min_priority != null) {
            if (event.priority < filters.min_priority) {
                match = false;
            }
        }

        if (match) {
            results = results + [event];
        }

        i = i + 1;
    }

    return results;
}

// Aggregate events by time window
function aggregate_by_window(events, window_size) {
    if (len(events) == 0) {
        return [];
    }

    // Group events into windows
    windows = [];
    current_window = [];
    window_count = 0;

    i = 0;
    while (i < len(events)) {
        current_window = current_window + [events[i]];

        // When window is full, calculate metrics
        if (len(current_window) >= window_size) {
            metrics = calculate_metrics(current_window);
            windows = windows + [{
                window_id: window_count,
                event_count: len(current_window),
                metrics: metrics
            }];

            current_window = [];
            window_count = window_count + 1;
        }

        i = i + 1;
    }

    // Add remaining events as final window
    if (len(current_window) > 0) {
        metrics = calculate_metrics(current_window);
        windows = windows + [{
            window_id: window_count,
            event_count: len(current_window),
            metrics: metrics
        }];
    }

    return windows;
}
