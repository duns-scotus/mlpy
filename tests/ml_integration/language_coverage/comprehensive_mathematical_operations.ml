// Comprehensive Mathematical Operations Test
// Demonstrates all mathematical operations, functions, and algorithms in ML

import string;
import datetime;

// Basic arithmetic operations and precedence
function basic_arithmetic_operations() {
    print("=== Basic Arithmetic Operations and Precedence ===");

    // Basic operations
    a = 15;
    b = 4;
    c = 2;

    addition = a + b;
    subtraction = a - b;
    multiplication = a * b;
    division = a / b;
    modulo = a % b;

    print("Basic arithmetic with a=" + a + ", b=" + b + ":");
    print("Addition: " + a + " + " + b + " = " + addition);
    print("Subtraction: " + a + " - " + b + " = " + subtraction);
    print("Multiplication: " + a + " * " + b + " = " + multiplication);
    print("Division: " + a + " / " + b + " = " + division);
    print("Modulo: " + a + " % " + b + " = " + modulo);

    // Operator precedence
    expr1 = a + b * c;           // 15 + (4 * 2) = 23
    expr2 = (a + b) * c;         // (15 + 4) * 2 = 38
    expr3 = a / b + c;           // (15 / 4) + 2 = 5.75
    expr4 = a / (b + c);         // 15 / (4 + 2) = 2.5
    expr5 = a + b - c * 2;       // 15 + 4 - (2 * 2) = 15
    expr6 = a * b % c + 1;       // ((15 * 4) % 2) + 1 = 1

    print("\nOperator precedence examples:");
    print("15 + 4 * 2 = " + expr1);
    print("(15 + 4) * 2 = " + expr2);
    print("15 / 4 + 2 = " + expr3);
    print("15 / (4 + 2) = " + expr4);
    print("15 + 4 - 2 * 2 = " + expr5);
    print("15 * 4 % 2 + 1 = " + expr6);

    // Unary operations
    positive = a;  // ML doesn't support unary plus operator
    negative = -a;
    double_negative = -(-a);

    print("\nUnary operations:");
    print("Positive: +" + a + " = " + positive);
    print("Negative: -" + a + " = " + negative);
    print("Double negative: -(-" + a + ") = " + double_negative);

    return {
        basic: {addition: addition, subtraction: subtraction, multiplication: multiplication, division: division, modulo: modulo},
        precedence: [expr1, expr2, expr3, expr4, expr5, expr6],
        unary: {positive: positive, negative: negative, double_negative: double_negative}
    };
}

// Advanced mathematical functions
function advanced_mathematical_functions() {
    print("\n=== Advanced Mathematical Functions ===");

    // Power and root operations
    function power(base, exponent) {
        if (exponent == 0) {
            return 1;
        }
        if (exponent == 1) {
            return base;
        }

        result = 1;
        i = 0;
        while (i < exponent) {
            result = result * base;
            i = i + 1;
        }
        return result;
    }

    function square_root(n) {
        if (n < 0) {
            return 0; // Invalid for negative numbers
        }
        if (n == 0 || n == 1) {
            return n;
        }

        // Newton's method approximation
        x = n;
        precision = 0.000001;
        iterations = 0;
        max_iterations = 100;

        while (iterations < max_iterations) {
            root = 0.5 * (x + (n / x));
            if (abs(root - x) < precision) {
                break;
            }
            x = root;
            iterations = iterations + 1;
        }

        return x;
    }

    function abs(x) {
        return x < 0 ? -x : x;
    }

    function max(a, b) {
        return a > b ? a : b;
    }

    function min(a, b) {
        return a < b ? a : b;
    }

    // Test power operations
    pow_results = [];
    pow_results[0] = power(2, 3);   // 8
    pow_results[1] = power(5, 2);   // 25
    pow_results[2] = power(3, 4);   // 81
    pow_results[3] = power(10, 0);  // 1
    pow_results[4] = power(7, 1);   // 7

    print("Power operations:");
    print("2^3 = " + pow_results[0]);
    print("5^2 = " + pow_results[1]);
    print("3^4 = " + pow_results[2]);
    print("10^0 = " + pow_results[3]);
    print("7^1 = " + pow_results[4]);

    // Test square root operations
    sqrt_results = [];
    sqrt_results[0] = square_root(25);    // 5
    sqrt_results[1] = square_root(16);    // 4
    sqrt_results[2] = square_root(2);     // ~1.414
    sqrt_results[3] = square_root(10);    // ~3.162
    sqrt_results[4] = square_root(0);     // 0

    print("\nSquare root operations:");
    print("sqrt(25) = " + sqrt_results[0]);
    print("sqrt(16) = " + sqrt_results[1]);
    print("sqrt(2) = " + sqrt_results[2]);
    print("sqrt(10) = " + sqrt_results[3]);
    print("sqrt(0) = " + sqrt_results[4]);

    // Test absolute value, min, max
    test_numbers = [-15, -3, 0, 7, 12];
    abs_results = [];
    i = 0;
    while (i < test_numbers.length()) {
        abs_results[i] = abs(test_numbers[i]);
        i = i + 1;
    }

    print("\nAbsolute value operations:");
    j = 0;
    while (j < test_numbers.length()) {
        print("abs(" + test_numbers[j] + ") = " + abs_results[j]);
        j = j + 1;
    }

    min_result = min(15, 23);
    max_result = max(15, 23);
    print("\nMin/Max operations:");
    print("min(15, 23) = " + min_result);
    print("max(15, 23) = " + max_result);

    return {
        power_results: pow_results,
        sqrt_results: sqrt_results,
        abs_results: abs_results,
        min_max: {min: min_result, max: max_result}
    };
}

