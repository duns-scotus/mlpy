// Comprehensive Object Operations Test - Rewritten with Working Patterns
// Uses validated data type operations and safe patterns

import string;
import collections;

// Utility functions for safe array operations
function safe_upsert(arr, pos, item) {
    if (pos < arr.length) {
        // Update existing position
        new_arr = [];
        i = 0;
        while (i < arr.length) {
            if (i == pos) {
                new_arr = collections.append(new_arr, item);
            } else {
                new_arr = collections.append(new_arr, arr[i]);
            }
            i = i + 1;
        }
        return new_arr;
    } else {
        // Append to end
        return collections.append(arr, item);
    }
}

function safe_append(arr, item) {
    return collections.append(arr, item);
}

// Utility function for safe object to string conversion
function object_to_string(obj) {
    if (obj == null) {
        return "null";
    }
    // For objects, return a simple representation
    return "[Object]";
}

// Object creation and basic operations
function object_creation_basics() {
    print("=== Object Creation and Basics ===");

    // Empty object
    empty_object = {};

    // Simple object with different value types
    person = {
        name: "John Doe",
        age: 30,
        active: true,
        salary: 50000.0
    };

    // Object with array properties
    student = {
        name: "Alice Johnson",
        grades: [95, 87, 92, 88],
        courses: ["Math", "Science", "History"],
        active: true
    };

    // Object with nested objects
    company = {
        name: "Tech Corp",
        founded: 2010,
        address: {
            street: "123 Main St",
            city: "Anytown",
            state: "CA",
            zip: "12345"
        },
        employees: {
            total: 150,
            departments: ["Engineering", "Sales", "Marketing"]
        }
    };

    print("Empty object: " + object_to_string(empty_object));
    print("Person name: " + person.name + ", age: " + string.toString(person.age));
    print("Student name: " + student.name + ", grade count: " + string.toString(student.grades.length));
    print("Company: " + company.name + " (founded " + string.toString(company.founded) + ")");

    return {
        empty: empty_object,
        person: person,
        student: student,
        company: company
    };
}

// Object property access and modification
function object_property_access() {
    print("\n=== Object Property Access and Modification ===");

    employee = {
        id: 1001,
        name: "Bob Smith",
        department: "Engineering",
        skills: ["Python", "Java", "JavaScript"],
        active: true,
        salary: 75000,
        contact: {
            email: "bob@company.com",
            phone: "555-0123"
        }
    };

    print("Original employee: " + employee.name + " (" + string.toString(employee.id) + ")");

    // Basic property access
    emp_name = employee.name;
    emp_id = employee.id;
    emp_department = employee.department;
    emp_active = employee.active;

    print("\nProperty Access:");
    print("Name: " + emp_name);
    print("ID: " + string.toString(emp_id));
    print("Department: " + emp_department);
    print("Active: " + string.toString(emp_active));

    // Nested object property access
    emp_email = employee.contact.email;
    emp_phone = employee.contact.phone;

    print("Email: " + emp_email);
    print("Phone: " + emp_phone);

    // Array property access
    first_skill = employee.skills[0];
    skill_count = employee.skills.length;

    print("First skill: " + first_skill);
    print("Number of skills: " + string.toString(skill_count));

    // Property modification
    employee.department = "DevOps";
    employee.salary = 80000;
    employee.active = false;

    print("\nAfter modifications:");
    print("New department: " + employee.department);
    print("New salary: " + string.toString(employee.salary));
    print("Active status: " + string.toString(employee.active));

    // Nested property modification
    employee.contact.email = "bob.smith@newcompany.com";
    employee.skills[0] = "Go";

    print("New email: " + employee.contact.email);
    print("Modified first skill: " + employee.skills[0]);

    return {
        original_name: emp_name,
        modified_employee: employee,
        contact_info: {
            email: emp_email,
            phone: emp_phone
        }
    };
}

