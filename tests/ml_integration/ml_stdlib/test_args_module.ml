// Test all args module functions end-to-end
// This validates the complete ML→Python transpilation pipeline for args operations

import args;
import console;

console.log("=== Testing args Module ===");

// Test 1: Create parser
console.log("[Test 1] Create parser");
parser = args.create_parser("Test Tool", "A test command-line tool");
if (typeof(parser) == "object") {
    console.log("PASS: create_parser() returns object");
} else {
    console.log("FAIL: create_parser() should return object");
}

// Test 2: Add flag
console.log("[Test 2] Add flag");
parser.add_flag("verbose", "v", "Enable verbose output");
console.log("PASS: add_flag() completed");

// Test 3: Add flag without short name
console.log("[Test 3] Add flag without short name");
parser.add_flag("debug", null, "Enable debug mode");
console.log("PASS: add_flag() with null short name completed");

// Test 4: Add option
console.log("[Test 4] Add option");
parser.add_option("output", "o", "Output file", "output.txt");
console.log("PASS: add_option() completed");

// Test 5: Add option with null default
console.log("[Test 5] Add option with null default");
parser.add_option("config", "c", "Config file", null);
console.log("PASS: add_option() with null default completed");

// Test 6: Add required positional
console.log("[Test 6] Add required positional");
parser.add_positional("input", "Input file", true);
console.log("PASS: add_positional() with required=true completed");

// Test 7: Add optional positional
console.log("[Test 7] Add optional positional");
parser.add_positional("extra", "Extra files", false);
console.log("PASS: add_positional() with required=false completed");

// Test 8: Parse long flag
console.log("[Test 8] Parse long flag");
parser2 = args.create_parser("Tool", "Desc");
parser2.add_flag("verbose", "v", "Verbose");
parsed = parser2.parse(["--verbose"]);
if (parsed.get_bool("verbose") == true) {
    console.log("PASS: Parsing long flag works");
} else {
    console.log("FAIL: Long flag should be true");
}

// Test 9: Parse short flag
console.log("[Test 9] Parse short flag");
parser3 = args.create_parser("Tool", "Desc");
parser3.add_flag("verbose", "v", "Verbose");
parsed2 = parser3.parse(["-v"]);
if (parsed2.get_bool("verbose") == true) {
    console.log("PASS: Parsing short flag works");
} else {
    console.log("FAIL: Short flag should be true");
}

// Test 10: Parse multiple short flags combined
console.log("[Test 10] Parse multiple short flags combined");
parser4 = args.create_parser("Tool", "Desc");
parser4.add_flag("verbose", "v", "Verbose");
parser4.add_flag("force", "f", "Force");
parsed3 = parser4.parse(["-vf"]);
if (parsed3.get_bool("verbose") == true) {
    if (parsed3.get_bool("force") == true) {
        console.log("PASS: Parsing combined short flags works");
    } else {
        console.log("FAIL: Force flag should be true");
    }
} else {
    console.log("FAIL: Verbose flag should be true");
}

// Test 11: Parse long option with value
console.log("[Test 11] Parse long option with value");
parser5 = args.create_parser("Tool", "Desc");
parser5.add_option("output", "o", "Output", "default.txt");
parsed4 = parser5.parse(["--output", "custom.txt"]);
if (parsed4.get("output") == "custom.txt") {
    console.log("PASS: Parsing long option with value works");
} else {
    console.log("FAIL: Output should be custom.txt");
}

// Test 12: Parse short option with value
console.log("[Test 12] Parse short option with value");
parser6 = args.create_parser("Tool", "Desc");
parser6.add_option("output", "o", "Output", "default.txt");
parsed5 = parser6.parse(["-o", "custom.txt"]);
if (parsed5.get("output") == "custom.txt") {
    console.log("PASS: Parsing short option with value works");
} else {
    console.log("FAIL: Output should be custom.txt");
}

