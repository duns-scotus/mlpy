"""Unit tests for crypto_bridge module."""

import os
import tempfile
import pytest

from mlpy.stdlib.crypto_bridge import Crypto


class TestCryptoModule:
    """Test suite for cryptographic operations."""

    def setup_method(self):
        """Setup for each test method."""
        self.crypto = Crypto()

    def test_sha256_basic(self):
        """Test basic SHA-256 hashing."""
        result = self.crypto.sha256("test_data")
        assert len(result) == 64  # SHA-256 produces 64 hex characters
        assert isinstance(result, str)

    def test_sha256_deterministic(self):
        """Test that SHA-256 is deterministic."""
        hash1 = self.crypto.sha256("test_data")
        hash2 = self.crypto.sha256("test_data")
        assert hash1 == hash2

    def test_sha256_with_salt(self):
        """Test SHA-256 with salt."""
        hash_no_salt = self.crypto.sha256("password")
        hash_with_salt = self.crypto.sha256("password", salt="random_salt")
        assert hash_no_salt != hash_with_salt

    def test_sha256_empty_string(self):
        """Test SHA-256 with empty string."""
        result = self.crypto.sha256("")
        assert len(result) == 64

    def test_sha1_basic(self):
        """Test basic SHA-1 hashing."""
        result = self.crypto.sha1("test_data")
        assert len(result) == 40  # SHA-1 produces 40 hex characters
        assert isinstance(result, str)

    def test_sha1_deterministic(self):
        """Test that SHA-1 is deterministic."""
        hash1 = self.crypto.sha1("test_data")
        hash2 = self.crypto.sha1("test_data")
        assert hash1 == hash2

    def test_md5_basic(self):
        """Test basic MD5 hashing."""
        result = self.crypto.md5("test_data")
        assert len(result) == 32  # MD5 produces 32 hex characters
        assert isinstance(result, str)

    def test_md5_deterministic(self):
        """Test that MD5 is deterministic."""
        hash1 = self.crypto.md5("test_data")
        hash2 = self.crypto.md5("test_data")
        assert hash1 == hash2

    def test_hash_file_sha256(self):
        """Test file hashing with SHA-256."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test file contents")
            temp_path = f.name

        try:
            result = self.crypto.hash_file(temp_path, "sha256")
            assert len(result) == 64
            assert isinstance(result, str)
        finally:
            os.unlink(temp_path)

    def test_hash_file_md5(self):
        """Test file hashing with MD5."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test file contents")
            temp_path = f.name

        try:
            result = self.crypto.hash_file(temp_path, "md5")
            assert len(result) == 32
        finally:
            os.unlink(temp_path)

    def test_hash_file_deterministic(self):
        """Test that file hashing is deterministic."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test file contents")
            temp_path = f.name

        try:
            hash1 = self.crypto.hash_file(temp_path, "sha256")
            hash2 = self.crypto.hash_file(temp_path, "sha256")
            assert hash1 == hash2
        finally:
            os.unlink(temp_path)

    def test_uuid_format(self):
        """Test UUID format."""
        result = self.crypto.uuid()
        assert len(result) == 36  # UUID format: 8-4-4-4-12 with hyphens
        assert result.count('-') == 4

    def test_uuid_uniqueness(self):
        """Test that UUIDs are unique."""
        uuid1 = self.crypto.uuid()
        uuid2 = self.crypto.uuid()
        assert uuid1 != uuid2

    def test_uuid_from_string_deterministic(self):
        """Test that UUID from string is deterministic."""
        uuid1 = self.crypto.uuid_from_string("test@example.com")
        uuid2 = self.crypto.uuid_from_string("test@example.com")
        assert uuid1 == uuid2
        assert len(uuid1) == 36

    def test_uuid_from_string_different_inputs(self):
        """Test that different inputs produce different UUIDs."""
        uuid1 = self.crypto.uuid_from_string("test1@example.com")
        uuid2 = self.crypto.uuid_from_string("test2@example.com")
        assert uuid1 != uuid2

    def test_random_bytes_length(self):
        """Test random bytes generation length."""
        result = self.crypto.random_bytes(32)
        assert len(result) == 32
        assert isinstance(result, bytes)

    def test_random_bytes_uniqueness(self):
        """Test that random bytes are unique."""
        bytes1 = self.crypto.random_bytes(32)
        bytes2 = self.crypto.random_bytes(32)
        assert bytes1 != bytes2

    def test_random_hex_length(self):
        """Test random hex string length."""
        result = self.crypto.random_hex(16)
        assert len(result) == 32  # 16 bytes = 32 hex characters
        assert isinstance(result, str)
        # Check all characters are valid hex
        int(result, 16)  # Should not raise

    def test_random_hex_uniqueness(self):
        """Test that random hex strings are unique."""
        hex1 = self.crypto.random_hex(16)
        hex2 = self.crypto.random_hex(16)
        assert hex1 != hex2

    def test_random_string_length(self):
        """Test random string length."""
        result = self.crypto.random_string(12)
        assert len(result) == 12
        assert isinstance(result, str)

    def test_random_string_alphanumeric(self):
        """Test that random string contains only alphanumeric characters."""
        result = self.crypto.random_string(100)
        assert result.isalnum()

    def test_random_string_uniqueness(self):
        """Test that random strings are unique."""
        str1 = self.crypto.random_string(12)
        str2 = self.crypto.random_string(12)
        assert str1 != str2

    def test_random_int_range(self):
        """Test random integer within range."""
        result = self.crypto.random_int(1, 10)
        assert 1 <= result <= 10
        assert isinstance(result, int)

    def test_random_int_single_value(self):
        """Test random integer with min == max."""
        result = self.crypto.random_int(5, 5)
        assert result == 5

    def test_random_int_negative_range(self):
        """Test random integer with negative range."""
        result = self.crypto.random_int(-10, -1)
        assert -10 <= result <= -1

    def test_random_int_distribution(self):
        """Test that random integers have reasonable distribution."""
        results = [self.crypto.random_int(1, 100) for _ in range(1000)]
        # Check we got different values (not all the same)
        assert len(set(results)) > 10

    def test_random_float_range(self):
        """Test random float range."""
        result = self.crypto.random_float()
        assert 0.0 <= result < 1.0
        assert isinstance(result, float)

    def test_random_float_uniqueness(self):
        """Test that random floats are unique."""
        float1 = self.crypto.random_float()
        float2 = self.crypto.random_float()
        assert float1 != float2

    def test_compare_hash_equal(self):
        """Test hash comparison with equal hashes."""
        hash1 = self.crypto.sha256("password")
        hash2 = self.crypto.sha256("password")
        assert self.crypto.compare_hash(hash1, hash2) is True

    def test_compare_hash_different(self):
        """Test hash comparison with different hashes."""
        hash1 = self.crypto.sha256("password1")
        hash2 = self.crypto.sha256("password2")
        assert self.crypto.compare_hash(hash1, hash2) is False

    def test_compare_hash_timing_resistant(self):
        """Test that hash comparison uses timing-resistant method."""
        # This test verifies the function runs without error
        # Timing resistance is provided by hmac.compare_digest
        hash1 = "a" * 64
        hash2 = "b" * 64
        result = self.crypto.compare_hash(hash1, hash2)
        assert result is False

    def test_hmac_basic(self):
        """Test basic HMAC generation."""
        result = self.crypto.hmac("message", "secret_key")
        assert len(result) == 64  # SHA-256 HMAC
        assert isinstance(result, str)

    def test_hmac_deterministic(self):
        """Test that HMAC is deterministic."""
        hmac1 = self.crypto.hmac("message", "secret_key")
        hmac2 = self.crypto.hmac("message", "secret_key")
        assert hmac1 == hmac2

    def test_hmac_different_keys(self):
        """Test that different keys produce different HMACs."""
        hmac1 = self.crypto.hmac("message", "key1")
        hmac2 = self.crypto.hmac("message", "key2")
        assert hmac1 != hmac2

    def test_hmac_different_messages(self):
        """Test that different messages produce different HMACs."""
        hmac1 = self.crypto.hmac("message1", "key")
        hmac2 = self.crypto.hmac("message2", "key")
        assert hmac1 != hmac2

    def test_hmac_with_sha1(self):
        """Test HMAC with SHA-1 algorithm."""
        result = self.crypto.hmac("message", "key", algorithm="sha1")
        assert len(result) == 40  # SHA-1 HMAC

    def test_verify_hmac_valid(self):
        """Test HMAC verification with valid signature."""
        message = "test message"
        key = "secret_key"
        signature = self.crypto.hmac(message, key)
        assert self.crypto.verify_hmac(message, signature, key) is True

    def test_verify_hmac_invalid_signature(self):
        """Test HMAC verification with invalid signature."""
        message = "test message"
        key = "secret_key"
        signature = self.crypto.hmac(message, key)
        invalid_signature = signature[:-1] + "X"
        assert self.crypto.verify_hmac(message, invalid_signature, key) is False

    def test_verify_hmac_wrong_key(self):
        """Test HMAC verification with wrong key."""
        message = "test message"
        signature = self.crypto.hmac(message, "key1")
        assert self.crypto.verify_hmac(message, signature, "key2") is False

    def test_verify_hmac_wrong_message(self):
        """Test HMAC verification with wrong message."""
        key = "secret_key"
        signature = self.crypto.hmac("message1", key)
        assert self.crypto.verify_hmac("message2", signature, key) is False


class TestCryptoModuleMetadata:
    """Test module metadata and decorators."""

    def test_module_has_metadata(self):
        """Test that module has required metadata."""
        assert hasattr(Crypto, '_ml_module_metadata')
        metadata = Crypto._ml_module_metadata

        assert metadata.name == "crypto"
        assert metadata.description == "Basic cryptographic operations (hashing, UUIDs, secure random)"
        assert "crypto.hash" in metadata.capabilities
        assert "crypto.random" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_function_capabilities(self):
        """Test that functions have correct capability metadata."""
        crypto = Crypto()

        # Hash operations
        assert hasattr(crypto.sha256, '_ml_function_metadata')
        assert "crypto.hash" in crypto.sha256._ml_function_metadata.capabilities

        assert hasattr(crypto.hmac, '_ml_function_metadata')
        assert "crypto.hash" in crypto.hmac._ml_function_metadata.capabilities

        # Random operations
        assert hasattr(crypto.uuid, '_ml_function_metadata')
        assert "crypto.random" in crypto.uuid._ml_function_metadata.capabilities

        assert hasattr(crypto.random_hex, '_ml_function_metadata')
        assert "crypto.random" in crypto.random_hex._ml_function_metadata.capabilities
