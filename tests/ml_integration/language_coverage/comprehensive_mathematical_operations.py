"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports



from mlpy.stdlib.collections_bridge import collections as ml_collections
from mlpy.stdlib.math_bridge import math as ml_math


def basic_arithmetic_operations():
    print("=== Basic Arithmetic Operations and Precedence ===")
    a = 15
    b = 4
    c = 2
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b
    modulo = a % b
    print(

            str(str(str("Basic arithmetic with a=" + str(a)) + ", b=") + str(b))
            + ":"

    )
    print(

            str(
                str(str(str("Addition: " + str(a)) + " + ") + str(b)) + " = "
            )
            + str(addition)

    )
    print(

            str(

                    str(str(str("Subtraction: " + str(a)) + " - ") + str(b))
                    + " = "

            )
            + str(subtraction)

    )
    print(

            str(

                    str(str(str("Multiplication: " + str(a)) + " * ") + str(b))
                    + " = "

            )
            + str(multiplication)

    )
    print(

            str(
                str(str(str("Division: " + str(a)) + " / ") + str(b)) + " = "
            )
            + str(division)

    )
    print(

            str(str(str(str("Modulo: " + str(a)) + " % ") + str(b)) + " = ")
            + str(modulo)

    )
    expr1 = a + (b * c)
    expr2 = (a + b) * c
    expr3 = (a / b) + c
    expr4 = a / (b + c)
    expr5 = (a + b) - (c * 2)
    expr6 = ((a * b) % c) + 1
    print("\\nOperator precedence examples:")
    print("15 + 4 * 2 = " + str(expr1))
    print("(15 + 4) * 2 = " + str(expr2))
    print("15 / 4 + 2 = " + str(expr3))
    print("15 / (4 + 2) = " + str(expr4))
    print("15 + 4 - 2 * 2 = " + str(expr5))
    print("15 * 4 % 2 + 1 = " + str(expr6))
    positive = a
    negative = a
    double_negative = a
    print("\\nUnary operations:")
    print(str(str("Positive: +" + str(a)) + " = ") + str(positive))
    print(str(str("Negative: -" + str(a)) + " = ") + str(negative))
    print(str(str("Double negative: -(-" + str(a)) + ") = ") + str(double_negative))
    return {
        "basic": {
            "addition": addition,
            "subtraction": subtraction,
            "multiplication": multiplication,
            "division": division,
            "modulo": modulo,
        },
        "precedence": [expr1, expr2, expr3, expr4, expr5, expr6],
        "unary": {"positive": positive, "negative": negative, "double_negative": double_negative},
    }


def advanced_mathematical_functions():
    print("\\n=== Advanced Mathematical Functions ===")

    def power(base, exponent):
        if exponent == 0:
            return 1
        if exponent == 1:
            return base
        result = 1
        i = 0
        while i < exponent:
            result = result * base
            i = i + 1
        return result

    def square_root(n):
        if n < 0:
            return 0
        if (n == 0) or (n == 1):
            return n
        x = n
        precision = 1e-06
        iterations = 0
        max_iterations = 100
        while iterations < max_iterations:
            root = 0.5 * (x + (n / x))
            if abs(root - x) < precision:
                break
            x = root
            iterations = iterations + 1
        return x

    def abs(x):
        return x if (x < 0) else x

    def max(a, b):
        return a if (a > b) else b

    def min(a, b):
        return a if (a < b) else b

    pow_results = [0, 0, 0, 0, 0]
    pow_results[0] = power(2, 3)
    pow_results[1] = power(5, 2)
    pow_results[2] = power(3, 4)
    pow_results[3] = power(10, 0)
    pow_results[4] = power(7, 1)
    print("Power operations:")
    print("2^3 = " + str(pow_results[0]))
    print("5^2 = " + str(pow_results[1]))
    print("3^4 = " + str(pow_results[2]))
    print("10^0 = " + str(pow_results[3]))
    print("7^1 = " + str(pow_results[4]))
    sqrt_results = [0, 0, 0, 0, 0]
    sqrt_results[0] = square_root(25)
    sqrt_results[1] = square_root(16)
    sqrt_results[2] = square_root(2)
    sqrt_results[3] = square_root(10)
    sqrt_results[4] = square_root(0)
    print("\\nSquare root operations:")
    print("sqrt(25) = " + str(sqrt_results[0]))
    print("sqrt(16) = " + str(sqrt_results[1]))
    print("sqrt(2) = " + str(sqrt_results[2]))
    print("sqrt(10) = " + str(sqrt_results[3]))
    print("sqrt(0) = " + str(sqrt_results[4]))
    test_numbers = [15, 3, 0, 7, 12]
    abs_results = [0, 0, 0, 0, 0]
    i = 0
    while i < ml_collections.length(test_numbers):
        abs_results[i] = abs(test_numbers[i])
        i = i + 1
    print("\\nAbsolute value operations:")
    j = 0
    while j < ml_collections.length(test_numbers):
        print(
            str(str("abs(" + str(test_numbers[j])) + ") = ") + str(abs_results[j])
        )
        j = j + 1
    min_result = min(15, 23)
    max_result = max(15, 23)
    print("\\nMin/Max operations:")
    print("min(15, 23) = " + str(min_result))
    print("max(15, 23) = " + str(max_result))
    return {
        "power_results": pow_results,
        "sqrt_results": sqrt_results,
        "abs_results": abs_results,
        "min_max": {"min": min_result, "max": max_result},
    }


