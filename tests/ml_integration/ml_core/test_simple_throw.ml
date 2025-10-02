// Simple throw test
function test() {
    result = null;

    try {
        throw {
            message: "Test error"
        };
    } except (e) {
        result = "caught";
    }

    return result;
}

x = test();
