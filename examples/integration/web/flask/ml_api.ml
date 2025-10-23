// ML API - Business logic in ML, web layer in Flask
// This demonstrates ML functions used as Flask route handlers

import regex;
import math;
import datetime;

// User validation
function validate_user(user) {
    errors = [];

    // Validate username
    if (len(user.username) < 3) {
        errors = errors + ["Username must be at least 3 characters"];
    }
    if (len(user.username) > 20) {
        errors = errors + ["Username must be at most 20 characters"];
    }

    // Validate email
    if (!regex.test("@", user.email)) {
        errors = errors + ["Email must contain @"];
    }
    if (!regex.test("\\.", user.email)) {
        errors = errors + ["Email must contain a domain"];
    }

    // Validate age
    if (user.age < 13) {
        errors = errors + ["User must be at least 13 years old"];
    }
    if (user.age > 120) {
        errors = errors + ["Invalid age"];
    }

    return {
        valid: len(errors) == 0,
        errors: errors
    };
}

// Calculate user score
function calculate_user_score(activity) {
    // Base score from posts
    post_score = activity.posts * 10;

    // Bonus for comments (engagement)
    comment_score = activity.comments * 5;

    // Bonus for likes received
    like_score = activity.likes_received * 2;

    // Penalty for reports
    report_penalty = activity.reports * -50;

    // Calculate total
    total = post_score + comment_score + like_score + report_penalty;

    // Ensure non-negative
    if (total < 0) {
        total = 0;
    }

    // Calculate level (every 100 points = 1 level)
    level = math.floor(total / 100) + 1;

    return {
        score: total,
        level: level,
        breakdown: {
            posts: post_score,
            comments: comment_score,
            likes: like_score,
            reports: report_penalty
        }
    };
}

// Analyze user cohort
function analyze_cohort(users) {
    if (len(users) == 0) {
        return null;
    }

    // Calculate statistics
    total_age = 0;
    total_score = 0;
    active_users = 0;
    i = 0;

    while (i < len(users)) {
        user = users[i];
        total_age = total_age + user.age;
        total_score = total_score + user.score;

        if (user.active) {
            active_users = active_users + 1;
        }

        i = i + 1;
    }

    avg_age = total_age / len(users);
    avg_score = total_score / len(users);
    activity_rate = (active_users / len(users)) * 100;

    // Find age distribution
    age_groups = {
        teen: 0,
        young_adult: 0,
        adult: 0,
        senior: 0
    };

    i = 0;
    while (i < len(users)) {
        age = users[i].age;

        if (age < 20) {
            age_groups.teen = age_groups.teen + 1;
        } elif (age < 35) {
            age_groups.young_adult = age_groups.young_adult + 1;
        } elif (age < 60) {
            age_groups.adult = age_groups.adult + 1;
        } else {
            age_groups.senior = age_groups.senior + 1;
        }

        i = i + 1;
    }

    return {
        total_users: len(users),
        active_users: active_users,
        average_age: avg_age,
        average_score: avg_score,
        activity_rate: activity_rate,
        age_distribution: age_groups
    };
}

// Search users by criteria
function search_users(users, criteria) {
    results = [];
    i = 0;

    while (i < len(users)) {
        user = users[i];
        match = true;

        // Filter by username
        if (criteria.username != null) {
            if (!regex.test(criteria.username, user.username)) {
                match = false;
            }
        }

        // Filter by age range
        if (criteria.min_age != null) {
            if (user.age < criteria.min_age) {
                match = false;
            }
        }
        if (criteria.max_age != null) {
            if (user.age > criteria.max_age) {
                match = false;
            }
        }

        // Filter by active status
        if (criteria.active != null) {
            if (user.active != criteria.active) {
                match = false;
            }
        }

        // Filter by minimum score
        if (criteria.min_score != null) {
            if (user.score < criteria.min_score) {
                match = false;
            }
        }

        if (match) {
            results = results + [user];
        }

        i = i + 1;
    }

    return results;
}

// Generate analytics report
function generate_report(users, time_period) {
    analysis = analyze_cohort(users);

    if (analysis == null) {
        return {
            success: false,
            error: "No users to analyze"
        };
    }

    // Calculate engagement metrics
    high_engagement = 0;
    medium_engagement = 0;
    low_engagement = 0;

    i = 0;
    while (i < len(users)) {
        score = users[i].score;

        if (score >= 500) {
            high_engagement = high_engagement + 1;
        } elif (score >= 100) {
            medium_engagement = medium_engagement + 1;
        } else {
            low_engagement = low_engagement + 1;
        }

        i = i + 1;
    }

    return {
        success: true,
        generated_at: datetime.now(),
        period: time_period,
        summary: analysis,
        engagement: {
            high: high_engagement,
            medium: medium_engagement,
            low: low_engagement
        },
        recommendations: generate_recommendations(analysis)
    };
}

// Generate recommendations based on analytics
function generate_recommendations(analysis) {
    recommendations = [];

    // Check activity rate
    if (analysis.activity_rate < 50) {
        recommendations = recommendations + ["Consider engagement campaigns - activity rate is below 50%"];
    }

    // Check average score
    if (analysis.average_score < 100) {
        recommendations = recommendations + ["User engagement is low - consider incentives"];
    }

    // Check age distribution
    distribution = analysis.age_distribution;
    if (distribution.teen < 10) {
        recommendations = recommendations + ["Low youth engagement - consider youth-oriented features"];
    }

    if (len(recommendations) == 0) {
        recommendations = ["Metrics look healthy - maintain current strategy"];
    }

    return recommendations;
}
