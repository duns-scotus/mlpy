// ML importing Python modules demonstration
import math;
import json;
import random;

function mathOperations() {
    // Using Python's math module
    radius = 5.0;
    area = math.pi * radius * radius;
    sqrt_result = math.sqrt(25.0);
    power_result = math.pow(2.0, 8.0);

    return {
        "area": area,
        "sqrt": sqrt_result,
        "power": power_result,
        "pi": math.pi,
        "e": math.e
    };
}

function randomOperations() {
    // Using Python's random module
    random_float = random.random();
    random_choice = random.choice([1, 2, 3, 4, 5]);

    return {
        "random_float": random_float,
        "choice": random_choice
    };
}

function jsonOperations() {
    // Using Python's json module
    data = {"name": "ML Program", "version": 1.0, "active": true};
    json_string = json.dumps(data);

    return {
        "original": data,
        "serialized": json_string
    };
}

function combinedOperations() {
    // Combining multiple Python modules
    math_result = mathOperations();
    random_result = randomOperations();
    json_result = jsonOperations();

    // Create comprehensive result
    final_result = {
        "math": math_result,
        "random": random_result,
        "json": json_result,
        "timestamp": "generated_by_ml"
    };

    return final_result;
}