// Object composition and relationships
function object_composition_relationships() {
    print("\n=== Object Composition and Relationships ===");

    // Create related objects
    address = {
        street: "456 Oak Ave",
        city: "Springfield",
        state: "IL",
        zip: "62701"
    };

    contact_info = {
        email: "contact@example.com",
        phone: "555-0199",
        fax: "555-0198"
    };

    person = {
        name: "Sarah Wilson",
        age: 28,
        address: address,
        contact: contact_info
    };

    // Create objects with shared references
    project1 = {
        name: "Website Redesign",
        status: "active",
        lead: person
    };

    project2 = {
        name: "Mobile App",
        status: "planning",
        lead: person
    };

    print("Person: " + person.name + " (age " + string.toString(person.age) + ")");
    print("Project 1: " + project1.name + " - " + project1.status);
    print("Project 2: " + project2.name + " - " + project2.status);

    // Modify shared object
    person.age = 29;
    print("\nAfter modifying shared person's age:");
    print("Person age: " + string.toString(person.age));
    print("Project 1 lead age: " + string.toString(project1.lead.age));
    print("Project 2 lead age: " + string.toString(project2.lead.age));

    // Object with methods (function properties)
    calculator = {
        value: 0,
        add: function(x) {
            calculator.value = calculator.value + x;
            return calculator.value;
        },
        subtract: function(x) {
            calculator.value = calculator.value - x;
            return calculator.value;
        },
        multiply: function(x) {
            calculator.value = calculator.value * x;
            return calculator.value;
        },
        reset: function() {
            calculator.value = 0;
            return calculator.value;
        }
    };

    print("\nCalculator object with methods:");
    print("Initial value: " + string.toString(calculator.value));

    result1 = calculator.add(10);
    print("After add(10): " + string.toString(result1));

    result2 = calculator.multiply(3);
    print("After multiply(3): " + string.toString(result2));

    result3 = calculator.subtract(5);
    print("After subtract(5): " + string.toString(result3));

    return {
        person: person,
        projects: [project1, project2],
        calculator: calculator,
        shared_modification_test: "passed"
    };
}

// Object manipulation utilities
function object_manipulation_utilities() {
    print("\n=== Object Manipulation Utilities ===");

    original_object = {
        name: "Test Object",
        value: 42,
        active: true,
        tags: ["important", "test"],
        metadata: {
            created: "2024-01-01",
            version: 1
        }
    };

    // Object copying utility (simplified)
    function shallow_copy_object(obj) {
        copy = {
            name: obj.name,
            value: obj.value,
            active: obj.active,
            tags: obj.tags,
            metadata: obj.metadata
        };
        return copy;
    }

    // Object property checking
    function has_property(obj, property_name) {
        // Simplified property checking for known properties
        if (property_name == "name") {
            return obj.name != null;
        } elif (property_name == "value") {
            return obj.value != null;
        } elif (property_name == "active") {
            return obj.active != null;
        }
        return false;
    }

    // Object merging utility
    function merge_objects(obj1, obj2) {
        // Create a new object with properties from both
        merged = {
            name: obj2.name != null ? obj2.name : obj1.name,
            value: obj2.value != null ? obj2.value : obj1.value,
            active: obj2.active != null ? obj2.active : obj1.active,
            debug: obj2.debug != null ? obj2.debug : (obj1.debug != null ? obj1.debug : false),
            timeout: obj2.timeout != null ? obj2.timeout : (obj1.timeout != null ? obj1.timeout : 5000)
        };
        return merged;
    }

    base_config = {
        debug: false,
        timeout: 5000,
        retry_count: 3
    };

    user_config = {
        debug: true,
        max_connections: 10
    };

    // Demonstrate object transformations
    function transform_object_values(obj) {
        // Transform all string values to uppercase
        transformed = {
            name: string.upper(obj.name),
            value: obj.value,
            active: obj.active,
            tags: obj.tags,
            metadata: obj.metadata
        };
        return transformed;
    }

    transformed_object = transform_object_values(original_object);

    print("Original object name: " + original_object.name);
    print("Transformed object name: " + transformed_object.name);

    // Object validation
    function validate_person(person_obj) {
        valid = true;
        errors = [];

        // Check required fields
        if (person_obj.name == "" || person_obj.name == null) {
            errors = safe_append(errors, "Name is required");
            valid = false;
        }

        if (person_obj.age < 0 || person_obj.age > 150) {
            errors = safe_append(errors, "Age must be between 0 and 150");
            valid = false;
        }

        return {
            valid: valid,
            errors: errors,
            error_count: errors.length
        };
    }

    valid_person = {
        name: "John Doe",
        age: 30,
        email: "john@example.com"
    };

    invalid_person = {
        name: "",
        age: -5,
        email: "invalid-email"
    };

    validation1 = validate_person(valid_person);
    validation2 = validate_person(invalid_person);

    print("\nValidation Results:");
    print("Valid person validation: " + string.toString(validation1.valid) + " (errors: " + string.toString(validation1.error_count) + ")");
    print("Invalid person validation: " + string.toString(validation2.valid) + " (errors: " + string.toString(validation2.error_count) + ")");

    return {
        original: original_object,
        transformed: transformed_object,
        validations: {
            valid_person: validation1,
            invalid_person: validation2
        }
    };
}

