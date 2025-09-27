// Test secure Python-style attribute access
text = "Hello World";
upper_text = text.upper();
text_length = text.length();

arr = [1, 2, 3];
arr_length = arr.length();
arr.append(4);

obj = {name: "John", age: 30};
name = obj.name;

console.log("Text:", text);
console.log("Upper:", upper_text);
console.log("Text length:", text_length);
console.log("Array:", arr);
console.log("Array length:", arr_length);
console.log("Name:", name);