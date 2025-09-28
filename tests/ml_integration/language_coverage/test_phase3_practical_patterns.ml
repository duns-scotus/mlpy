// Phase 3 Test: Practical Object Patterns
import collections;
import string;

function safe_upsert(arr, pos, item) {
    if (pos < arr.length) {
        new_arr = [];
        i = 0;
        while (i < arr.length) {
            if (i == pos) {
                new_arr = collections.append(new_arr, item);
            } else {
                new_arr = collections.append(new_arr, arr[i]);
            }
            i = i + 1;
        }
        return new_arr;
    } else {
        return collections.append(arr, item);
    }
}

function test_configuration_objects() {
    print("=== Configuration Objects ===");

    default_config = {
        timeout: 5000,
        retries: 3,
        debug: false,
        api_version: "v1"
    };

    user_config = {
        timeout: 8000,
        debug: true
    };

    // Merge configurations
    final_config = {
        timeout: user_config.timeout,
        retries: default_config.retries,
        debug: user_config.debug,
        api_version: default_config.api_version
    };

    print("Final timeout: " + string.toString(final_config.timeout));
    print("Debug mode: " + string.toString(final_config.debug));

    return final_config;
}

function test_result_objects() {
    print("=== Result Objects ===");

    function create_success(data) {
        return {
            success: true,
            data: data,
            error: null,
            timestamp: 1640995200
        };
    }

    function create_error(message) {
        return {
            success: false,
            data: null,
            error: message,
            timestamp: 1640995200
        };
    }

    success_result = create_success("Operation completed");
    error_result = create_error("Network timeout");

    print("Success: " + string.toString(success_result.success));
    print("Error: " + error_result.error);

    return [success_result, error_result];
}

function test_collection_objects() {
    print("=== Collection Objects ===");

    user_list = {
        items: [],
        count: 0,
        name: "UserCollection"
    };

    // Add users
    user1 = {name: "Alice", role: "admin"};
    user2 = {name: "Bob", role: "user"};

    // Add to collection
    user_list.items = collections.append(user_list.items, user1);
    user_list.count = user_list.count + 1;

    user_list.items = collections.append(user_list.items, user2);
    user_list.count = user_list.count + 1;

    print("User count: " + string.toString(user_list.count));
    print("First user: " + user_list.items[0].name);

    return user_list;
}

// Run tests
test_configuration_objects();
test_result_objects();
test_collection_objects();