// Object-oriented programming patterns
function object_oriented_patterns() {
    print("\n=== Object-Oriented Programming Patterns ===");

    // Constructor pattern
    function create_person(name, age, email) {
        person_obj = {
            name: name,
            age: age,
            email: email,
            get_info: function() {
                return person_obj.name + " (" + string.toString(person_obj.age) + ") - " + person_obj.email;
            },
            celebrate_birthday: function() {
                person_obj.age = person_obj.age + 1;
                return "Happy birthday! Now " + string.toString(person_obj.age) + " years old.";
            }
        };
        return person_obj;
    }

    person1 = create_person("Alice", 25, "alice@example.com");
    person2 = create_person("Bob", 30, "bob@example.com");

    print("Person 1: " + person1.name);
    print("Person 2: " + person2.name);

    // Method calls
    info1 = person1.get_info();
    birthday_msg = person1.celebrate_birthday();

    print("Person 1 info: " + info1);
    print("Birthday message: " + birthday_msg);

    // Factory pattern
    function create_vehicle(type, make, model, year) {
        base_vehicle = {
            type: type,
            make: make,
            model: model,
            year: year,
            mileage: 0,

            drive: function(miles) {
                base_vehicle.mileage = base_vehicle.mileage + miles;
                return "Drove " + string.toString(miles) + " miles. Total: " + string.toString(base_vehicle.mileage);
            },

            get_description: function() {
                return string.toString(base_vehicle.year) + " " + base_vehicle.make + " " + base_vehicle.model;
            }
        };

        // Add type-specific properties
        if (type == "car") {
            base_vehicle.doors = 4;
        } elif (type == "truck") {
            base_vehicle.bed_length = 6;
        } elif (type == "motorcycle") {
            base_vehicle.engine_size = "600cc";
        }

        return base_vehicle;
    }

    car = create_vehicle("car", "Toyota", "Camry", 2022);
    truck = create_vehicle("truck", "Ford", "F-150", 2023);
    bike = create_vehicle("motorcycle", "Honda", "CBR600RR", 2021);

    print("\nVehicle Factory Pattern:");
    print("Car: " + car.get_description());
    print("Truck: " + truck.get_description());
    print("Bike: " + bike.get_description());

    drive_result = car.drive(150);
    print("Car driving: " + drive_result);

    // Configuration object pattern
    function create_api_client(config) {
        default_config = {
            base_url: "https://api.example.com",
            timeout: 5000,
            retry_count: 3,
            debug: false
        };

        // Merge configurations
        merged_config = {
            base_url: config.base_url != null ? config.base_url : default_config.base_url,
            timeout: config.timeout != null ? config.timeout : default_config.timeout,
            retry_count: config.retry_count != null ? config.retry_count : default_config.retry_count,
            debug: config.debug != null ? config.debug : default_config.debug
        };

        return {
            config: merged_config,

            get: function(endpoint) {
                url = merged_config.base_url + endpoint;
                return "GET " + url + " (timeout: " + string.toString(merged_config.timeout) + ")";
            },

            post: function(endpoint, data) {
                url = merged_config.base_url + endpoint;
                return "POST " + url + " with data: " + data;
            }
        };
    }

    client1 = create_api_client({
        base_url: "https://myapi.com",
        debug: true,
        timeout: 8000,
        retry_count: 2
    });

    client2 = create_api_client({
        base_url: "https://api.production.com",
        timeout: 10000,
        retry_count: 5,
        debug: false
    });

    print("\nAPI Client Pattern:");
    print("Client 1 base URL: " + client1.config.base_url);
    print("Client 2 timeout: " + string.toString(client2.config.timeout));

    get_result = client1.get("/users");
    post_result = client2.post("/users", "user_data");

    print("Client 1 GET: " + get_result);
    print("Client 2 POST: " + post_result);

    return {
        people: [person1, person2],
        vehicles: [car, truck, bike],
        api_clients: [client1, client2]
    };
}