def trigonometric_approximations():
    print("\\n=== Trigonometric Function Approximations ===")
    PI = 3.14159265359
    E = 2.71828182846

    def factorial(n):
        if n <= 1:
            return 1
        result = 1
        i = 2
        while i <= n:
            result = result * i
            i = i + 1
        return result

    def sine(x):
        while x > (2 * PI):
            x = x - (2 * PI)
        while x < (2 * PI):
            x = x + (2 * PI)
        result = 0
        term = x
        i = 1
        while i <= 19:
            if (i % 4) == 1:
                result = result + term
            else:
                result = result - term
            term = ((term * x) * x) / ((i + 1) * (i + 2))
            i = i + 2
        return result

    def cosine(x):
        return sine((PI / 2) - x)

    def tangent(x):
        cos_x = cosine(x)
        if abs(cos_x) < 1e-06:
            return 0
        return sine(x) / cos_x

    def abs(x):
        return x if (x < 0) else x

    angles = [0, (PI / 6), (PI / 4), (PI / 3), (PI / 2), PI]
    angle_names = [
        "0",
        "pi/6 (30deg)",
        "pi/4 (45deg)",
        "pi/3 (60deg)",
        "pi/2 (90deg)",
        "pi (180deg)",
    ]
    print("Trigonometric function values:")
    k = 0
    while k < ml_collections.length(angles):
        angle = angles[k]
        name = angle_names[k]
        sin_val = sine(angle)
        cos_val = cosine(angle)
        tan_val = tangent(angle)
        print("Angle: " + str(name))
        print("  sin = " + str(sin_val))
        print("  cos = " + str(cos_val))
        print("  tan = " + str(tan_val))
        k = k + 1
    return {
        "constants": {"pi": PI, "e": E},
        "test_angles": angles,
        "results": "trigonometric_calculations_completed",
    }


def statistical_analytical_functions():
    print("\\n=== Statistical and Analytical Functions ===")

    def mean(numbers):
        if ml_collections.length(numbers) == 0:
            return 0
        sum = 0
        i = 0
        while i < ml_collections.length(numbers):
            sum = sum + numbers[i]
            i = i + 1
        return sum / ml_collections.length(numbers)

    def median(numbers):
        if ml_collections.length(numbers) == 0:
            return 0
        sorted = []
        j = 0
        while j < ml_collections.length(numbers):
            sorted = ml_collections.append(sorted, numbers[j])
            j = j + 1
        n = ml_collections.length(sorted)
        k = 0
        while k < (n - 1):
            l = 0
            while l < ((n - k) - 1):
                if sorted[l] > sorted[(l + 1)]:
                    temp = sorted[l]
                    sorted[l] = sorted[(l + 1)]
                    sorted[(l + 1)] = temp
                l = l + 1
            k = k + 1
        middle = ml_math.floor(n / 2)
        if (n % 2) == 0:
            return (sorted[(middle - 1)] + sorted[middle]) / 2
        else:
            return sorted[middle]

    def standard_deviation(numbers):
        if ml_collections.length(numbers) <= 1:
            return 0
        avg = mean(numbers)
        sum_squared_diff = 0
        i = 0
        while i < ml_collections.length(numbers):
            diff = numbers[i] - avg
            sum_squared_diff = sum_squared_diff + (diff * diff)
            i = i + 1
        variance = sum_squared_diff / (ml_collections.length(numbers) - 1)
        return sqrt_approximation(variance)

    def sqrt_approximation(n):
        if n < 0:
            return 0
        if (n == 0) or (n == 1):
            return n
        x = n
        precision = 1e-06
        iterations = 0
        while iterations < 50:
            root = 0.5 * (x + (n / x))
            if abs(root - x) < precision:
                break
            x = root
            iterations = iterations + 1
        return x

    def abs(x):
        return x if (x < 0) else x

    def mode(numbers):
        if ml_collections.length(numbers) == 0:
            return None
        return numbers[0]

    dataset1 = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    dataset2 = [1, 3, 3, 6, 7, 8, 9, 3, 5, 2]
    dataset3 = [100, 85, 92, 78, 96, 88, 91, 79, 83, 87]
    datasets = [dataset1, dataset2, dataset3]
    dataset_names = ["Even numbers 2-20", "Mixed small numbers", "Test scores"]
    print("Statistical analysis of datasets:")
    m = 0
    while m < ml_collections.length(datasets):
        data = datasets[m]
        name = dataset_names[m]
        mean_val = mean(data)
        median_val = median(data)
        mode_val = mode(data)
        std_dev = standard_deviation(data)
        print("\\nDataset: " + str(name))
        print("  Data: " + str(data))
        print("  Mean: " + str(mean_val))
        print("  Median: " + str(median_val))
        print("  Mode: " + str(mode_val))
        print("  Standard Deviation: " + str(std_dev))
        m = m + 1
    return {"datasets": datasets, "statistics": "calculated_for_all_datasets"}


