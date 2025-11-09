// ML Language Type Hints: Comprehensive Examples
// Demonstrates all type hint scenarios with optional runtime checking
// Date: November 4, 2025

// =============================================================================
// SECTION 1: REGULAR FUNCTIONS - TYPE HINTS
// =============================================================================

// 1.1 No type hints (existing behavior - fully dynamic)
function add_untyped(a, b) {
    return a + b;
}

// 1.2 Parameter type hints only
function add_params_typed(a: number, b: number) {
    return a + b;  // No return type check
}

// 1.3 Return type hint only
function add_return_typed(a, b): number {
    return a + b;  // Return value checked
}

// 1.4 Fully typed function
function add_fully_typed(a: number, b: number): number {
    return a + b;  // All checked
}

// 1.5 Mixed typing (some params typed, some not)
function process_mixed(user: string, data, config: object): array {
    // user and config checked, data is dynamic
    return [user, data, config];
}

// =============================================================================
// SECTION 2: ARROW FUNCTIONS - TYPE HINTS
// =============================================================================

// 2.1 Untyped arrow function
identity = fn(x) => x;

// 2.2 Arrow with parameter type
double = fn(x: number) => x * 2;

// 2.3 Arrow with return type
triple = fn(x): number => x * 3;

// 2.4 Arrow fully typed
quadruple = fn(x: number): number => x * 4;

// 2.5 Arrow with block body and types
complex_calc = fn(a: number, b: number): number => {
    intermediate = a * a + b * b;
    return intermediate;
};

// =============================================================================
// SECTION 3: STRUCT DEFINITIONS - FIELD TYPE HINTS
// =============================================================================

// 3.1 Fully typed struct (all fields checked at creation)
struct Point {
    x: number,
    y: number
}

// 3.2 Untyped struct (no checking - pure shape definition)
struct Config {
    host,
    port,
    options
}

// 3.3 Partially typed struct (mixed checking)
struct Person {
    name: string,      // Checked
    age: number,       // Checked
    metadata           // Dynamic - no checking
}

// 3.4 Complex struct with nested types
struct Address {
    street: string,
    city: string,
    zip_code: string
}

struct Employee {
    id: number,
    name: string,
    email: string,
    address: Address,   // Custom struct type
    metadata            // Dynamic field
}

// =============================================================================
// SECTION 4: STRUCT METHODS - ALL TYPE HINT COMBINATIONS
// =============================================================================

// 4.1 Method with typed receiver only
function (p: Point) get_x() {
    return p.x;
}

// 4.2 Method with typed receiver and return type
function (p: Point) get_y(): number {
    return p.y;
}

// 4.3 Method with typed receiver, typed params, no return type
function (p: Point) move(dx: number, dy: number) {
    p.x = p.x + dx;
    p.y = p.y + dy;
}

// 4.4 Fully typed method (receiver, params, return)
function (p: Point) distance_to(other: Point): number {
    import math;
    dx = other.x - p.x;
    dy = other.y - p.y;
    return math.sqrt(dx * dx + dy * dy);
}

// 4.5 Method with mixed typing (some params typed, some not)
function (p: Point) transform(scale: number, offset, rotation: number): Point {
    // scale and rotation checked, offset is dynamic
    import math;
    angle_rad = rotation * (math.pi() / 180.0);
    cos_a = math.cos(angle_rad);
    sin_a = math.sin(angle_rad);

    new_x = (p.x * scale) * cos_a - (p.y * scale) * sin_a;
    new_y = (p.x * scale) * sin_a + (p.y * scale) * cos_a;

    return Point{
        x: new_x + offset,
        y: new_y + offset
    };
}

// =============================================================================
// SECTION 5: STRUCT USAGE - CREATION AND METHOD CALLS
// =============================================================================

function test_struct_usage() {
    // 5.1 Create fully typed struct (runtime checks x, y are numbers)
    p1 = Point{x: 3, y: 4};

    // 5.2 Create partially typed struct
    person = Person{
        name: "Alice",     // Checked: must be string
        age: 30,           // Checked: must be number
        metadata: {        // Dynamic: accepts anything
            joined: "2025-01-01",
            role: "admin"
        }
    };

    // 5.3 Create untyped struct (no checks)
    config = Config{
        host: "localhost",
        port: 8080,
        options: {debug: true}
    };

    // 5.4 Call methods (structural type checking)
    x = p1.get_x();                    // ✅ OK
    y = p1.get_y();                    // ✅ OK (returns number)
    p1.move(10, 20);                   // ✅ OK (dx, dy are numbers)

    // 5.5 Method calls with structural matching
    p2 = Point{x: 5, y: 12};
    dist = p1.distance_to(p2);         // ✅ OK (both are Points)
}