// Trigonometric approximations
function trigonometric_approximations() {
    print("\n=== Trigonometric Function Approximations ===");

    // Mathematical constants
    PI = 3.14159265359;
    E = 2.71828182846;

    // Factorial function for series calculations
    function factorial(n) {
        if (n <= 1) {
            return 1;
        }
        result = 1;
        i = 2;
        while (i <= n) {
            result = result * i;
            i = i + 1;
        }
        return result;
    }

    // Sine approximation using Taylor series
    function sine(x) {
        // Normalize x to [-2π, 2π] range
        while (x > 2 * PI) {
            x = x - 2 * PI;
        }
        while (x < -2 * PI) {
            x = x + 2 * PI;
        }

        result = 0;
        term = x;
        i = 1;

        // Calculate first 10 terms of Taylor series
        while (i <= 19) {
            if (i % 4 == 1) {
                result = result + term;
            } else {
                result = result - term;
            }

            term = term * x * x / ((i + 1) * (i + 2));
            i = i + 2;
        }

        return result;
    }

    // Cosine approximation using Taylor series
    function cosine(x) {
        // cos(x) = sin(π/2 - x)
        return sine(PI / 2 - x);
    }

    // Tangent approximation
    function tangent(x) {
        cos_x = cosine(x);
        if (abs(cos_x) < 0.000001) {
            return 0; // Avoid division by zero
        }
        return sine(x) / cos_x;
    }

    function abs(x) {
        return x < 0 ? -x : x;
    }

    // Test trigonometric functions
    angles = [0, PI / 6, PI / 4, PI / 3, PI / 2, PI];
    angle_names = ["0", "π/6 (30°)", "π/4 (45°)", "π/3 (60°)", "π/2 (90°)", "π (180°)"];

    print("Trigonometric function values:");

    k = 0;
    while (k < angles.length()) {
        angle = angles[k];
        name = angle_names[k];
        sin_val = sine(angle);
        cos_val = cosine(angle);
        tan_val = tangent(angle);

        print("Angle: " + name);
        print("  sin = " + sin_val);
        print("  cos = " + cos_val);
        print("  tan = " + tan_val);

        k = k + 1;
    }

    return {
        constants: {pi: PI, e: E},
        test_angles: angles,
        results: "trigonometric_calculations_completed"
    };
}