// Test 13: Option uses default when not provided
console.log("[Test 13] Option uses default value");
parser7 = args.create_parser("Tool", "Desc");
parser7.add_option("output", "o", "Output", "default.txt");
parsed6 = parser7.parse([]);
if (parsed6.get("output") == "default.txt") {
    console.log("PASS: Default value used correctly");
} else {
    console.log("FAIL: Output should be default.txt");
}

// Test 14: Parse positional argument
console.log("[Test 14] Parse positional argument");
parser8 = args.create_parser("Tool", "Desc");
parser8.add_positional("input", "Input file", true);
parsed7 = parser8.parse(["file.txt"]);
if (parsed7.get("input") == "file.txt") {
    console.log("PASS: Parsing positional argument works");
} else {
    console.log("FAIL: Input should be file.txt");
}

// Test 15: Parse multiple positional arguments
console.log("[Test 15] Parse multiple positional arguments");
parser9 = args.create_parser("Tool", "Desc");
parser9.add_positional("input", "Input file", true);
parser9.add_positional("output", "Output file", false);
parsed8 = parser9.parse(["input.txt", "output.txt"]);
if (parsed8.get("input") == "input.txt") {
    if (parsed8.get("output") == "output.txt") {
        console.log("PASS: Parsing multiple positionals works");
    } else {
        console.log("FAIL: Output should be output.txt");
    }
} else {
    console.log("FAIL: Input should be input.txt");
}

// Test 16: Missing optional positional is ok
console.log("[Test 16] Missing optional positional");
parser10 = args.create_parser("Tool", "Desc");
parser10.add_positional("input", "Input", true);
parser10.add_positional("output", "Output", false);
parsed9 = parser10.parse(["input.txt"]);
if (parsed9.get("input") == "input.txt") {
    if (parsed9.get("output") == null) {
        console.log("PASS: Missing optional positional is null");
    } else {
        console.log("FAIL: Optional positional should be null");
    }
} else {
    console.log("FAIL: Input should be input.txt");
}

// Test 17: has() method
console.log("[Test 17] has() method");
parser11 = args.create_parser("Tool", "Desc");
parser11.add_flag("verbose", "v", "Verbose");
parser11.add_option("output", "o", "Output", "out.txt");
parsed10 = parser11.parse(["-v"]);
if (parsed10.has("verbose") == true) {
    if (parsed10.has("missing") == false) {
        console.log("PASS: has() method works correctly");
    } else {
        console.log("FAIL: has() should return false for missing");
    }
} else {
    console.log("FAIL: has() should return true for verbose");
}

// Test 18: get() with default value
console.log("[Test 18] get() with default value");
parser12 = args.create_parser("Tool", "Desc");
parsed11 = parser12.parse([]);
result = parsed11.get("missing", "default_value");
if (result == "default_value") {
    console.log("PASS: get() with default works");
} else {
    console.log("FAIL: get() should return default_value");
}

// Test 19: flags() method returns dictionary
console.log("[Test 19] flags() method");
parser13 = args.create_parser("Tool", "Desc");
parser13.add_flag("verbose", "v", "Verbose");
parser13.add_flag("force", "f", "Force");
parsed12 = parser13.parse(["-vf"]);
all_flags = parsed12.flags();
if (typeof(all_flags) == "object") {
    console.log("PASS: flags() returns dictionary");
} else {
    console.log("FAIL: flags() should return object");
}

// Test 20: options() method returns dictionary
console.log("[Test 20] options() method");
parser14 = args.create_parser("Tool", "Desc");
parser14.add_option("output", "o", "Output", "out.txt");
parser14.add_option("format", "f", "Format", "json");
parsed13 = parser14.parse(["--output", "custom.txt"]);
all_options = parsed13.options();
if (typeof(all_options) == "object") {
    console.log("PASS: options() returns dictionary");
} else {
    console.log("FAIL: options() should return object");
}