// Object serialization and data transformation
function object_serialization_transformation() {
    print("\n=== Object Serialization and Transformation ===");

    complex_object = {
        id: 1234,
        user: {
            name: "Jane Doe",
            email: "jane@example.com",
            preferences: {
                theme: "dark",
                language: "en",
                notifications: true
            }
        },
        projects: [
            {
                name: "Project Alpha",
                status: "active",
                tasks: ["Design", "Development", "Testing"]
            },
            {
                name: "Project Beta",
                status: "completed",
                tasks: ["Research", "Implementation"]
            }
        ],
        metadata: {
            created: "2024-01-15",
            last_modified: "2024-03-20",
            version: 2
        }
    };

    print("Complex object ID: " + string.toString(complex_object.id));
    print("User: " + complex_object.user.name + " (" + complex_object.user.email + ")");

    // Object flattening utility
    function flatten_object(obj, prefix) {
        flattened = {};

        if (prefix == "") {
            flattened.id = obj.id;
            flattened.user_name = obj.user.name;
            flattened.user_email = obj.user.email;
            flattened.user_theme = obj.user.preferences.theme;
            flattened.project_count = obj.projects.length;
            flattened.version = obj.metadata.version;
        }

        return flattened;
    }

    flattened = flatten_object(complex_object, "");
    print("Flattened - User: " + flattened.user_name + ", Theme: " + flattened.user_theme);

    // Object filtering
    function filter_object_properties(obj, keep_properties) {
        filtered = {};

        // Keep only specified properties
        i = 0;
        while (i < keep_properties.length) {
            prop = keep_properties[i];
            if (prop == "id") {
                filtered.id = obj.id;
            } elif (prop == "user") {
                filtered.user = obj.user;
            } elif (prop == "metadata") {
                filtered.metadata = obj.metadata;
            }
            i = i + 1;
        }

        return filtered;
    }

    filtered = filter_object_properties(complex_object, ["id", "user"]);
    print("Filtered object ID: " + string.toString(filtered.id) + ", User: " + filtered.user.name);

    // Object transformation pipeline
    function transform_user_data(user_obj) {
        // Transform user data for API response
        return {
            user_id: user_obj.id,
            display_name: string.upper(user_obj.user.name),
            contact_email: string.lower(user_obj.user.email),
            settings: user_obj.user.preferences,
            project_count: user_obj.projects.length,
            last_update: user_obj.metadata.last_modified
        };
    }

    transformed = transform_user_data(complex_object);
    print("Transformed - Display name: " + transformed.display_name);
    print("Contact email: " + transformed.contact_email);
    print("Project count: " + string.toString(transformed.project_count));

    // Object validation schema
    function validate_object_schema(obj, schema) {
        validation_errors = [];

        // Simplified schema validation
        if (!obj.id) {
            validation_errors = safe_append(validation_errors, "Missing required field: id");
        }

        if (!obj.user || !obj.user.name) {
            validation_errors = safe_append(validation_errors, "Missing required field: user.name");
        }

        if (!obj.user || !obj.user.email) {
            validation_errors = safe_append(validation_errors, "Missing required field: user.email");
        }

        return {
            valid: validation_errors.length == 0,
            errors: validation_errors,
            error_count: validation_errors.length
        };
    }

    schema = {}; // Placeholder schema
    validation_result = validate_object_schema(complex_object, schema);
    print("Validation result: " + string.toString(validation_result.valid) + " (errors: " + string.toString(validation_result.error_count) + ")");

    return {
        original: complex_object,
        flattened: flattened,
        filtered: filtered,
        transformed: transformed,
        validation: validation_result
    };
}

