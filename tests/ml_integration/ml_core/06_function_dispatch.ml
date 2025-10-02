// Test core language: Function dispatch pattern
// Features tested: function variables, dictionaries as dispatch tables, closures
// NO external function calls - pure language features only

// Math operations
function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b == 0) {
        return 0;  // Avoid division by zero
    }
    return a / b;
}

function power(a, b) {
    result = 1;
    i = 0;
    while (i < b) {
        result = result * a;
        i = i + 1;
    }
    return result;
}

// Function dispatch table using if/elif
function dispatch_operation(op, a, b) {
    if (op == "add") {
        return add(a, b);
    } elif (op == "subtract") {
        return subtract(a, b);
    } elif (op == "multiply") {
        return multiply(a, b);
    } elif (op == "divide") {
        return divide(a, b);
    } elif (op == "power") {
        return power(a, b);
    } else {
        return 0;
    }
}

// Create a calculator using function variables
function create_calculator() {
    function calc_add(x, y) {
        return x + y;
    }

    function calc_sub(x, y) {
        return x - y;
    }

    function calc_mul(x, y) {
        return x * y;
    }

    return {
        add: calc_add,
        sub: calc_sub,
        mul: calc_mul
    };
}

// Strategy pattern - different sorting strategies
function strategy_bubble(arr, len) {
    // Bubble sort
    i = 0;
    while (i < len) {
        j = 0;
        while (j < len - i - 1) {
            if (arr[j] > arr[j + 1]) {
                temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
            j = j + 1;
        }
        i = i + 1;
    }
    return arr;
}

function strategy_insertion(arr, len) {
    // Insertion sort
    i = 1;
    while (i < len) {
        key = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
        i = i + 1;
    }
    return arr;
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

// Execute strategy based on choice
function execute_strategy(strategy_name, arr) {
    len = get_length(arr);

    // Copy array
    result = [];
    i = 0;
    while (i < len) {
        result = result + [arr[i]];
        i = i + 1;
    }

    if (strategy_name == "bubble") {
        return strategy_bubble(result, len);
    } elif (strategy_name == "insertion") {
        return strategy_insertion(result, len);
    } else {
        return result;
    }
}

// Command pattern
function create_command(action, value) {
    return {
        action: action,
        value: value
    };
}

function execute_command(state, command) {
    if (command.action == "increment") {
        state.counter = state.counter + command.value;
    } elif (command.action == "decrement") {
        state.counter = state.counter - command.value;
    } elif (command.action == "multiply") {
        state.counter = state.counter * command.value;
    } elif (command.action == "reset") {
        state.counter = 0;
    }
    return state;
}

// Function composition
function compose(f, g) {
    function composed(x) {
        return f(g(x));
    }
    return composed;
}

function double(x) {
    return x * 2;
}

function add_ten(x) {
    return x + 10;
}

function square(x) {
    return x * x;
}

// Pipeline pattern
function pipeline(value, functions) {
    len = get_length(functions);
    result = value;
    i = 0;
    while (i < len) {
        func = functions[i];
        result = func(result);
        i = i + 1;
    }
    return result;
}

// Main test function
function main() {
    results = {};

    // Test 1: Basic dispatch
    results.add_5_3 = dispatch_operation("add", 5, 3);
    results.mul_4_7 = dispatch_operation("multiply", 4, 7);
    results.pow_2_5 = dispatch_operation("power", 2, 5);

    // Test 2: Calculator object
    calc = create_calculator();
    results.calc_add = calc.add(10, 5);
    results.calc_sub = calc.sub(10, 5);
    results.calc_mul = calc.mul(10, 5);

    // Test 3: Strategy pattern
    test_arr = [5, 2, 8, 1, 9];
    results.bubble_sorted = execute_strategy("bubble", test_arr);
    results.insertion_sorted = execute_strategy("insertion", test_arr);

    // Test 4: Command pattern
    state = {counter: 0};
    commands = [
        create_command("increment", 5),
        create_command("increment", 3),
        create_command("multiply", 2),
        create_command("decrement", 4)
    ];

    i = 0;
    cmd_len = get_length(commands);
    while (i < cmd_len) {
        state = execute_command(state, commands[i]);
        i = i + 1;
    }
    results.final_counter = state.counter;

    // Test 5: Function composition
    double_then_add_ten = compose(add_ten, double);
    results.composed_5 = double_then_add_ten(5);  // (5*2)+10 = 20

    // Test 6: Pipeline
    pipeline_funcs = [double, add_ten, square];

    results.pipeline_3 = pipeline(3, pipeline_funcs);  // ((3*2)+10)^2 = 256

    // Test 7: Multiple dispatches
    operations = [
        {op: "add", a: 10, b: 5},
        {op: "multiply", a: 3, b: 4},
        {op: "power", a: 2, b: 3},
        {op: "subtract", a: 20, b: 7}
    ];

    batch_results = [];
    i = 0;
    op_len = get_length(operations);
    while (i < op_len) {
        op = operations[i];
        batch_results = batch_results + [dispatch_operation(op.op, op.a, op.b)];
        i = i + 1;
    }
    results.batch_operations = batch_results;

    return results;
}

// Run tests
test_results = main();
