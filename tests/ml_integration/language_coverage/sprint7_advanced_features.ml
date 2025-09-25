// Sprint 7: Advanced ML Language Features Demonstration
// Showcases pattern matching, enhanced types, and advanced constructs

// Enhanced Type Definitions
type Person = {
    name: string;
    age: number;
    email: string?;  // Optional type
};

type Result<T, E> = T | E;
type Option<T> = T | void;

// Generic Function with Type Parameters
function<T> identity(value: T): T {
    return value;
}

// Pattern Matching Example
function processValue(input: number | string): string {
    match input {
        n: number when n > 100 => "Large number: " + n;
        n: number when n > 0 => "Small number: " + n;
        s: string => "Text: " + s;
        _ => "Unknown type";
    }
}

// Advanced Function Constructs
person_data = {
    name: "Alice",
    age: 30,
    email: "alice@example.com"
};

// Pipeline Operator Example
result = person_data
    |> validatePerson
    |> formatPersonInfo
    |> print;

// Function Composition
validation_chain = validateEmail << validateAge << validateName;

// Array and Object Comprehensions
numbers = [1, 2, 3, 4, 5];
squares = [x * x for x in numbers if x > 2];

person_names = {
    p.name: p.age for p in people if p.age >= 18
};

// Pattern Matching with Destructuring
function handleResponse(response: Result<Person, string>): string {
    match response {
        {name, age}: Person => "Person: " + name + " (" + age + ")";
        error: string => "Error: " + error;
        _ => "Unknown response";
    }
}

// Advanced Array Patterns
function processArray(data: number[]): string {
    match data {
        [] => "Empty array";
        [x] => "Single element: " + x;
        [first, ...rest] => "First: " + first + ", Rest: " + rest;
        _ => "Complex array";
    }
}

// Tuple and Set Literals
coordinates = (10, 20, 30);
unique_numbers = #{1, 2, 3, 4, 5};
lookup_table = #{
    "key1": "value1",
    "key2": "value2"
};

// Enhanced Error Handling
function divide(a: number, b: number): Result<number, string> {
    if (b == 0) {
        return "Division by zero error";
    } else {
        return a / b;
    }
}

// Error Propagation
function complexCalculation(x: number, y: number): Result<number, string> {
    intermediate1 = divide(x, 2)?;
    intermediate2 = divide(y, 3)?;
    return intermediate1 + intermediate2;
}

// Interface Definition
interface Drawable {
    draw(): void;
    getArea(): number;
}

// Type with Interface Implementation
type Circle = {
    radius: number;
    center: (number, number);
    draw: () => void;
    getArea: () => number;
};

// Capability-Based Function
capability (graphics, math) function drawCircle(circle: Circle) {
    circle.draw();
    area = circle.getArea();
    print("Circle area: " + area);
}

// Async Function Example
async function fetchUserData(userId: number): Promise<Person> {
    response = await httpGet("/users/" + userId);
    return parsePersonData(response);
}

// Module Exports
export function processData(input: any[]): Result<any[], string>;
export type DataProcessor<T> = (T) => Result<T, string>;

// Demonstration Usage
main_demo = function() {
    // Test pattern matching
    print(processValue(150));
    print(processValue("hello"));

    // Test comprehensions
    print("Squares:", squares);

    // Test error handling
    safe_result = complexCalculation(10, 6);
    match safe_result {
        value: number => print("Result:", value);
        error: string => print("Error:", error);
    }

    // Test advanced data structures
    print("Coordinates:", coordinates);
    print("Unique numbers:", unique_numbers);
};

main_demo();