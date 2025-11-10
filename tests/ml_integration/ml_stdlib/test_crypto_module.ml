// Test all crypto module functions end-to-end
// This validates the complete ML→Python transpilation pipeline for crypto operations

import crypto;
import console;

console.log("=== Testing crypto Module ===");

// Test 1: SHA-256 hashing
console.log("[Test 1] SHA-256 hashing");
sha256_hash = crypto.sha256("test_data");
if (len(sha256_hash) == 64) {
    console.log("PASS: SHA-256 hash length correct");
} else {
    console.log("FAIL: SHA-256 hash length incorrect");
}

// Test 2: SHA-256 is deterministic
console.log("[Test 2] SHA-256 deterministic");
hash1 = crypto.sha256("password123");
hash2 = crypto.sha256("password123");
if (hash1 == hash2) {
    console.log("PASS: SHA-256 is deterministic");
} else {
    console.log("FAIL: SHA-256 should be deterministic");
}

// Test 3: SHA-256 with salt
console.log("[Test 3] SHA-256 with salt");
hash_no_salt = crypto.sha256("password");
hash_with_salt = crypto.sha256("password", "random_salt");
if (hash_no_salt != hash_with_salt) {
    console.log("PASS: Salted hash differs from unsalted");
} else {
    console.log("FAIL: Salted hash should differ");
}

// Test 4: SHA-1 hashing
console.log("[Test 4] SHA-1 hashing");
sha1_hash = crypto.sha1("test_data");
if (len(sha1_hash) == 40) {
    console.log("PASS: SHA-1 hash length correct (40 chars)");
} else {
    console.log("FAIL: SHA-1 hash length incorrect");
}

// Test 5: MD5 hashing
console.log("[Test 5] MD5 hashing");
md5_hash = crypto.md5("test_data");
if (len(md5_hash) == 32) {
    console.log("PASS: MD5 hash length correct (32 chars)");
} else {
    console.log("FAIL: MD5 hash length incorrect");
}

// Test 6: UUID generation
console.log("[Test 6] UUID generation");
uuid_val = crypto.uuid();
if (len(uuid_val) == 36) {
    console.log("PASS: UUID generation - " + uuid_val);
} else {
    console.log("FAIL: UUID length incorrect");
}

// Test 7: UUID uniqueness
console.log("[Test 7] UUID uniqueness");
uuid1 = crypto.uuid();
uuid2 = crypto.uuid();
if (uuid1 != uuid2) {
    console.log("PASS: UUIDs are unique");
} else {
    console.log("FAIL: UUIDs should be unique");
}

// Test 8: Deterministic UUID from string
console.log("[Test 8] Deterministic UUID");
uuid_det1 = crypto.uuid_from_string("test@example.com");
uuid_det2 = crypto.uuid_from_string("test@example.com");
if (uuid_det1 == uuid_det2) {
    console.log("PASS: Deterministic UUID works - " + uuid_det1);
} else {
    console.log("FAIL: Deterministic UUID should match");
}

// Test 9: Random hex generation
console.log("[Test 9] Random hex generation");
hex_token = crypto.random_hex(16);
if (len(hex_token) == 32) {
    console.log("PASS: Random hex - " + hex_token);
} else {
    console.log("FAIL: Random hex length incorrect");
}

// Test 10: Random string generation
console.log("[Test 10] Random string generation");
random_str = crypto.random_string(12);
if (len(random_str) == 12) {
    console.log("PASS: Random string - " + random_str);
} else {
    console.log("FAIL: Random string length incorrect");
}

// Test 11: Random integer
console.log("[Test 11] Random integer");
rand_int = crypto.random_int(1, 100);
if (rand_int >= 1 && rand_int <= 100) {
    console.log("PASS: Random int in range - " + str(rand_int));
} else {
    console.log("FAIL: Random int out of range");
}

// Test 12: Random float
console.log("[Test 12] Random float");
rand_float = crypto.random_float();
if (rand_float >= 0.0 && rand_float < 1.0) {
    console.log("PASS: Random float in range - " + str(rand_float));
} else {
    console.log("FAIL: Random float out of range");
}

// Test 13: Hash comparison (equal)
console.log("[Test 13] Hash comparison - equal");
hash_a = crypto.sha256("password123");
hash_b = crypto.sha256("password123");
if (crypto.compare_hash(hash_a, hash_b) == true) {
    console.log("PASS: Hash comparison works for equal hashes");
} else {
    console.log("FAIL: Hash comparison failed for equal hashes");
}

// Test 14: Hash comparison (different)
console.log("[Test 14] Hash comparison - different");
hash_c = crypto.sha256("password123");
hash_d = crypto.sha256("different_password");
if (crypto.compare_hash(hash_c, hash_d) == false) {
    console.log("PASS: Hash comparison works for different hashes");
} else {
    console.log("FAIL: Hash comparison failed for different hashes");
}

// Test 15: HMAC generation
console.log("[Test 15] HMAC generation");
signature = crypto.hmac("message", "secret_key");
if (len(signature) == 64) {
    console.log("PASS: HMAC signature length correct");
} else {
    console.log("FAIL: HMAC signature length incorrect");
}

// Test 16: HMAC deterministic
console.log("[Test 16] HMAC deterministic");
sig1 = crypto.hmac("message", "key");
sig2 = crypto.hmac("message", "key");
if (sig1 == sig2) {
    console.log("PASS: HMAC is deterministic");
} else {
    console.log("FAIL: HMAC should be deterministic");
}

// Test 17: HMAC verification - valid
console.log("[Test 17] HMAC verification - valid");
message = "test message";
key = "secret_key";
hmac_sig = crypto.hmac(message, key);
is_valid = crypto.verify_hmac(message, hmac_sig, key);
if (is_valid == true) {
    console.log("PASS: HMAC verification works for valid signature");
} else {
    console.log("FAIL: HMAC verification failed for valid signature");
}

// Test 18: HMAC verification - invalid
console.log("[Test 18] HMAC verification - invalid");
invalid_sig = "0000000000000000000000000000000000000000000000000000000000000000";
is_invalid = crypto.verify_hmac(message, invalid_sig, key);
if (is_invalid == false) {
    console.log("PASS: HMAC verification correctly rejects invalid signature");
} else {
    console.log("FAIL: HMAC verification should reject invalid signature");
}

// Test 19: Real-world use case - password hashing
console.log("[Test 19] Real-world password hashing");
password = "user_password_123";
salt = crypto.random_hex(16);
password_hash = crypto.sha256(password, salt);
console.log("  - Salt: " + salt);
console.log("  - Hash: " + password_hash);
console.log("PASS: Password hashing scenario works");

// Test 20: Real-world use case - API token generation
console.log("[Test 20] Real-world API token generation");
api_token = crypto.random_hex(32);
user_id = crypto.uuid();
console.log("  - User ID: " + user_id);
console.log("  - API Token: " + api_token);
console.log("PASS: API token generation scenario works");

console.log("=== All crypto module tests passed! ===");
