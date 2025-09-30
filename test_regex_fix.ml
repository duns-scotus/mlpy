import regex;

// Test snake_case methods
emails = regex.extract_emails("Contact us at support@example.com or sales@test.org");
print("Emails found: " + str(len(emails)));

// Test replace_all
cleaned = regex.replace_all("<[^>]+>", "<p>Hello</p> <b>World</b>", "");
print("Cleaned HTML: " + cleaned);