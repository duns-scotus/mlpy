// ============================================
// Example: Object Techniques
// Category: tutorial
// Demonstrates: Working with objects and properties
// ============================================

import console;

// Creating and accessing objects
console.log("=== Basic Objects ===");
person = {
    name: "Alice",
    age: 30,
    city: "Boston"
};
console.log("Name: " + person.name);
console.log("Age: " + str(person.age));
console.log("City: " + person.city);

// Modifying objects
console.log("");
console.log("=== Modifying Objects ===");
book = {
    title: "ML Programming",
    author: "Jane Smith",
    pages: 200
};
console.log("Original pages: " + str(book.pages));
book.pages = 250;
console.log("Updated pages: " + str(book.pages));

// Adding properties
console.log("");
console.log("=== Adding Properties ===");
product = {
    name: "Widget",
    price: 29.99
};
console.log("Name: " + product.name);
console.log("Price: $" + str(product.price));
product.inStock = true;
console.log("In stock: " + str(product.inStock));

// Objects as function parameters
function describeProduct(prod) {
    description = prod.name + " costs $" + str(prod.price);
    return description;
}

console.log("");
console.log("=== Objects in Functions ===");
item1 = {name: "Laptop", price: 999.99};
item2 = {name: "Mouse", price: 24.99};
console.log(describeProduct(item1));
console.log(describeProduct(item2));

// Functions that return objects
function createUser(username, email) {
    return {
        name: username,
        email: email,
        active: true
    };
}

console.log("");
console.log("=== Creating Objects with Functions ===");
user1 = createUser("alice", "alice@example.com");
user2 = createUser("bob", "bob@example.com");
console.log("User 1: " + user1.name + " (" + user1.email + ")");
console.log("User 2: " + user2.name + " (" + user2.email + ")");

// Nested objects
console.log("");
console.log("=== Nested Objects ===");
employee = {
    name: "John Doe",
    position: "Developer",
    contact: {
        email: "john@company.com",
        phone: "555-0100"
    },
    address: {
        street: "123 Main St",
        city: "Boston",
        zip: "02101"
    }
};
console.log("Employee: " + employee.name);
console.log("Position: " + employee.position);
console.log("Email: " + employee.contact.email);
console.log("City: " + employee.address.city);

// Updating nested properties
employee.contact.phone = "555-0200";
employee.address.zip = "02102";
console.log("Updated phone: " + employee.contact.phone);
console.log("Updated zip: " + employee.address.zip);
