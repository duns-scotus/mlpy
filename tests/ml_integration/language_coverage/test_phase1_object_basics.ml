// Phase 1 Test: Simple Object Basics
import collections;
import string;

function test_basic_object_creation() {
    print("=== Basic Object Creation ===");

    // Simple object creation
    person = {name: "John", age: 30, active: true};

    // Property access
    name = person.name;
    age = person.age;

    print("Person: " + name + ", age: " + string.toString(age));

    // Property modification
    person.age = 31;
    person.city = "New York";

    print("Updated age: " + string.toString(person.age));

    return person;
}

function test_object_composition() {
    print("=== Object Composition ===");

    address = {street: "123 Main St", city: "Boston", zip: "02101"};
    contact = {email: "john@example.com", phone: "555-0123"};

    employee = {
        id: 1001,
        name: "John Doe",
        address: address,
        contact: contact,
        active: true
    };

    print("Employee: " + employee.name);
    print("City: " + employee.address.city);
    print("Email: " + employee.contact.email);

    return employee;
}

function create_user(name, email, role) {
    user = {
        name: name,
        email: email,
        role: role,
        created_at: 1640995200,
        active: true
    };
    return user;
}

function test_object_factory() {
    print("=== Object Factory Pattern ===");

    admin = create_user("Alice", "alice@admin.com", "admin");
    user = create_user("Bob", "bob@user.com", "user");

    print("Admin: " + admin.name + " (" + admin.role + ")");
    print("User: " + user.name + " (" + user.role + ")");

    return [admin, user];
}

// Run tests
test_basic_object_creation();
test_object_composition();
test_object_factory();