// =============================================================================
// SECTION 6: STRUCTURAL TYPING - PLAIN OBJECTS WITH STRUCT METHODS
// =============================================================================

function test_structural_typing() {
    // 6.1 Plain object that matches Point structure
    plain_point = {x: 7, y: 24};

    // 6.2 Call Point methods on plain object (structural match)
    x_val = plain_point.get_x();                          // ✅ OK (has x field)
    y_val = plain_point.get_y();                          // ✅ OK (has y field)
    plain_point.move(5, 5);                               // ✅ OK (has x, y numbers)

    // 6.3 Mixed: struct and plain object
    real_point = Point{x: 1, y: 1};
    dist = real_point.distance_to(plain_point);           // ✅ OK (structural match)

    // 6.4 Plain object with wrong types (runtime error)
    bad_point = {x: "hello", y: "world"};
    // bad_point.get_x();  // ❌ TypeError: x must be number (if get_x checks types)
}

// =============================================================================
// SECTION 7: CONSTRUCTOR FUNCTIONS WITH TYPE CHECKING
// =============================================================================

// 7.1 Simple constructor with validation
function new_point(x: number, y: number): Point {
    return Point{x: x, y: y};
}

// 7.2 Constructor with business logic validation
function new_person(name: string, age: number): Person {
    if (age < 0) {
        throw {message: "Age cannot be negative"};
    }
    if (age > 150) {
        throw {message: "Age seems unrealistic"};
    }

    return Person{
        name: name,
        age: age,
        metadata: {created: "2025-11-04"}
    };
}

// 7.3 Constructor with computed fields
function new_employee(name: string, email: string): Employee {
    import random;

    emp_id = random.randint(10000, 99999);
    default_address = Address{
        street: "Unknown",
        city: "Unknown",
        zip_code: "00000"
    };

    return Employee{
        id: emp_id,
        name: name,
        email: email,
        address: default_address,
        metadata: {}
    };
}

// =============================================================================
// SECTION 8: COMPLEX EXAMPLE - BANKING SYSTEM
// =============================================================================

struct Account {
    account_number: string,
    balance: number,
    owner: string,
    transactions           // Array - dynamic (could be typed as 'array')
}

struct Transaction {
    timestamp: number,
    amount: number,
    type: string,          // "deposit" or "withdrawal"
    balance_after: number
}

// Constructor with full validation
function new_account(owner: string, initial: number): Account {
    if (initial < 0) {
        throw {message: "Initial balance cannot be negative"};
    }

    import random;
    account_num = "ACC" + str(random.randint(100000, 999999));

    return Account{
        account_number: account_num,
        balance: initial,
        owner: owner,
        transactions: []
    };
}

// Method: deposit with full type checking
function (acc: Account) deposit(amount: number): number {
    if (amount <= 0) {
        throw {message: "Deposit amount must be positive"};
    }

    acc.balance = acc.balance + amount;

    // Create transaction record
    import datetime;
    txn = Transaction{
        timestamp: datetime.timestamp(),
        amount: amount,
        type: "deposit",
        balance_after: acc.balance
    };

    acc.transactions = acc.transactions + [txn];
    return acc.balance;
}

// Method: withdraw with validation
function (acc: Account) withdraw(amount: number): number {
    if (amount <= 0) {
        throw {message: "Withdrawal amount must be positive"};
    }
    if (amount > acc.balance) {
        throw {message: "Insufficient funds"};
    }

    acc.balance = acc.balance - amount;

    import datetime;
    txn = Transaction{
        timestamp: datetime.timestamp(),
        amount: amount,
        type: "withdrawal",
        balance_after: acc.balance
    };

    acc.transactions = acc.transactions + [txn];
    return acc.balance;
}

// Method: get balance (simple getter)
function (acc: Account) get_balance(): number {
    return acc.balance;
}

// Method: get statement (untyped return - returns array)
function (acc: Account) get_statement() {
    return acc.transactions;
}

// Usage example
function banking_example() {
    // Create account
    account = new_account("Alice", 1000);

    // Perform operations
    account.deposit(500);    // Balance: 1500
    account.withdraw(200);   // Balance: 1300
    account.deposit(100);    // Balance: 1400

    // Get balance
    balance = account.get_balance();
    print("Current balance: " + str(balance));

    // Get transaction history
    statement = account.get_statement();
    print("Transactions: " + str(len(statement)));
}

