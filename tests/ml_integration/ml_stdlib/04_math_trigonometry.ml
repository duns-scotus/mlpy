// Test stdlib module: math - Trigonometric functions
// Features tested: sin(), cos(), tan(), asin(), acos(), atan(), atan2(), radians(), degrees()
// Module: math

import math;

function test_angle_conversions() {
    results = {};

    // Degrees to radians
    results.deg_0 = math.radians(0.0);          // 0
    results.deg_90 = math.radians(90.0);        // ~1.57
    results.deg_180 = math.radians(180.0);      // ~3.14
    results.deg_360 = math.radians(360.0);      // ~6.28

    // Radians to degrees
    pi = math.pi;
    results.rad_0 = math.degrees(0.0);          // 0
    results.rad_pi_2 = math.degrees(pi / 2.0);  // 90
    results.rad_pi = math.degrees(pi);          // 180
    results.rad_2pi = math.degrees(2.0 * pi);   // 360

    return results;
}

function test_basic_trig() {
    results = {};

    pi = math.pi;

    // Sine
    results.sin_0 = math.round(math.sin(0.0));              // 0
    results.sin_90 = math.round(math.sin(pi / 2.0));        // 1
    results.sin_180 = math.round(math.sin(pi));             // 0
    results.sin_270 = math.round(math.sin(3.0 * pi / 2.0)); // -1

    // Cosine
    results.cos_0 = math.round(math.cos(0.0));              // 1
    results.cos_90 = math.round(math.cos(pi / 2.0));        // 0
    results.cos_180 = math.round(math.cos(pi));             // -1
    results.cos_270 = math.round(math.cos(3.0 * pi / 2.0)); // 0

    // Tangent
    results.tan_0 = math.round(math.tan(0.0));              // 0
    results.tan_45 = math.round(math.tan(pi / 4.0));        // 1
    results.tan_180 = math.round(math.tan(pi));             // 0

    return results;
}

function test_inverse_trig() {
    results = {};

    // Arcsine
    results.asin_0 = math.round(math.asin(0.0));            // 0
    results.asin_1 = math.round(math.asin(1.0));            // 2 (rounded from pi/2)
    results.asin_neg1 = math.round(math.asin(-1.0));        // -2 (rounded from -pi/2)

    // Arccosine
    results.acos_1 = math.round(math.acos(1.0));            // 0
    results.acos_0 = math.round(math.acos(0.0));            // 2 (rounded from pi/2)
    results.acos_neg1 = math.round(math.acos(-1.0));        // 3 (rounded from pi)

    // Arctangent
    results.atan_0 = math.round(math.atan(0.0));            // 0
    results.atan_1 = math.round(math.atan(1.0));            // 1 (rounded from pi/4)
    results.atan_neg1 = math.round(math.atan(-1.0));        // -1 (rounded from -pi/4)

    return results;
}

function test_atan2() {
    results = {};

    // atan2(y, x) - Returns angle in radians
    results.atan2_0_1 = math.round(math.atan2(0.0, 1.0));   // 0 (0 degrees)
    results.atan2_1_0 = math.round(math.atan2(1.0, 0.0));   // 2 (90 degrees)
    results.atan2_0_neg1 = math.round(math.atan2(0.0, -1.0)); // 3 (180 degrees)
    results.atan2_neg1_0 = math.round(math.atan2(-1.0, 0.0)); // -2 (-90 degrees)

    return results;
}

function test_trig_identities() {
    results = {};

    pi = math.pi;

    // sin²(x) + cos²(x) = 1
    angle = pi / 3.0;  // 60 degrees
    sin_val = math.sin(angle);
    cos_val = math.cos(angle);
    identity = math.pow(sin_val, 2.0) + math.pow(cos_val, 2.0);
    results.pythagorean_identity = math.round(identity);  // 1

    // tan(x) = sin(x) / cos(x)
    angle2 = pi / 4.0;  // 45 degrees
    tan_direct = math.tan(angle2);
    tan_calculated = math.sin(angle2) / math.cos(angle2);
    results.tan_identity = math.round(tan_direct) == math.round(tan_calculated);

    return results;
}

function test_triangle_calculations() {
    results = {};

    // Right triangle with 30-60-90 angles
    hypotenuse = 10.0;
    angle_30 = math.radians(30.0);

    // Opposite side = hypotenuse * sin(angle)
    opposite = hypotenuse * math.sin(angle_30);
    results.opposite_30 = math.round(opposite);  // 5

    // Adjacent side = hypotenuse * cos(angle)
    adjacent = hypotenuse * math.cos(angle_30);
    results.adjacent_30 = math.round(adjacent);  // 9

    return results;
}

function test_circular_motion() {
    results = {};

    // Point on unit circle at 45 degrees
    angle = math.radians(45.0);
    x = math.cos(angle);
    y = math.sin(angle);

    // Both x and y should be approximately 0.707 (√2/2)
    results.circle_x = math.round(x * 100.0);  // 71
    results.circle_y = math.round(y * 100.0);  // 71

    // Distance from origin should be 1 (unit circle)
    dist = math.sqrt(math.pow(x, 2.0) + math.pow(y, 2.0));
    results.unit_radius = math.round(dist);    // 1

    return results;
}

function main() {
    all_results = {};

    all_results.conversions = test_angle_conversions();
    all_results.trig = test_basic_trig();
    all_results.inverse = test_inverse_trig();
    all_results.atan2 = test_atan2();
    all_results.identities = test_trig_identities();
    all_results.triangles = test_triangle_calculations();
    all_results.circular = test_circular_motion();

    return all_results;
}

// Run tests
test_results = main();