def number_theory_discrete_math():
    print("\\n=== Number Theory and Discrete Mathematics ===")

    def is_prime(n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if ((n % 2) == 0) or ((n % 3) == 0):
            return False
        i = 5
        while (i * i) <= n:
            if ((n % i) == 0) or ((n % (i + 2)) == 0):
                return False
            i = i + 6
        return True

    def prime_factors(n):
        factors = []
        divisor = 2
        while (divisor * divisor) <= n:
            while (n % divisor) == 0:
                factors = ml_collections.append(factors, divisor)
                n = n / divisor
            divisor = divisor + 1
        if n > 1:
            factors = ml_collections.append(factors, n)
        return factors

    def gcd(a, b):
        while b != 0:
            temp = b
            b = a % b
            a = temp
        return a

    def lcm(a, b):
        return abs(a * b) / gcd(a, b)

    def abs(x):
        return x if (x < 0) else x

    def fibonacci_sequence(n):
        if n <= 0:
            return []
        if n == 1:
            return [0]
        if n == 2:
            return [0, 1]
        sequence = [0, 1]
        i = 2
        while i < n:
            next = sequence[(i - 1)] + sequence[(i - 2)]
            sequence = ml_collections.append(sequence, next)
            i = i + 1
        return sequence

    def collatz_sequence(n):
        sequence = [n]
        while n != 1:
            if (n % 2) == 0:
                n = n / 2
            else:
                n = (3 * n) + 1
            sequence = ml_collections.append(sequence, n)
        return sequence

    print("Prime number testing:")
    test_primes = [2, 3, 4, 5, 17, 25, 29, 35, 41, 49]
    n = 0
    while n < ml_collections.length(test_primes):
        num = test_primes[n]
        prime_result = is_prime(num)
        print(

                str(str("  " + str(num)) + " is ")
                + str("prime" if prime_result else "not prime")

        )
        n = n + 1
    print("\\nPrime factorization:")
    factor_numbers = [12, 18, 60, 100, 37]
    o = 0
    while o < ml_collections.length(factor_numbers):
        num = factor_numbers[o]
        factors = prime_factors(num)
        print(str(str("  " + str(num)) + " = ") + str(factors))
        o = o + 1
    print("\\nGCD and LCM calculations:")
    number_pairs = [[12, 18], [24, 36], [17, 19], [48, 18]]
    p = 0
    while p < ml_collections.length(number_pairs):
        pair = number_pairs[p]
        a = pair[0]
        b = pair[1]
        gcd_result = gcd(a, b)
        lcm_result = lcm(a, b)
        print(

                str(

                        str(

                                str(

                                        str(

                                                str(

                                                        str(

                                                                str(

                                                                        str(

                                                                                str(

                                                                                        str(

                                                                                                "  GCD("
                                                                                                + str(
                                                                                                    a
                                                                                                )

                                                                                        )
                                                                                        + ", "

                                                                                )
                                                                                + str(b)

                                                                        )
                                                                        + ") = "

                                                                )
                                                                + str(gcd_result)

                                                        )
                                                        + ", LCM("

                                                )
                                                + str(a)

                                        )
                                        + ", "

                                )
                                + str(b)

                        )
                        + ") = "

                )
                + str(lcm_result)

        )
        p = p + 1
    print("\\nFibonacci sequence (first 15 numbers):")
    fib_seq = fibonacci_sequence(15)
    print("  " + str(fib_seq))
    print("\\nCollatz sequences:")
    collatz_starts = [3, 5, 7, 12]
    q = 0
    while q < ml_collections.length(collatz_starts):
        start = collatz_starts[q]
        collatz_seq = collatz_sequence(start)
        print(

                str(

                        str(

                                str(str("  Starting with " + str(start)) + " (")
                                + str(ml_collections.length(collatz_seq))

                        )
                        + " steps): "

                )
                + str(collatz_seq)

        )
        q = q + 1
    return {
        "primes_tested": test_primes,
        "factorizations": factor_numbers,
        "fibonacci": fib_seq,
        "collatz_examples": collatz_starts,
    }


def complex_mathematical_algorithms():
    print("\\n=== Complex Mathematical Algorithms ===")

    def matrix_multiply(A, B):
        rows_A = ml_collections.length(A)
        cols_A = ml_collections.length(A[0])
        rows_B = ml_collections.length(B)
        cols_B = ml_collections.length(B[0])
        if cols_A != rows_B:
            return None
        result = []
        i = 0
        while i < rows_A:
            result = ml_collections.append(result, [])
            j = 0
            while j < cols_B:
                sum = 0
                k = 0
                while k < cols_A:
                    sum = sum + (A[i][k] * B[k][j])
                    k = k + 1
                result[i] = ml_collections.append(result[i], sum)
                j = j + 1
            i = i + 1
        return result

    def matrix_determinant_2x2(matrix):
        if (ml_collections.length(matrix) != 2) or (ml_collections.length(matrix[0]) != 2):
            return 0
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

    def evaluate_polynomial(coefficients, x):
        if ml_collections.length(coefficients) == 0:
            return 0
        result = coefficients[0]
        i = 1
        while i < ml_collections.length(coefficients):
            result = (result * x) + coefficients[i]
            i = i + 1
        return result

    def trapezoidal_integration(func_values, a, b):
        n = ml_collections.length(func_values)
        if n < 2:
            return 0
        h = (b - a) / (n - 1)
        sum = func_values[0] + func_values[(n - 1)]
        i = 1
        while i < (n - 1):
            sum = sum + (2 * func_values[i])
            i = i + 1
        return (h / 2) * sum

    def newton_raphson(initial_guess, tolerance, max_iterations):
        x = initial_guess
        iteration = 0
        while iteration < max_iterations:
            fx = (x * x) - 2
            fpx = 2 * x
            if abs(fpx) < tolerance:
                break
            x_new = x - (fx / fpx)
            if abs(x_new - x) < tolerance:
                break
            x = x_new
            iteration = iteration + 1
        return {"root": x, "iterations": iteration, "converged": (iteration < max_iterations)}

    def abs(x):
        return x if (x < 0) else x

    print("Matrix operations:")
    matrix_A = [[1, 2], [3, 4]]
    matrix_B = [[5, 6], [7, 8]]
    matrix_result = matrix_multiply(matrix_A, matrix_B)
    print("  Matrix A: [[1, 2], [3, 4]]")
    print("  Matrix B: [[5, 6], [7, 8]]")
    print("  A × B = " + str(matrix_result))
    det_A = matrix_determinant_2x2(matrix_A)
    det_B = matrix_determinant_2x2(matrix_B)
    print("  det(A) = " + str(det_A))
    print("  det(B) = " + str(det_B))
    print("\\nPolynomial evaluation:")
    coeffs = [2, 3, 1]
    test_x_values = [0, 1, 2, 3, 1]
    r = 0
    while r < ml_collections.length(test_x_values):
        x_val = test_x_values[r]
        poly_result = evaluate_polynomial(coeffs, x_val)
        print(str(str("  P(" + str(x_val)) + ") = ") + str(poly_result))
        r = r + 1
    print("\\nNumerical integration (y = x^2 from 0 to 2):")
    x_points = [0, 0.5, 1.0, 1.5, 2.0]
    y_values = [0, 0, 0, 0, 0]
    s = 0
    while s < ml_collections.length(x_points):
        x = x_points[s]
        y_values[s] = x * x
        s = s + 1
    integral_result = trapezoidal_integration(y_values, 0, 2)
    print(
        str("  Approximate integral = " + str(integral_result)) + " (exact = 2.667)"
    )
    print("\\nNewton-Raphson method (finding sqrt(2)):")
    nr_result = newton_raphson(1.0, 1e-06, 50)
    print("  Root found: " + str(nr_result["root"]))
    print("  Iterations: " + str(nr_result["iterations"]))
    print("  Converged: " + str(nr_result["converged"]))
    return {
        "matrix_ops": matrix_result,
        "polynomial_test": "completed",
        "integration_result": integral_result,
        "newton_raphson": nr_result,
    }


def main():
    print("==============================================")
    print("  COMPREHENSIVE MATHEMATICAL OPERATIONS TEST")
    print("==============================================")
    results = {}
    results["basic_arithmetic"] = basic_arithmetic_operations()
    results["advanced_functions"] = advanced_mathematical_functions()
    results["trigonometric"] = trigonometric_approximations()
    results["statistical"] = statistical_analytical_functions()
    results["number_theory"] = number_theory_discrete_math()
    results["complex_algorithms"] = complex_mathematical_algorithms()
    print("\\n==============================================")
    print("  ALL MATHEMATICAL OPERATIONS TESTS COMPLETED")
    print("==============================================")
    return results


main()

# End of generated code