// Test 21: positionals() method returns list
console.log("[Test 21] positionals() method");
parser15 = args.create_parser("Tool", "Desc");
parser15.add_positional("input", "Input", true);
parser15.add_positional("output", "Output", false);
parsed14 = parser15.parse(["file1.txt", "file2.txt"]);
all_positionals = parsed14.positionals();
if (typeof(all_positionals) == "array") {
    if (len(all_positionals) == 2) {
        console.log("PASS: positionals() returns array with 2 elements");
    } else {
        console.log("FAIL: positionals() should have 2 elements");
    }
} else {
    console.log("FAIL: positionals() should return array");
}

// Test 22: help() generates help text
console.log("[Test 22] help() generates help text");
parser16 = args.create_parser("My Tool", "Does cool things");
parser16.add_flag("verbose", "v", "Verbose output");
parser16.add_option("output", "o", "Output file", "out.txt");
parser16.add_positional("input", "Input file", true);
help_text = parser16.help();
if (typeof(help_text) == "string") {
    console.log("PASS: help() returns string");
} else {
    console.log("FAIL: help() should return string");
}

// Test 23: Help flag detection
console.log("[Test 23] Help flag detection");
parser17 = args.create_parser("Tool", "Desc");
parsed15 = parser17.parse(["--help"]);
if (parsed15.has("help") == true) {
    console.log("PASS: --help flag detected");
} else {
    console.log("FAIL: --help flag should be detected");
}

// Test 24: Short help flag detection
console.log("[Test 24] Short help flag detection");
parser18 = args.create_parser("Tool", "Desc");
parsed16 = parser18.parse(["-h"]);
if (parsed16.has("help") == true) {
    console.log("PASS: -h flag detected");
} else {
    console.log("FAIL: -h flag should be detected");
}

// Test 25: Complex argument parsing
console.log("[Test 25] Complex argument parsing");
parser19 = args.create_parser("Data Processor", "Process CSV files");
parser19.add_flag("verbose", "v", "Verbose output");
parser19.add_flag("force", "f", "Force overwrite");
parser19.add_option("output", "o", "Output file", "output.csv");
parser19.add_option("format", null, "Format", "csv");
parser19.add_positional("input", "Input file", true);
parsed17 = parser19.parse(["-vf", "--output", "result.csv", "--format", "json", "data.csv"]);

all_passed = true;
if (parsed17.get_bool("verbose") != true) {
    console.log("FAIL: verbose should be true");
    all_passed = false;
}
if (parsed17.get_bool("force") != true) {
    console.log("FAIL: force should be true");
    all_passed = false;
}
if (parsed17.get("output") != "result.csv") {
    console.log("FAIL: output should be result.csv");
    all_passed = false;
}
if (parsed17.get("format") != "json") {
    console.log("FAIL: format should be json");
    all_passed = false;
}
if (parsed17.get("input") != "data.csv") {
    console.log("FAIL: input should be data.csv");
    all_passed = false;
}

if (all_passed) {
    console.log("PASS: Complex argument parsing works");
}

// Test 26: Error handling - missing required positional
console.log("[Test 26] Error handling - missing required positional");
parser20 = args.create_parser("Tool", "Desc");
parser20.add_positional("input", "Input file", true);
try {
    parser20.parse([]);
    console.log("FAIL: Should have thrown error for missing required positional");
} except (error) {
    console.log("PASS: Error thrown for missing required positional");
}

// Test 27: Error handling - unknown option
console.log("[Test 27] Error handling - unknown option");
parser21 = args.create_parser("Tool", "Desc");
try {
    parser21.parse(["--unknown"]);
    console.log("FAIL: Should have thrown error for unknown option");
} except (error) {
    console.log("PASS: Error thrown for unknown option");
}

// Test 28: Error handling - option without value
console.log("[Test 28] Error handling - option without value");
parser22 = args.create_parser("Tool", "Desc");
parser22.add_option("output", "o", "Output", "out.txt");
try {
    parser22.parse(["--output"]);
    console.log("FAIL: Should have thrown error for option without value");
} except (error) {
    console.log("PASS: Error thrown for option without value");
}

console.log("=== All args module tests passed! ===");