// Statistical and analytical functions
function statistical_analytical_functions() {
    print("\n=== Statistical and Analytical Functions ===");

    // Statistical measures
    function mean(numbers) {
        if (numbers.length() == 0) {
            return 0;
        }

        sum = 0;
        i = 0;
        while (i < numbers.length()) {
            sum = sum + numbers[i];
            i = i + 1;
        }
        return sum / numbers.length();
    }

    function median(numbers) {
        if (numbers.length() == 0) {
            return 0;
        }

        // Simple bubble sort
        sorted = [];
        j = 0;
        while (j < numbers.length()) {
            sorted[j] = numbers[j];
            j = j + 1;
        }

        // Bubble sort implementation
        n = sorted.length();
        k = 0;
        while (k < n - 1) {
            l = 0;
            while (l < n - k - 1) {
                if (sorted[l] > sorted[l + 1]) {
                    temp = sorted[l];
                    sorted[l] = sorted[l + 1];
                    sorted[l + 1] = temp;
                }
                l = l + 1;
            }
            k = k + 1;
        }

        middle = n / 2;
        if (n % 2 == 0) {
            return (sorted[middle - 1] + sorted[middle]) / 2;
        } else {
            return sorted[middle - 0.5];
        }
    }

    function standard_deviation(numbers) {
        if (numbers.length() <= 1) {
            return 0;
        }

        avg = mean(numbers);
        sum_squared_diff = 0;

        i = 0;
        while (i < numbers.length()) {
            diff = numbers[i] - avg;
            sum_squared_diff = sum_squared_diff + (diff * diff);
            i = i + 1;
        }

        variance = sum_squared_diff / (numbers.length() - 1);
        return sqrt_approximation(variance);
    }

    function sqrt_approximation(n) {
        if (n < 0) {
            return 0;
        }
        if (n == 0 || n == 1) {
            return n;
        }

        x = n;
        precision = 0.000001;
        iterations = 0;

        while (iterations < 50) {
            root = 0.5 * (x + (n / x));
            if (abs(root - x) < precision) {
                break;
            }
            x = root;
            iterations = iterations + 1;
        }

        return x;
    }

    function abs(x) {
        return x < 0 ? -x : x;
    }

    function mode(numbers) {
        if (numbers.length() == 0) {
            return null;
        }

        // Count frequencies
        frequency = {};
        max_count = 0;
        mode_value = numbers[0];

        i = 0;
        while (i < numbers.length()) {
            num = numbers[i];
            count = frequency[num];
            if (count == null) {
                count = 0;
            }
            count = count + 1;
            frequency[num] = count;

            if (count > max_count) {
                max_count = count;
                mode_value = num;
            }

            i = i + 1;
        }

        return mode_value;
    }

    // Test with sample data
    dataset1 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20];
    dataset2 = [1, 3, 3, 6, 7, 8, 9, 3, 5, 2];
    dataset3 = [100, 85, 92, 78, 96, 88, 91, 79, 83, 87];

    datasets = [dataset1, dataset2, dataset3];
    dataset_names = ["Even numbers 2-20", "Mixed small numbers", "Test scores"];

    print("Statistical analysis of datasets:");

    m = 0;
    while (m < datasets.length()) {
        data = datasets[m];
        name = dataset_names[m];

        mean_val = mean(data);
        median_val = median(data);
        mode_val = mode(data);
        std_dev = standard_deviation(data);

        print("\nDataset: " + name);
        print("  Data: " + data);
        print("  Mean: " + mean_val);
        print("  Median: " + median_val);
        print("  Mode: " + mode_val);
        print("  Standard Deviation: " + std_dev);

        m = m + 1;
    }

    return {
        datasets: datasets,
        statistics: "calculated_for_all_datasets"
    };
}

