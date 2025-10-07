// ============================================
// Example: Closures and Variable Scope
// Category: language-reference/functions
// Demonstrates: Lexical scoping, closures, nonlocal keyword
// ============================================

import console;

console.log("=== Closures and Variable Scope ===\n");

// Example 1: Basic closure
console.log("Example 1: Basic closure - counter");
function makeCounter() {
    count = 0;

    function increment() {
        nonlocal count;
        count = count + 1;
        return count;
    }

    return increment;
}

counter1 = makeCounter();
console.log("Counter 1: " + str(counter1()));  // 1
console.log("Counter 1: " + str(counter1()));  // 2
console.log("Counter 1: " + str(counter1()));  // 3

counter2 = makeCounter();
console.log("Counter 2: " + str(counter2()));  // 1 (independent)
console.log("Counter 2: " + str(counter2()));  // 2

// Example 2: Closure with parameters
console.log("\nExample 2: Closure factory - adder");
function makeAdder(x) {
    return fn(y) => x + y;
}

add5 = makeAdder(5);
add10 = makeAdder(10);

console.log("add5(3) = " + str(add5(3)));      // 8
console.log("add5(7) = " + str(add5(7)));      // 12
console.log("add10(3) = " + str(add10(3)));    // 13
console.log("add10(7) = " + str(add10(7)));    // 17

// Example 3: Closure for configuration
console.log("\nExample 3: Configuration closure");
function makeMultiplier(factor) {
    return fn(value) => value * factor;
}

double = makeMultiplier(2);
triple = makeMultiplier(3);
quadruple = makeMultiplier(4);

numbers = [1, 2, 3, 4, 5];
console.log("Original: " + str(numbers));

doubled = [];
for (n in numbers) { doubled = doubled + [double(n)]; }
console.log("Doubled: " + str(doubled));

tripled = [];
for (n in numbers) { tripled = tripled + [triple(n)]; }
console.log("Tripled: " + str(tripled));

quadrupled = [];
for (n in numbers) { quadrupled = quadrupled + [quadruple(n)]; }
console.log("Quadrupled: " + str(quadrupled));

// Example 4: Variable scope demonstration
console.log("\nExample 4: Variable scope");
globalVar = "global";

function demonstrateScope() {
    localVar = "local";
    console.log("Inside function - global: " + globalVar);
    console.log("Inside function - local: " + localVar);
}

demonstrateScope();
console.log("Outside function - global: " + globalVar);
// localVar not accessible here

// Example 5: Closure with multiple variables
console.log("\nExample 5: Closure with state");
function makeAccount(initialBalance) {
    balance = initialBalance;

    function deposit(amount) {
        nonlocal balance;
        balance = balance + amount;
        return balance;
    }

    function withdraw(amount) {
        nonlocal balance;
        if (amount <= balance) {
            balance = balance - amount;
            return balance;
        } else {
            return null;
        }
    }

    getBalance = fn() => balance;

    return {
        deposit: deposit,
        withdraw: withdraw,
        getBalance: getBalance
    };
}

account = makeAccount(100);
console.log("Initial balance: $" + str(account.getBalance()));
account.deposit(50);
console.log("After deposit $50: $" + str(account.getBalance()));
account.withdraw(30);
console.log("After withdraw $30: $" + str(account.getBalance()));

// Example 6: Closure for private data
console.log("\nExample 6: Private data with closures");
function createPerson(name, age) {
    // Private variables
    personName = name;
    personAge = age;

    // Public methods
    getName = fn() => personName;
    getAge = fn() => personAge;

    function setAge(newAge) {
        nonlocal personAge;
        if (newAge > 0 && newAge < 150) {
            personAge = newAge;
            return true;
        } else {
            return false;
        }
    }

    introduce = fn() => "Hi, I'm " + personName + " and I'm " + str(personAge) + " years old.";

    return {
        getName: getName,
        getAge: getAge,
        setAge: setAge,
        introduce: introduce
    };
}

person = createPerson("Alice", 30);
console.log(person.introduce());
person.setAge(31);
console.log("After birthday: " + person.introduce());

// Example 7: Nested closures
console.log("\nExample 7: Nested closures");
function outer(x) {
    outerVar = x;

    function middle(y) {
        middleVar = y;

        inner = fn(z) => outerVar + middleVar + z;

        return inner;
    }

    return middle;
}

f = outer(10);
g = f(20);
result = g(30);
console.log("outer(10) + middle(20) + inner(30) = " + str(result));  // 60

console.log("\n=== Closures and Scope Complete ===");