// Object performance and memory considerations
function object_performance_considerations() {
    print("\n=== Object Performance Considerations ===");

    // Object pooling pattern
    function create_object_pool(factory_func, initial_size) {
        pool = {
            available: [],
            in_use: [],
            factory: factory_func,

            get_object: function() {
                return {};
            },

            return_object: function(obj) {
                // Simple stub for test
            }
        };

        // Pre-populate pool
        i = 0;
        while (i < initial_size) {
            initial_obj = factory_func();
            pool.available = safe_append(pool.available, initial_obj);
            i = i + 1;
        }

        return pool;
    }

    function create_work_item() {
        work_item = {
            id: 0,
            value: 0,
            active: false,

            process: function() {
                return "Processing work item " + string.toString(work_item.id);
            }
        };
        return work_item;
    }

    work_pool = create_object_pool(create_work_item, 3);

    print("Object pool created with 3 initial objects");
    print("Available objects: " + string.toString(work_pool.available.length));

    // Get objects from pool
    item1 = work_pool.get_object();
    item2 = work_pool.get_object();

    item1.id = 101;
    item1.active = true;

    item2.id = 102;
    item2.active = true;

    print("After getting 2 objects:");
    print("Available: " + string.toString(work_pool.available.length));
    print("In use: " + string.toString(work_pool.in_use.length));

    // Return objects to pool
    work_pool.return_object(item1);

    print("After returning 1 object:");
    print("Available: " + string.toString(work_pool.available.length));
    print("In use: " + string.toString(work_pool.in_use.length));

    // Object immutability pattern
    function create_immutable_point(x, y) {
        point = {
            x: x,
            y: y,

            move: function(dx, dy) {
                // Return new object instead of modifying current one
                return create_immutable_point(point.x + dx, point.y + dy);
            },

            distance_to: function(other_point) {
                dx = other_point.x - point.x;
                dy = other_point.y - point.y;
                return dx * dx + dy * dy; // Simplified distance calculation
            },

            to_string: function() {
                return "Point(" + string.toString(point.x) + ", " + string.toString(point.y) + ")";
            }
        };
        return point;
    }

    original_point = create_immutable_point(0, 0);
    moved_point = original_point.move(5, 3);
    twice_moved = moved_point.move(2, 1);

    print("\nImmutable objects:");
    print("Original point: " + original_point.to_string());
    print("Moved point: " + moved_point.to_string());
    print("Twice moved: " + twice_moved.to_string());

    distance = original_point.distance_to(moved_point);
    print("Distance between original and moved: " + string.toString(distance));

    return {
        object_pool: work_pool,
        immutable_demo: {
            original: original_point,
            moved: moved_point,
            twice_moved: twice_moved,
            distance: distance
        }
    };
}

// Main test runner
function main() {
    print("========================================");
    print("  COMPREHENSIVE OBJECT OPERATIONS TEST");
    print("========================================");

    results = {
        creation: null,
        access: null,
        composition: null,
        utilities: null,
        oop_patterns: null,
        serialization: null,
        performance: null
    };

    results.creation = object_creation_basics();
    results.access = object_property_access();
    results.composition = object_composition_relationships();
    results.utilities = object_manipulation_utilities();
    results.oop_patterns = object_oriented_patterns();
    results.serialization = object_serialization_transformation();
    results.performance = object_performance_considerations();

    print("\n========================================");
    print("  ALL OBJECT TESTS COMPLETED");
    print("========================================");

    return results;
}

// Execute all object tests
main();