// =============================================================================
// SECTION 9: GRADUAL TYPING - MIGRATION EXAMPLE
// =============================================================================

// 9.1 Original untyped code (Phase 0)
function calculate_distance_v0(p1, p2) {
    dx = p2.x - p1.x;
    dy = p2.y - p1.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}

// 9.2 Add struct definition but keep function untyped (Phase 1)
struct PointV1 {
    x: number,
    y: number
}

function calculate_distance_v1(p1, p2) {
    dx = p2.x - p1.x;
    dy = p2.y - p1.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}

// 9.3 Add parameter types (Phase 2)
function calculate_distance_v2(p1: PointV1, p2: PointV1) {
    dx = p2.x - p1.x;
    dy = p2.y - p1.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}

// 9.4 Add return type - fully typed (Phase 3)
function calculate_distance_v3(p1: PointV1, p2: PointV1): number {
    dx = p2.x - p1.x;
    dy = p2.y - p1.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}

// 9.5 Convert to method (Phase 4)
function (p: PointV1) distance_to_v4(other: PointV1): number {
    dx = other.x - p.x;
    dy = other.y - p.y;
    import math;
    return math.sqrt(dx * dx + dy * dy);
}

// =============================================================================
// SECTION 10: TYPE SYSTEM EDGE CASES
// =============================================================================

// 10.1 Function returning struct
function create_origin(): Point {
    return Point{x: 0, y: 0};
}

// 10.2 Function returning nothing (void - no return statement)
function log_point(p: Point) {
    print("Point(" + str(p.x) + ", " + str(p.y) + ")");
    // No return statement
}

// 10.3 Function with early returns (all must match return type)
function abs_value(x: number): number {
    if (x < 0) {
        return x * -1;  // Must return number
    }
    return x;           // Must return number
}

// 10.4 Higher-order function with type hints
function apply_twice(f, x: number): number {
    // f is untyped (function), x is typed
    return f(f(x));
}

// 10.5 Callback with type hints
function filter_array(arr: array, predicate): array {
    // arr is typed, predicate is untyped function
    result = [];
    for (item in arr) {
        if (predicate(item)) {
            result = result + [item];
        }
    }
    return result;
}

// =============================================================================
// SECTION 11: RUNTIME TYPE ERROR EXAMPLES
// =============================================================================

function test_type_errors() {
    // These would cause runtime TypeErrors when types are checked:

    // 11.1 Wrong parameter type
    // add_fully_typed("hello", "world");  // ❌ TypeError: expected number

    // 11.2 Wrong struct field type
    // bad_point = Point{x: "not a number", y: 4};  // ❌ TypeError

    // 11.3 Wrong return type
    // function bad_return(): number {
    //     return "not a number";  // ❌ TypeError: must return number
    // }

    // 11.4 Missing struct fields
    // incomplete = Point{x: 3};  // ❌ Error: missing required field 'y'

    // 11.5 Structural type mismatch
    // not_a_point = {z: 5, w: 10};
    // not_a_point.get_x();  // ❌ TypeError: missing required field 'x'
}

// =============================================================================
// SECTION 12: PERFORMANCE - MIXED TYPED/UNTYPED CODE
// =============================================================================

// 12.1 Hot path - untyped for performance (no checking overhead)
function fast_loop(n) {
    sum = 0;
    i = 0;
    while (i < n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}

// 12.2 Public API - typed for safety
function safe_calculate(x: number, y: number): number {
    // Type checking at API boundary
    if (x == 0 || y == 0) {
        return 0;
    }

    // Call untyped hot path
    return fast_loop(x * y);
}

// =============================================================================
// SECTION 13: SUMMARY OF TYPE HINT BEHAVIOR
// =============================================================================

// Type hints are OPTIONAL everywhere:
// ✅ Function parameters: optional
// ✅ Function return types: optional
// ✅ Struct fields: optional
// ✅ Method receivers: optional (but recommended)

// Type checking is RUNTIME only:
// ✅ No compile-time type checking
// ✅ Types checked when provided at runtime
// ✅ No checking when types omitted
// ✅ Structural matching for struct types

// Benefits:
// ✅ Gradual typing: add types incrementally
// ✅ Backward compatible: untyped code still works
// ✅ Safety where needed: catch errors early
// ✅ Performance: no overhead for untyped code
// ✅ Documentation: types clarify intent
// ✅ IDE support: autocomplete and hints

// Main execution
function main() {
    print("=== ML Language Type Hints Examples ===");

    // Test all sections
    test_struct_usage();
    test_structural_typing();
    banking_example();

    print("All type hint scenarios demonstrated!");
}

main();
