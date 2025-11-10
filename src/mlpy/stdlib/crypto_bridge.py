"""Basic cryptography module for ML.

This module provides basic cryptographic operations including hashing (SHA-256, SHA-1, MD5),
UUID generation, secure random data generation, and HMAC message authentication.

Required Capabilities:
    - crypto.hash: Cryptographic hashing operations
    - crypto.random: Secure random number generation

Example:
    ```ml
    import crypto;

    // Hash data
    hash = crypto.sha256("password123");

    // Generate UUID
    id = crypto.uuid();

    // Secure random
    token = crypto.random_hex(32);
    ```
"""

import hashlib
import hmac
import secrets
import uuid
from typing import Optional

from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="crypto",
    description="Basic cryptographic operations (hashing, UUIDs, secure random)",
    capabilities=["crypto.hash", "crypto.random"],
    version="1.0.0"
)
class Crypto:
    """Cryptographic operations."""

    @ml_function(description="SHA-256 hash", capabilities=["crypto.hash"])
    def sha256(self, data: str, salt: str = "") -> str:
        """Compute SHA-256 hash of string.

        Args:
            data: String to hash
            salt: Optional salt to prepend

        Returns:
            Hex-encoded hash string (64 characters)

        Example:
            ```ml
            hash = crypto.sha256("password123");
            salted = crypto.sha256("password", salt="random_salt");
            ```
        """
        content = (salt + data).encode('utf-8')
        return hashlib.sha256(content).hexdigest()

    @ml_function(description="SHA-1 hash", capabilities=["crypto.hash"])
    def sha1(self, data: str, salt: str = "") -> str:
        """Compute SHA-1 hash of string.

        Args:
            data: String to hash
            salt: Optional salt to prepend

        Returns:
            Hex-encoded hash string (40 characters)

        Example:
            ```ml
            hash = crypto.sha1("data");
            ```
        """
        content = (salt + data).encode('utf-8')
        return hashlib.sha1(content).hexdigest()

    @ml_function(description="MD5 hash", capabilities=["crypto.hash"])
    def md5(self, data: str, salt: str = "") -> str:
        """Compute MD5 hash of string.

        Note: MD5 is not secure for cryptographic purposes. Use for checksums only.

        Args:
            data: String to hash
            salt: Optional salt to prepend

        Returns:
            Hex-encoded hash string (32 characters)

        Example:
            ```ml
            checksum = crypto.md5("file contents");
            ```
        """
        content = (salt + data).encode('utf-8')
        return hashlib.md5(content).hexdigest()

    @ml_function(description="Hash file contents", capabilities=["crypto.hash", "file.read"])
    def hash_file(self, file_path: str, algorithm: str = "sha256") -> str:
        """Hash entire file contents.

        Args:
            file_path: Path to file
            algorithm: Hash algorithm (sha256, sha1, md5)

        Returns:
            Hex-encoded hash

        Example:
            ```ml
            file_hash = crypto.hash_file("document.pdf", algorithm="sha256");
            ```
        """
        hash_func = getattr(hashlib, algorithm)
        hasher = hash_func()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)

        return hasher.hexdigest()

    @ml_function(description="Generate UUID v4", capabilities=["crypto.random"])
    def uuid(self) -> str:
        """Generate random UUID (version 4).

        Returns:
            UUID string (36 characters with hyphens)

        Example:
            ```ml
            id = crypto.uuid();
            // "a7f3d8e2-4b5c-4d9e-8f7a-6b3c2d1e0f9a"
            ```
        """
        return str(uuid.uuid4())

    @ml_function(description="Generate UUID v5 from string", capabilities=["crypto.hash"])
    def uuid_from_string(self, data: str, namespace: Optional[str] = None) -> str:
        """Generate deterministic UUID from string (version 5).

        Args:
            data: Input string
            namespace: UUID namespace (default: DNS namespace)

        Returns:
            UUID string (36 characters with hyphens)

        Example:
            ```ml
            id1 = crypto.uuid_from_string("user@example.com");
            id2 = crypto.uuid_from_string("user@example.com");
            // id1 == id2 (deterministic)
            ```
        """
        ns = uuid.UUID(namespace) if namespace else uuid.NAMESPACE_DNS
        return str(uuid.uuid5(ns, data))

    @ml_function(description="Generate random bytes", capabilities=["crypto.random"])
    def random_bytes(self, length: int) -> bytes:
        """Generate cryptographically secure random bytes.

        Args:
            length: Number of bytes to generate

        Returns:
            Random bytes

        Example:
            ```ml
            token = crypto.random_bytes(32);
            ```
        """
        return secrets.token_bytes(length)

    @ml_function(description="Generate random hex string", capabilities=["crypto.random"])
    def random_hex(self, length: int) -> str:
        """Generate random hex string (2x length characters).

        Args:
            length: Number of random bytes (output will be 2x characters)

        Returns:
            Hex-encoded random string

        Example:
            ```ml
            token = crypto.random_hex(16);  // 32-character hex string
            ```
        """
        return secrets.token_hex(length)

    @ml_function(description="Generate random alphanumeric string", capabilities=["crypto.random"])
    def random_string(self, length: int) -> str:
        """Generate random alphanumeric string [A-Za-z0-9].

        Args:
            length: Number of characters

        Returns:
            Random alphanumeric string

        Example:
            ```ml
            password = crypto.random_string(12);
            ```
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @ml_function(description="Generate secure random integer", capabilities=["crypto.random"])
    def random_int(self, min_val: int, max_val: int) -> int:
        """Generate cryptographically secure random integer in range [min, max].

        Args:
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)

        Returns:
            Random integer in range

        Example:
            ```ml
            dice_roll = crypto.random_int(1, 6);
            ```
        """
        return secrets.randbelow(max_val - min_val + 1) + min_val

    @ml_function(description="Generate secure random float", capabilities=["crypto.random"])
    def random_float(self) -> float:
        """Generate cryptographically secure random float in [0.0, 1.0).

        Returns:
            Random float between 0.0 and 1.0

        Example:
            ```ml
            rand = crypto.random_float();
            ```
        """
        return secrets.randbelow(2**32) / 2**32

    @ml_function(description="Compare hashes securely", capabilities=["crypto.hash"])
    def compare_hash(self, hash1: str, hash2: str) -> bool:
        """Compare two hashes using timing-attack resistant comparison.

        Args:
            hash1: First hash
            hash2: Second hash

        Returns:
            True if hashes match

        Example:
            ```ml
            is_valid = crypto.compare_hash(computed_hash, stored_hash);
            ```
        """
        return hmac.compare_digest(hash1.encode(), hash2.encode())

    @ml_function(description="Generate HMAC signature", capabilities=["crypto.hash"])
    def hmac(self, message: str, key: str, algorithm: str = "sha256") -> str:
        """Generate HMAC signature for message authentication.

        Args:
            message: Message to sign
            key: Secret key
            algorithm: Hash algorithm (sha256, sha1, md5)

        Returns:
            Hex-encoded HMAC signature

        Example:
            ```ml
            signature = crypto.hmac("message", "secret_key");
            ```
        """
        hash_func = getattr(hashlib, algorithm)
        h = hmac.new(key.encode(), message.encode(), hash_func)
        return h.hexdigest()

    @ml_function(description="Verify HMAC signature", capabilities=["crypto.hash"])
    def verify_hmac(self, message: str, signature: str, key: str,
                    algorithm: str = "sha256") -> bool:
        """Verify HMAC signature.

        Args:
            message: Original message
            signature: HMAC signature to verify
            key: Secret key
            algorithm: Hash algorithm

        Returns:
            True if signature is valid

        Example:
            ```ml
            is_valid = crypto.verify_hmac("message", signature, "secret_key");
            ```
        """
        expected = self.hmac(message, key, algorithm)
        return hmac.compare_digest(signature.encode(), expected.encode())


# Create singleton instance for module-level access
crypto = Crypto()