// Number theory and discrete mathematics
function number_theory_discrete_math() {
    print("\n=== Number Theory and Discrete Mathematics ===");

    // Prime number functions
    function is_prime(n) {
        if (n <= 1) {
            return false;
        }
        if (n <= 3) {
            return true;
        }
        if (n % 2 == 0 || n % 3 == 0) {
            return false;
        }

        i = 5;
        while (i * i <= n) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
            i = i + 6;
        }
        return true;
    }

    function prime_factors(n) {
        factors = [];
        divisor = 2;

        while (divisor * divisor <= n) {
            while (n % divisor == 0) {
                factors[factors.length()] = divisor;
                n = n / divisor;
            }
            divisor = divisor + 1;
        }

        if (n > 1) {
            factors[factors.length()] = n;
        }

        return factors;
    }

    function gcd(a, b) {
        while (b != 0) {
            temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    function lcm(a, b) {
        return abs(a * b) / gcd(a, b);
    }

    function abs(x) {
        return x < 0 ? -x : x;
    }

    // Fibonacci sequence
    function fibonacci_sequence(n) {
        if (n <= 0) {
            return [];
        }
        if (n == 1) {
            return [0];
        }
        if (n == 2) {
            return [0, 1];
        }

        sequence = [0, 1];
        i = 2;
        while (i < n) {
            next = sequence[i - 1] + sequence[i - 2];
            sequence[i] = next;
            i = i + 1;
        }

        return sequence;
    }

    // Collatz conjecture sequence
    function collatz_sequence(n) {
        sequence = [n];
        while (n != 1) {
            if (n % 2 == 0) {
                n = n / 2;
            } else {
                n = 3 * n + 1;
            }
            sequence[sequence.length()] = n;
        }
        return sequence;
    }

    // Test prime numbers
    print("Prime number testing:");
    test_primes = [2, 3, 4, 5, 17, 25, 29, 35, 41, 49];
    n = 0;
    while (n < test_primes.length()) {
        num = test_primes[n];
        prime_result = is_prime(num);
        print("  " + num + " is " + (prime_result ? "prime" : "not prime"));
        n = n + 1;
    }

    // Test prime factorization
    print("\nPrime factorization:");
    factor_numbers = [12, 18, 60, 100, 37];
    o = 0;
    while (o < factor_numbers.length()) {
        num = factor_numbers[o];
        factors = prime_factors(num);
        print("  " + num + " = " + factors);
        o = o + 1;
    }

    // Test GCD and LCM
    print("\nGCD and LCM calculations:");
    number_pairs = [[12, 18], [24, 36], [17, 19], [48, 18]];
    p = 0;
    while (p < number_pairs.length()) {
        pair = number_pairs[p];
        a = pair[0];
        b = pair[1];
        gcd_result = gcd(a, b);
        lcm_result = lcm(a, b);
        print("  GCD(" + a + ", " + b + ") = " + gcd_result + ", LCM(" + a + ", " + b + ") = " + lcm_result);
        p = p + 1;
    }

    // Test Fibonacci
    print("\nFibonacci sequence (first 15 numbers):");
    fib_seq = fibonacci_sequence(15);
    print("  " + fib_seq);

    // Test Collatz conjecture
    print("\nCollatz sequences:");
    collatz_starts = [3, 5, 7, 12];
    q = 0;
    while (q < collatz_starts.length()) {
        start = collatz_starts[q];
        collatz_seq = collatz_sequence(start);
        print("  Starting with " + start + " (" + collatz_seq.length() + " steps): " + collatz_seq);
        q = q + 1;
    }

    return {
        primes_tested: test_primes,
        factorizations: factor_numbers,
        fibonacci: fib_seq,
        collatz_examples: collatz_starts
    };
}

// Complex mathematical algorithms
function complex_mathematical_algorithms() {
    print("\n=== Complex Mathematical Algorithms ===");

    // Matrix operations
    function matrix_multiply(A, B) {
        rows_A = A.length();
        cols_A = A[0].length();
        rows_B = B.length();
        cols_B = B[0].length();

        if (cols_A != rows_B) {
            return null; // Cannot multiply
        }

        result = [];
        i = 0;
        while (i < rows_A) {
            result[i] = [];
            j = 0;
            while (j < cols_B) {
                sum = 0;
                k = 0;
                while (k < cols_A) {
                    sum = sum + A[i][k] * B[k][j];
                    k = k + 1;
                }
                result[i][j] = sum;
                j = j + 1;
            }
            i = i + 1;
        }

        return result;
    }

    function matrix_determinant_2x2(matrix) {
        if (matrix.length() != 2 || matrix[0].length() != 2) {
            return 0;
        }
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
    }

    // Polynomial evaluation using Horner's method
    function evaluate_polynomial(coefficients, x) {
        if (coefficients.length() == 0) {
            return 0;
        }

        result = coefficients[0];
        i = 1;
        while (i < coefficients.length()) {
            result = result * x + coefficients[i];
            i = i + 1;
        }

        return result;
    }

    // Numerical integration (Trapezoidal rule)
    function trapezoidal_integration(func_values, a, b) {
        n = func_values.length();
        if (n < 2) {
            return 0;
        }

        h = (b - a) / (n - 1);
        sum = func_values[0] + func_values[n - 1];

        i = 1;
        while (i < n - 1) {
            sum = sum + 2 * func_values[i];
            i = i + 1;
        }

        return (h / 2) * sum;
    }

    // Newton-Raphson method for finding roots
    function newton_raphson(initial_guess, tolerance, max_iterations) {
        // Find root of f(x) = x^2 - 2 (should find sqrt(2))
        x = initial_guess;
        iteration = 0;

        while (iteration < max_iterations) {
            fx = x * x - 2;           // f(x)
            fpx = 2 * x;              // f'(x)

            if (abs(fpx) < tolerance) {
                break;
            }

            x_new = x - fx / fpx;

            if (abs(x_new - x) < tolerance) {
                break;
            }

            x = x_new;
            iteration = iteration + 1;
        }

        return {
            root: x,
            iterations: iteration,
            converged: iteration < max_iterations
        };
    }

    function abs(x) {
        return x < 0 ? -x : x;
    }

    // Test matrix multiplication
    print("Matrix operations:");
    matrix_A = [[1, 2], [3, 4]];
    matrix_B = [[5, 6], [7, 8]];
    matrix_result = matrix_multiply(matrix_A, matrix_B);

    print("  Matrix A: [[1, 2], [3, 4]]");
    print("  Matrix B: [[5, 6], [7, 8]]");
    print("  A × B = " + matrix_result);

    det_A = matrix_determinant_2x2(matrix_A);
    det_B = matrix_determinant_2x2(matrix_B);
    print("  det(A) = " + det_A);
    print("  det(B) = " + det_B);

    // Test polynomial evaluation
    print("\nPolynomial evaluation:");
    coeffs = [2, -3, 1]; // 2x^2 - 3x + 1
    test_x_values = [0, 1, 2, 3, -1];
    r = 0;
    while (r < test_x_values.length()) {
        x_val = test_x_values[r];
        poly_result = evaluate_polynomial(coeffs, x_val);
        print("  P(" + x_val + ") = " + poly_result);
        r = r + 1;
    }

    // Test trapezoidal integration
    print("\nNumerical integration (y = x^2 from 0 to 2):");
    x_points = [0, 0.5, 1.0, 1.5, 2.0];
    y_values = [];
    s = 0;
    while (s < x_points.length()) {
        x = x_points[s];
        y_values[s] = x * x;
        s = s + 1;
    }
    integral_result = trapezoidal_integration(y_values, 0, 2);
    print("  Approximate integral = " + integral_result + " (exact = 2.667)");

    // Test Newton-Raphson
    print("\nNewton-Raphson method (finding sqrt(2)):");
    nr_result = newton_raphson(1.0, 0.000001, 50);
    print("  Root found: " + nr_result.root);
    print("  Iterations: " + nr_result.iterations);
    print("  Converged: " + nr_result.converged);

    return {
        matrix_ops: matrix_result,
        polynomial_test: "completed",
        integration_result: integral_result,
        newton_raphson: nr_result
    };
}

// Main function to run all mathematical tests
function main() {
    print("==============================================");
    print("  COMPREHENSIVE MATHEMATICAL OPERATIONS TEST");
    print("==============================================");

    results = {};

    results.basic_arithmetic = basic_arithmetic_operations();
    results.advanced_functions = advanced_mathematical_functions();
    results.trigonometric = trigonometric_approximations();
    results.statistical = statistical_analytical_functions();
    results.number_theory = number_theory_discrete_math();
    results.complex_algorithms = complex_mathematical_algorithms();

    print("\n==============================================");
    print("  ALL MATHEMATICAL OPERATIONS TESTS COMPLETED");
    print("==============================================");

    return results;
}

// Execute comprehensive mathematical operations test
main();