// ============================================
// Example: Comprehensive Regex Application
// Category: standard-library/regex
// Demonstrates: Real-world text processing pipeline
// ============================================

import console;
import regex;

console.log("=== Comprehensive Text Processing ===\n");

// Example 1: Email validator
console.log("Example 1: Email validation system");

function isValidEmail(email) {
    pattern = regex.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');
    return pattern.test(email);
}

emails = [
    "user@example.com",
    "invalid.email",
    "admin@site.org",
    "test@",
    "good.name@company.co.uk"
];

console.log("Email validation:");
for (email in emails) {
    valid = isValidEmail(email);
    status = "valid";
    if (!valid) {
        status = "invalid";
    }
    console.log("  " + email + " - " + status);
}

// Example 2: Log parser
console.log("\nExample 2: Log file parse");

function parseLogEntry(line) {
    pattern = regex.compile('^\[(?P<level>\w+)\]\s+(?P<timestamp>[\d-]+\s+[\d:]+)\s+-\s+(?P<message>.+)$');
    match = pattern.search(line);

    if (match != null) {
        return match.groupDict();
    }
    return null;
}

logLines = [
    "[ERROR] 2025-10-05 10:32:15 - Database connection failed",
    "[INFO] 2025-10-05 10:32:20 - Server started successfully",
    "[WARN] 2025-10-05 10:32:25 - High memory usage detected",
    "[ERROR] 2025-10-05 10:32:30 - Failed to process request"
];

errorCount = 0;
warnCount = 0;
infoCount = 0;

console.log("Parsing logs:");
for (line in logLines) {
    entry = parseLogEntry(line);
    if (entry != null) {
        console.log("  [" + entry.level + "] " + entry.timestamp + ": " + entry.message);

        if (entry.level == "ERROR") {
            errorCount = errorCount + 1;
        } elif (entry.level == "WARN") {
            warnCount = warnCount + 1;
        } else {
            infoCount = infoCount + 1;
        }
    }
}

console.log("Summary: " + str(errorCount) + " errors, " + str(warnCount) + " warnings, " + str(infoCount) + " info");

// Example 3: URL extractor and classifier
console.log("\nExample 3: URL extraction and classification");

function extractUrls(text) {
    pattern = regex.compile('(https?)://([\w.-]+)(/[\w/.-]*)?');
    matches = pattern.finditer(text);

    urls = [];
    for (match in matches) {
        url = {
            full: match.group(0),
            protocol: match.group(1),
            domain: match.group(2),
            path: match.group(3)
        };
        urls = urls + [url];
    }
    return urls;
}

text = "Check https://example.com/api and http://site.org/docs for information";
urls = extractUrls(text);

console.log("Extracted URLs:");
for (url in urls) {
    console.log("  " + url.full);
    console.log("    Protocol: " + url.protocol);
    console.log("    Domain: " + url.domain);
    console.log("    Path: " + str(url.path));
}

// Example 4: Data sanitizer
console.log("\nExample 4: Data sanitization");

