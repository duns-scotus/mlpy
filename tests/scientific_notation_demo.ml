// Comprehensive scientific notation test program
// Tests: very large numbers, very small numbers, scientific calculations

function physicalConstants() {
    // Fundamental physical constants in scientific notation
    speed_of_light = 2.998e8;        // m/s
    planck_constant = 6.626e-34;     // J*s
    avogadro_number = 6.022e23;      // mol^-1
    elementary_charge = 1.602e-19;   // C
    gravitational_constant = 6.674e-11;  // m^3 kg^-1 s^-2

    return {
        "c": speed_of_light,
        "h": planck_constant,
        "Na": avogadro_number,
        "e": elementary_charge,
        "G": gravitational_constant
    };
}

function astronomicalScales() {
    // Very large numbers in astronomy
    light_year = 9.461e15;           // meters
    parsec = 3.086e16;               // meters
    age_of_universe = 4.35e17;       // seconds
    observable_universe = 8.8e26;    // meters diameter

    // Very small atomic scales
    proton_mass = 1.673e-27;         // kg
    electron_mass = 9.109e-31;       // kg
    bohr_radius = 5.292e-11;         // meters

    return {
        "large": [light_year, parsec, age_of_universe, observable_universe],
        "small": [proton_mass, electron_mass, bohr_radius]
    };
}

function scientificCalculations() {
    // Energy calculations with scientific notation
    mass = 1e-26;                    // kg (small particle)
    velocity = 3e7;                  // m/s (10% speed of light)

    // Kinetic energy: KE = 0.5 * m * v^2
    kinetic_energy = 0.5 * mass * velocity * velocity;

    // Wavelength calculation: λ = h / (m * v)
    h = 6.626e-34;                   // Planck constant
    wavelength = h / (mass * velocity);

    // Power calculations
    power = 1.5e6;                   // 1.5 MW
    time = 3.6e3;                    // 1 hour in seconds
    energy = power * time;           // Joules

    return {
        "kinetic_energy": kinetic_energy,
        "wavelength": wavelength,
        "energy": energy,
        "ratios": {
            "mass_velocity_ratio": mass / velocity,
            "energy_power_ratio": energy / power
        }
    };
}

function extremeNumbers() {
    // Test edge cases and extreme values

    // Very large positive exponents
    googol = 1e100;                  // 10^100
    planck_time_inverse = 1.855e43;  // 1/Planck time (Hz)

    // Very small positive numbers
    planck_length = 1.616e-35;       // meters
    planck_time = 5.391e-44;         // seconds

    // Mixed calculations
    ratio_large_small = googol / planck_length;

    // Zero exponent (should equal the base)
    unity_test = 42.0e0;             // Should equal 42.0

    return {
        "extremes": {
            "very_large": [googol, planck_time_inverse],
            "very_small": [planck_length, planck_time],
            "calculated": ratio_large_small,
            "zero_exp": unity_test
        }
    };
}

function scientificNotationValidation() {
    // Test all supported scientific notation formats

    // Positive exponents
    positive_e = 1.5e6;              // lowercase e
    positive_E = 2.3E8;              // uppercase E
    positive_explicit = 3.7e+4;     // explicit +

    // Negative exponents
    negative_e = 4.2e-5;             // lowercase e
    negative_E = 5.1E-7;             // uppercase E

    // Integer base with scientific notation
    int_scientific = 7e9;            // No decimal point

    // Zero exponent
    zero_exp = 8.9e0;                // Should equal 8.9

    return {
        "formats": [
            positive_e, positive_E, positive_explicit,
            negative_e, negative_E, int_scientific, zero_exp
        ],
        "validation": {
            "sum": positive_e + negative_e,
            "product": int_scientific * planck_length,
            "difference": positive_E - positive_e
        }
    };
}

// Main computation combining all scientific notation features
function main() {
    constants = physicalConstants();
    scales = astronomicalScales();
    calculations = scientificCalculations();
    extremes = extremeNumbers();
    validation = scientificNotationValidation();

    return {
        "constants": constants,
        "scales": scales,
        "calculations": calculations,
        "extremes": extremes,
        "validation": validation,
        "meta": {
            "total_numbers": 25,
            "scientific_notation_count": 23
        }
    };
}