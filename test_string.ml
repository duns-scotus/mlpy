// Test string module imports
import string;

text = "hello world";
upper = string.upper(text);
print("Uppercase: " + upper);

words = string.split(text, " ");
print("Word count: " + str(len(words)));

camel = string.camel_case("hello_world_test");
print("Camel case: " + camel);