function sanitizeData(data) {
    result = data;

    // Remove email addresses
    result = regex.sub('\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL]', result);

    // Remove phone numbers
    result = regex.sub('\b\d{3}-\d{3}-\d{4}\b', '[PHONE]', result);

    // Remove credit card numbers
    result = regex.sub('\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '[CARD]', result);

    // Remove SSN
    result = regex.sub('\b\d{3}-\d{2}-\d{4}\b', '[SSN]', result);

    return result;
}

text = "Contact john@example.com or call 555-123-4567. Card: 1234-5678-9012-3456. SSN: 123-45-6789.";
sanitized = sanitizeData(text);

console.log("Original:");
console.log("  " + text);
console.log("Sanitized:");
console.log("  " + sanitized);

// Example 5: Markdown link parser
console.log("\nExample 5: Markdown link extraction");

function extractMarkdownLinks(markdown) {
    pattern = regex.compile('\[(?P<text>[^\]]+)\]\((?P<url>[^\)]+)\)');
    matches = pattern.finditer(markdown);

    links = [];
    for (match in matches) {
        link = {
            text: match.group("text"),
            url: match.group("url")
        };
        links = links + [link];
    }
    return links;
}

markdown = "Check [Google](https://google.com) and [GitHub](https://github.com) for info.";
links = extractMarkdownLinks(markdown);

console.log("Markdown links:");
for (link in links) {
    console.log("  " + link.text + " -> " + link.url);
}

// Example 6: Configuration parser
console.log("\nExample 6: Configuration file parse");

function parseConfig(configText) {
    config = {};

    // Parse key=value pairs
    pattern = regex.compile('^\s*(\w+)\s*=\s*(.+?)\s*$', regex.MULTILINE());
    matches = pattern.finditer(configText);

    for (match in matches) {
        key = match.group(1);
        value = match.group(2);
        // In real code: config[key] = value
        console.log("  " + key + " = " + value);
    }

    return config;
}

configText = "width = 800\nheight = 600\nfullscreen = true\nfps = 60";
console.log("Parsing configuration:");
config = parseConfig(configText);

// Example 7: Text statistics
console.log("\nExample 7: Text analysis");

function analyzeText(text) {
    stats = {
        sentences: 0,
        words: 0,
        numbers: 0,
        emails: 0,
        urls: 0
    };

    // Count sentences
    sentences = regex.findall('[.!?]+', text);
    stats.sentences = len(sentences);

    // Count words
    words = regex.findall('\b\w+\b', text);
    stats.words = len(words);

    // Count numbers
    numbers = regex.findall('\b\d+\b', text);
    stats.numbers = len(numbers);

    // Count emails
    emails = regex.findall('\b[\w.-]+@[\w.-]+\.\w+\b', text);
    stats.emails = len(emails);

    // Count URLs
    urls = regex.findall('https?://[\w./]+', text);
    stats.urls = len(urls);

    return stats;
}

text = "I have 5 apples. Contact me at user@example.com or visit https://example.com! There are 3 oranges.";
stats = analyzeText(text);

console.log("Text statistics:");
console.log("  Sentences: " + str(stats.sentences));
console.log("  Words: " + str(stats.words));
console.log("  Numbers: " + str(stats.numbers));
console.log("  Email addresses: " + str(stats.emails));
console.log("  URLs: " + str(stats.urls));

// Example 8: CSV parser
console.log("\nExample 8: Simple CSV parsing");

function parseCSV(csvLine) {
    // Handle quoted fields with commas
    pattern = regex.compile('(?:^|,)(?:"([^"]*)"|([^,]*))');
    matches = pattern.finditer(csvLine);

    fields = [];
    for (match in matches) {
        // Get quoted or unquoted field
        field = match.group(1);
        if (field == null) {
            field = match.group(2);
        }
        if (field != null) {
            fields = fields + [field];
        }
    }
    return fields;
}

csvLines = [
    "John,Doe,30",
    '"Jane","Smith, Jr.",25',
    "Bob,Johnson,35"
];

console.log("Parsing CSV:");
for (line in csvLines) {
    fields = parseCSV(line);
    console.log("  " + str(fields));
}

// Example 9: Password strength checker
console.log("\nExample 9: Password strength validation");

function checkPasswordStrength(password) {
    hasLower = regex.test('[a-z]', password);
    hasUpper = regex.test('[A-Z]', password);
    hasDigit = regex.test('\d', password);
    hasSpecial = regex.test('[!@#$%^&*(),.?":{}|<>]', password);
    longEnough = len(password) >= 8;

    score = 0;
    if (hasLower) {
        score = score + 1;
    }
    if (hasUpper) {
        score = score + 1;
    }
    if (hasDigit) {
        score = score + 1;
    }
    if (hasSpecial) {
        score = score + 1;
    }
    if (longEnough) {
        score = score + 1;
    }

    return score;
}

passwords = [
    "password",
    "Password1",
    "P@ssw0rd",
    "MyS3cur3P@ss!"
];

console.log("Password strength:");
for (pwd in passwords) {
    strength = checkPasswordStrength(pwd);
    console.log("  " + pwd + " - Score: " + str(strength) + "/5");
}

// Example 10: Template engine
console.log("\nExample 10: Simple template replacement");

function fillTemplate(template, data) {
    result = template;

    // Replace {{key}} with values
    pattern = regex.compile('\{\{(\w+)\}\}');
    matches = pattern.finditer(template);

    for (match in matches) {
        key = match.group(1);
        placeholder = match.group(0);

        // In real code, you'd look up key in data object
        if (key == "name") {
            result = regex.sub(regex.escape(placeholder), "John", result, 1);
        } elif (key == "age") {
            result = regex.sub(regex.escape(placeholder), "30", result, 1);
        }
    }

    return result;
}

template = "Hello {{name}}, you are {{age}} years old!";
filled = fillTemplate(template, {});
console.log("Template: " + template);
console.log("Filled: " + filled);

console.log("\n=== Comprehensive Example Complete ===");
