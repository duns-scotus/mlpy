// Test core language: Closures and function variables
// Features tested: closures, function variables, scope, nested functions
// NO external function calls - pure language features only

// Simple closure - capture variable from outer scope
function create_counter(initial) {
    count = initial;

    function increment() {
        count = count + 1;
        return count;
    }

    return increment;
}

// Closure with multiple functions
function create_account(initial_balance) {
    balance = initial_balance;

    function deposit(amount) {
        balance = balance + amount;
        return balance;
    }

    function withdraw(amount) {
        if (balance >= amount) {
            balance = balance - amount;
            return balance;
        } else {
            return balance;  // Insufficient funds
        }
    }

    function get_balance() {
        return balance;
    }

    return {
        deposit: deposit,
        withdraw: withdraw,
        balance: get_balance
    };
}

// Function factory - creates functions with different behaviors
function create_multiplier(factor) {
    function multiply(value) {
        return value * factor;
    }
    return multiply;
}

function create_adder(amount) {
    function add(value) {
        return value + amount;
    }
    return add;
}

// Currying simulation
function curry_add(a) {
    function add_to_a(b) {
        return a + b;
    }
    return add_to_a;
}

function curry_multiply(a) {
    function multiply_by_a(b) {
        return a * b;
    }
    return multiply_by_a;
}

// Partial application
function partial_power(base) {
    function raise_to(exponent) {
        result = 1;
        i = 0;
        while (i < exponent) {
            result = result * base;
            i = i + 1;
        }
        return result;
    }
    return raise_to;
}

// Function that returns different functions based on condition
function get_operation(op_type) {
    function add_op(a, b) {
        return a + b;
    }

    function mul_op(a, b) {
        return a * b;
    }

    function sub_op(a, b) {
        return a - b;
    }

    if (op_type == "add") {
        return add_op;
    } elif (op_type == "mul") {
        return mul_op;
    } else {
        return sub_op;
    }
}

// Closure with state preservation
function create_sequence() {
    current = 0;

    function next() {
        current = current + 1;
        return current;
    }

    function reset() {
        current = 0;
        return current;
    }

    function get_current() {
        return current;
    }

    return {
        next: next,
        reset: reset,
        current: get_current
    };
}

// Private variables using closures
function create_person(name, age) {
    person_name = name;
    person_age = age;

    function get_name() {
        return person_name;
    }

    function get_age() {
        return person_age;
    }

    function have_birthday() {
        person_age = person_age + 1;
        return person_age;
    }

    return {
        name: get_name,
        age: get_age,
        birthday: have_birthday
    };
}

// Helper: get array length
function get_length(arr) {
    len = 0;
    try {
        i = 0;
        while (true) {
            temp = arr[i];
            i = i + 1;
            len = len + 1;
        }
    } except (e) {
        // Out of bounds
    }
    return len;
}

// Higher-order function that takes function as parameter
function apply_to_array(arr, func) {
    len = get_length(arr);
    result = [];
    i = 0;
    while (i < len) {
        result[i] = func(arr[i]);
        i = i + 1;
    }
    return result;
}

// Main test function
function main() {
    results = {};

    // Test 1: Simple counter
    counter = create_counter(10);
    results.count1 = counter();  // 11
    results.count2 = counter();  // 12
    results.count3 = counter();  // 13

    // Test 2: Account with multiple operations
    account = create_account(100);
    results.initial = account.balance();      // 100
    results.after_deposit = account.deposit(50);  // 150
    results.after_withdraw = account.withdraw(30);  // 120
    results.final_balance = account.balance();  // 120

    // Test 3: Function factories
    double = create_multiplier(2);
    triple = create_multiplier(3);
    add_five = create_adder(5);

    results.double_10 = double(10);  // 20
    results.triple_10 = triple(10);  // 30
    results.add_five_10 = add_five(10);  // 15

    // Test 4: Currying
    add_5 = curry_add(5);
    mul_3 = curry_multiply(3);

    results.curried_add = add_5(10);  // 15
    results.curried_mul = mul_3(7);   // 21

    // Test 5: Partial application
    power_of_2 = partial_power(2);
    power_of_3 = partial_power(3);

    results.two_pow_5 = power_of_2(5);  // 32
    results.three_pow_3 = power_of_3(3);  // 27

    // Test 6: Dynamic function selection
    add_func = get_operation("add");
    mul_func = get_operation("mul");

    results.dynamic_add = add_func(8, 7);  // 15
    results.dynamic_mul = mul_func(8, 7);  // 56

    // Test 7: Sequence generator
    seq = create_sequence();
    results.seq1 = seq.next();  // 1
    results.seq2 = seq.next();  // 2
    results.seq3 = seq.next();  // 3
    seq.reset();
    results.seq_after_reset = seq.next();  // 1

    // Test 8: Person with private state
    person = create_person("Alice", 25);
    results.person_name = person.name();
    results.person_age = person.age();
    results.age_after_birthday = person.birthday();  // 26
    results.person_age_final = person.age();  // 26

    // Test 9: Higher-order function with array
    test_array = [1, 2, 3, 4, 5];
    square_func = create_multiplier(1);  // Will use for identity

    function square(x) {
        return x * x;
    }

    results.squared_array = apply_to_array(test_array, square);

    // Test 10: Multiple independent closures
    counter_a = create_counter(0);
    counter_b = create_counter(100);

    results.counter_a1 = counter_a();  // 1
    results.counter_b1 = counter_b();  // 101
    results.counter_a2 = counter_a();  // 2
    results.counter_b2 = counter_b();  // 102

    return results;
}

// Run tests
test_results = main();
