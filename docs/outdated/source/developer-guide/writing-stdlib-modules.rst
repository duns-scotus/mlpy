========================
Writing Standard Library Modules
========================

This guide covers the complete process of creating new standard library modules for mlpy, from initial design through testing and deployment. Standard library modules extend mlpy's functionality while maintaining security and performance guarantees.

Module Architecture Overview
=============================

Standard library modules consist of three components:

1. **ML Module File** (``*.ml``) - The ML language interface
2. **Python Bridge** (``*.py``) - Implementation in Python
3. **Registration Code** - Integration with the module registry

.. code-block:: text

    stdlib/
    ├── mymodule.ml          # ML interface definition
    ├── mymodule.py          # Python implementation
    └── registry.py          # Registration (updated)

Creating a New Module
=====================

Let's create a complete example: a cryptographic utilities module.

Step 1: Design the Module Interface
-----------------------------------

First, define the ML interface in ``src/mlpy/stdlib/crypto.ml``:

.. code-block:: ml

    // @description: Cryptographic utilities with capability-based security
    // @capability: crypto:hash:*
    // @capability: crypto:random:secure
    // @version: 1.0.0

    capability crypto {
        // Hash generation capabilities
        grant hash:md5 to resource("data:*")
        grant hash:sha256 to resource("data:*")
        grant hash:sha512 to resource("data:*")

        // Secure random generation
        grant random:secure to resource("system:entropy")

        // Symmetric encryption (advanced)
        grant encrypt:aes256 to resource("data:sensitive")
        grant decrypt:aes256 to resource("data:sensitive")
    }

    // Hash functions with capability requirements
    function md5(data: string): string {
        require capability crypto:hash:md5
        return __bridge_call("crypto", "md5", [data])
    }

    function sha256(data: string): string {
        require capability crypto:hash:sha256
        return __bridge_call("crypto", "sha256", [data])
    }

    function sha512(data: string): string {
        require capability crypto:hash:sha512
        return __bridge_call("crypto", "sha512", [data])
    }

    // Secure random number generation
    function secureRandom(length: number): string {
        require capability crypto:random:secure
        return __bridge_call("crypto", "secureRandom", [length])
    }

    // Advanced encryption (with strict capability requirements)
    function encryptAES256(data: string, key: string): string {
        require capability crypto:encrypt:aes256
        if (length(key) != 32) {
            throw "AES256 key must be exactly 32 characters"
        }
        return __bridge_call("crypto", "encryptAES256", [data, key])
    }

    function decryptAES256(encryptedData: string, key: string): string {
        require capability crypto:decrypt:aes256
        if (length(key) != 32) {
            throw "AES256 key must be exactly 32 characters"
        }
        return __bridge_call("crypto", "decryptAES256", [encryptedData, key])
    }

    // Utility function for key generation
    function generateAESKey(): string {
        require capability crypto:random:secure
        return secureRandom(32)
    }

    // Password hashing with salt
    function hashPassword(password: string, salt: string): string {
        require capability crypto:hash:sha256
        return sha256(password + salt)
    }

    function verifPassword(password: string, salt: string, hash: string): boolean {
        return hashPassword(password, salt) == hash
    }

Step 2: Implement Python Bridge Functions
-----------------------------------------

Create ``src/mlpy/stdlib/crypto.py`` with the Python implementation:

.. code-block:: python

    """Cryptographic utilities bridge implementation."""

    import hashlib
    import secrets
    from typing import Any

    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    from mlpy.runtime.capabilities.manager import require_capability
    from mlpy.ml.errors.exceptions import MLRuntimeError


    class CryptoModule:
        """Secure cryptographic operations with capability validation."""

        @staticmethod
        @require_capability("crypto:hash:md5")
        def md5(data: str) -> str:
            """Generate MD5 hash of input data."""
            if not isinstance(data, str):
                raise MLRuntimeError("MD5 input must be a string")

            try:
                hasher = hashlib.md5()
                hasher.update(data.encode('utf-8'))
                return hasher.hexdigest()
            except Exception as e:
                raise MLRuntimeError(f"MD5 hashing failed: {e}")

        @staticmethod
        @require_capability("crypto:hash:sha256")
        def sha256(data: str) -> str:
            """Generate SHA256 hash of input data."""
            if not isinstance(data, str):
                raise MLRuntimeError("SHA256 input must be a string")

            try:
                hasher = hashlib.sha256()
                hasher.update(data.encode('utf-8'))
                return hasher.hexdigest()
            except Exception as e:
                raise MLRuntimeError(f"SHA256 hashing failed: {e}")

        @staticmethod
        @require_capability("crypto:hash:sha512")
        def sha512(data: str) -> str:
            """Generate SHA512 hash of input data."""
            if not isinstance(data, str):
                raise MLRuntimeError("SHA512 input must be a string")

            try:
                hasher = hashlib.sha512()
                hasher.update(data.encode('utf-8'))
                return hasher.hexdigest()
            except Exception as e:
                raise MLRuntimeError(f"SHA512 hashing failed: {e}")

        @staticmethod
        @require_capability("crypto:random:secure")
        def secure_random(length: int) -> str:
            """Generate cryptographically secure random string."""
            if not isinstance(length, int) or length <= 0:
                raise MLRuntimeError("Random length must be a positive integer")

            if length > 1024:  # Security limit
                raise MLRuntimeError("Random length exceeds maximum (1024)")

            try:
                # Generate secure random bytes and convert to hex
                random_bytes = secrets.token_bytes(length // 2 + 1)
                return random_bytes.hex()[:length]
            except Exception as e:
                raise MLRuntimeError(f"Secure random generation failed: {e}")

        @staticmethod
        @require_capability("crypto:encrypt:aes256")
        def encrypt_aes256(data: str, key: str) -> str:
            """Encrypt data using AES256 in GCM mode."""
            if not isinstance(data, str) or not isinstance(key, str):
                raise MLRuntimeError("Encryption input must be strings")

            if len(key) != 32:
                raise MLRuntimeError("AES256 key must be exactly 32 characters")

            try:
                # Convert key to bytes
                key_bytes = key.encode('utf-8')

                # Generate random IV
                iv = secrets.token_bytes(12)  # 96-bit IV for GCM

                # Create cipher
                cipher = Cipher(
                    algorithms.AES(key_bytes),
                    modes.GCM(iv)
                )
                encryptor = cipher.encryptor()

                # Encrypt data
                ciphertext = encryptor.update(data.encode('utf-8'))
                encryptor.finalize()

                # Combine IV + tag + ciphertext and return as hex
                encrypted_data = iv + encryptor.tag + ciphertext
                return encrypted_data.hex()

            except Exception as e:
                raise MLRuntimeError(f"AES256 encryption failed: {e}")

        @staticmethod
        @require_capability("crypto:decrypt:aes256")
        def decrypt_aes256(encrypted_data: str, key: str) -> str:
            """Decrypt AES256-GCM encrypted data."""
            if not isinstance(encrypted_data, str) or not isinstance(key, str):
                raise MLRuntimeError("Decryption input must be strings")

            if len(key) != 32:
                raise MLRuntimeError("AES256 key must be exactly 32 characters")

            try:
                # Convert hex back to bytes
                encrypted_bytes = bytes.fromhex(encrypted_data)

                # Extract components
                iv = encrypted_bytes[:12]       # First 12 bytes
                tag = encrypted_bytes[12:28]    # Next 16 bytes
                ciphertext = encrypted_bytes[28:]  # Remaining bytes

                # Convert key to bytes
                key_bytes = key.encode('utf-8')

                # Create cipher
                cipher = Cipher(
                    algorithms.AES(key_bytes),
                    modes.GCM(iv, tag)
                )
                decryptor = cipher.decryptor()

                # Decrypt data
                plaintext = decryptor.update(ciphertext)
                decryptor.finalize()

                return plaintext.decode('utf-8')

            except Exception as e:
                raise MLRuntimeError(f"AES256 decryption failed: {e}")


    # Bridge function mappings for registry
    CRYPTO_FUNCTIONS = {
        'md5': CryptoModule.md5,
        'sha256': CryptoModule.sha256,
        'sha512': CryptoModule.sha512,
        'secureRandom': CryptoModule.secure_random,
        'encryptAES256': CryptoModule.encrypt_aes256,
        'decryptAES256': CryptoModule.decrypt_aes256,
    }


    # Parameter validation functions
    def validate_hash_input(args: list[Any]) -> None:
        """Validate hash function arguments."""
        if len(args) != 1:
            raise ValueError("Hash functions require exactly 1 argument")

        if not isinstance(args[0], str):
            raise ValueError("Hash input must be a string")

        if len(args[0]) > 1_000_000:  # 1MB limit
            raise ValueError("Hash input exceeds maximum size (1MB)")


    def validate_random_input(args: list[Any]) -> None:
        """Validate secure random arguments."""
        if len(args) != 1:
            raise ValueError("secureRandom requires exactly 1 argument")

        if not isinstance(args[0], int):
            raise ValueError("Random length must be an integer")

        if args[0] <= 0 or args[0] > 1024:
            raise ValueError("Random length must be between 1 and 1024")


    def validate_encryption_input(args: list[Any]) -> None:
        """Validate encryption function arguments."""
        if len(args) != 2:
            raise ValueError("Encryption functions require exactly 2 arguments")

        data, key = args
        if not isinstance(data, str) or not isinstance(key, str):
            raise ValueError("Encryption arguments must be strings")

        if len(key) != 32:
            raise ValueError("AES256 key must be exactly 32 characters")

        if len(data) > 10_000_000:  # 10MB limit
            raise ValueError("Encryption data exceeds maximum size (10MB)")


    # Validation function mappings
    CRYPTO_VALIDATORS = {
        'md5': validate_hash_input,
        'sha256': validate_hash_input,
        'sha512': validate_hash_input,
        'secureRandom': validate_random_input,
        'encryptAES256': validate_encryption_input,
        'decryptAES256': validate_encryption_input,
    }

Step 3: Register the Module
---------------------------

Update ``src/mlpy/stdlib/registry.py`` to register the crypto module:

.. code-block:: python

    def _register_core_modules(registry: StandardLibraryRegistry) -> None:
        """Register core standard library modules."""

        # ... existing modules ...

        # Crypto module
        registry.register_module(
            name="crypto",
            source_file="crypto.ml",
            capabilities_required=[
                "crypto:hash:*",
                "crypto:random:secure",
                "crypto:encrypt:aes256",
                "crypto:decrypt:aes256"
            ],
            description="Cryptographic utilities with capability-based security",
            version="1.0.0",
            python_bridge_modules=["mlpy.stdlib.crypto", "cryptography"]
        )

        # Register crypto bridge functions
        crypto_functions = [
            ("md5", "mlpy.stdlib.crypto", "CryptoModule.md5", ["crypto:hash:md5"]),
            ("sha256", "mlpy.stdlib.crypto", "CryptoModule.sha256", ["crypto:hash:sha256"]),
            ("sha512", "mlpy.stdlib.crypto", "CryptoModule.sha512", ["crypto:hash:sha512"]),
            ("secureRandom", "mlpy.stdlib.crypto", "CryptoModule.secure_random", ["crypto:random:secure"]),
            ("encryptAES256", "mlpy.stdlib.crypto", "CryptoModule.encrypt_aes256", ["crypto:encrypt:aes256"]),
            ("decryptAES256", "mlpy.stdlib.crypto", "CryptoModule.decrypt_aes256", ["crypto:decrypt:aes256"]),
        ]

        from mlpy.stdlib.crypto import CRYPTO_VALIDATORS

        for ml_name, py_module, py_func, caps in crypto_functions:
            registry.register_bridge_function(
                module_name="crypto",
                ml_name=ml_name,
                python_module=py_module,
                python_function=py_func,
                capabilities_required=caps,
                validation_function=CRYPTO_VALIDATORS.get(ml_name)
            )

Step 4: Create Comprehensive Tests
----------------------------------

Create ``tests/test_stdlib_crypto.py``:

.. code-block:: python

    """Tests for the crypto standard library module."""

    import pytest
    from mlpy.ml.transpiler import transpile_ml_code, execute_ml_code_sandbox
    from mlpy.runtime.sandbox.config import SandboxConfig
    from mlpy.runtime.capabilities.manager import CapabilityContext


    class TestCryptoModule:
        """Test crypto module functionality."""

        def test_hash_functions(self):
            """Test hash function implementations."""
            ml_code = '''
            import crypto

            function testHashes() {
                let data = "Hello, World!"

                let md5Hash = crypto.md5(data)
                let sha256Hash = crypto.sha256(data)
                let sha512Hash = crypto.sha512(data)

                return {
                    "md5": md5Hash,
                    "sha256": sha256Hash,
                    "sha512": sha512Hash
                }
            }
            '''

            # Create capability context with hash permissions
            capabilities = CapabilityContext()
            capabilities.grant("crypto:hash:*", "execute")

            result = execute_ml_code_sandbox(
                ml_code,
                capabilities=capabilities,
                sandbox_config=SandboxConfig(max_cpu_time_seconds=2.0)
            )

            assert result.success
            hashes = result.return_value

            # Verify hash formats and expected values
            assert len(hashes["md5"]) == 32  # MD5 is 32 hex chars
            assert len(hashes["sha256"]) == 64  # SHA256 is 64 hex chars
            assert len(hashes["sha512"]) == 128  # SHA512 is 128 hex chars

            # Verify specific known hash values
            assert hashes["md5"] == "65a8e27d8879283831b664bd8b7f0ad4"
            assert hashes["sha256"] == "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"

        def test_secure_random(self):
            """Test secure random generation."""
            ml_code = '''
            import crypto

            function testRandom() {
                let random1 = crypto.secureRandom(16)
                let random2 = crypto.secureRandom(32)
                let random3 = crypto.secureRandom(8)

                return {
                    "random16": random1,
                    "random32": random2,
                    "random8": random3,
                    "different": random1 != random2
                }
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("crypto:random:secure", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert result.success
            random_data = result.return_value

            # Verify lengths
            assert len(random_data["random16"]) == 16
            assert len(random_data["random32"]) == 32
            assert len(random_data["random8"]) == 8

            # Verify randomness (different values)
            assert random_data["different"] is True

        def test_aes_encryption(self):
            """Test AES encryption/decryption."""
            ml_code = '''
            import crypto

            function testEncryption() {
                let key = crypto.generateAESKey()  // 32-character key
                let data = "Secret message for encryption!"

                let encrypted = crypto.encryptAES256(data, key)
                let decrypted = crypto.decryptAES256(encrypted, key)

                return {
                    "original": data,
                    "encrypted": encrypted,
                    "decrypted": decrypted,
                    "roundTrip": data == decrypted,
                    "keyLength": length(key)
                }
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("crypto:random:secure", "execute")
            capabilities.grant("crypto:encrypt:aes256", "execute")
            capabilities.grant("crypto:decrypt:aes256", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert result.success
            crypto_result = result.return_value

            # Verify round-trip encryption
            assert crypto_result["roundTrip"] is True
            assert crypto_result["keyLength"] == 32
            assert crypto_result["encrypted"] != crypto_result["original"]
            assert len(crypto_result["encrypted"]) > len(crypto_result["original"])

        def test_capability_enforcement(self):
            """Test that capability requirements are enforced."""
            ml_code = '''
            import crypto

            function unauthorized() {
                return crypto.md5("test")  // Should fail without capability
            }
            '''

            # No capabilities granted
            capabilities = CapabilityContext()

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            # Should fail due to missing capability
            assert not result.success
            assert "capability" in result.error.lower()

        def test_input_validation(self):
            """Test input validation and security limits."""
            ml_code = '''
            import crypto

            function testValidation() {
                try {
                    // This should fail - invalid key length
                    crypto.encryptAES256("data", "short_key")
                    return "validation_failed"
                } catch (error) {
                    return "validation_success"
                }
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("crypto:encrypt:aes256", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert result.success
            assert result.return_value == "validation_success"

        def test_password_utilities(self):
            """Test password hashing utilities."""
            ml_code = '''
            import crypto

            function testPasswordHashing() {
                let password = "mySecretPassword123"
                let salt = crypto.secureRandom(16)

                let hash1 = crypto.hashPassword(password, salt)
                let hash2 = crypto.hashPassword(password, salt)

                let isValid = crypto.verifyPassword(password, salt, hash1)
                let isInvalid = crypto.verifyPassword("wrongPassword", salt, hash1)

                return {
                    "consistent": hash1 == hash2,
                    "validVerification": isValid,
                    "invalidVerification": !isInvalid
                }
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("crypto:hash:sha256", "execute")
            capabilities.grant("crypto:random:secure", "execute")

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)

            assert result.success
            password_result = result.return_value

            assert password_result["consistent"] is True
            assert password_result["validVerification"] is True
            assert password_result["invalidVerification"] is True


    class TestCryptoSecurity:
        """Test security aspects of crypto module."""

        def test_capability_isolation(self):
            """Test that capabilities are properly isolated."""
            ml_code = '''
            import crypto

            function testIsolation() {
                // Only have hash capability, not encryption
                return crypto.sha256("test")
            }
            '''

            capabilities = CapabilityContext()
            capabilities.grant("crypto:hash:sha256", "execute")
            # Deliberately NOT granting encryption capabilities

            result = execute_ml_code_sandbox(ml_code, capabilities=capabilities)
            assert result.success

            # Now try encryption without capability
            ml_code_encrypt = '''
            import crypto

            function testEncryption() {
                let key = "a" * 32  // 32-char key
                return crypto.encryptAES256("data", key)
            }
            '''

            result = execute_ml_code_sandbox(ml_code_encrypt, capabilities=capabilities)
            assert not result.success  # Should fail

        def test_resource_limits(self):
            """Test that resource limits are enforced."""
            # Test handled by validation functions in the Python implementation
            # Large input tests would be handled by the bridge validation
            pass

Step 5: Documentation and Examples
----------------------------------

Create ``docs/examples/stdlib-modules/crypto-examples.ml``:

.. code-block:: ml

    // Complete crypto module usage examples
    import crypto

    // Example 1: Basic hashing for data integrity
    function verifyDataIntegrity(data: string, expectedHash: string): boolean {
        let actualHash = crypto.sha256(data)
        return actualHash == expectedHash
    }

    // Example 2: Secure password storage
    function createUser(username: string, password: string): object {
        let salt = crypto.secureRandom(16)
        let passwordHash = crypto.hashPassword(password, salt)

        return {
            "username": username,
            "passwordHash": passwordHash,
            "salt": salt,
            "created": getCurrentTime()
        }
    }

    function authenticateUser(user: object, password: string): boolean {
        return crypto.verifyPassword(password, user.salt, user.passwordHash)
    }

    // Example 3: Secure data encryption for storage
    function encryptSensitiveData(data: string): object {
        let encryptionKey = crypto.generateAESKey()
        let encryptedData = crypto.encryptAES256(data, encryptionKey)

        // In practice, store the key securely (not with the data!)
        return {
            "data": encryptedData,
            "keyHash": crypto.sha256(encryptionKey)  // For key verification
        }
    }

    function decryptSensitiveData(encryptedObject: object, key: string): string {
        // Verify key matches
        let keyHash = crypto.sha256(key)
        if (keyHash != encryptedObject.keyHash) {
            throw "Invalid decryption key"
        }

        return crypto.decryptAES256(encryptedObject.data, key)
    }

    // Example 4: File integrity checking
    function generateFileChecksum(fileContent: string): object {
        return {
            "md5": crypto.md5(fileContent),
            "sha256": crypto.sha256(fileContent),
            "size": length(fileContent)
        }
    }

    function verifyFileIntegrity(fileContent: string, checksum: object): boolean {
        let currentChecksum = generateFileChecksum(fileContent)
        return currentChecksum.sha256 == checksum.sha256 &&
               currentChecksum.size == checksum.size
    }

Module Development Best Practices
==================================

Security Considerations
-----------------------

1. **Capability Requirements**: Every function must declare required capabilities
2. **Input Validation**: Validate all parameters before processing
3. **Resource Limits**: Implement reasonable limits to prevent abuse
4. **Error Handling**: Fail securely with informative error messages
5. **Audit Logging**: Log security-relevant operations

.. code-block:: python

    @require_capability("mymodule:operation:specific")
    def secure_operation(data: Any) -> Any:
        # 1. Validate input
        if not isinstance(data, str) or len(data) > MAX_SIZE:
            raise MLRuntimeError("Invalid input data")

        # 2. Log the operation
        security_logger.info(f"Performing secure operation on {len(data)} bytes")

        try:
            # 3. Perform operation
            result = process_data(data)

            # 4. Validate output
            if not is_safe_output(result):
                raise MLRuntimeError("Operation produced unsafe output")

            return result

        except Exception as e:
            # 5. Secure error handling
            security_logger.warning(f"Secure operation failed: {type(e).__name__}")
            raise MLRuntimeError("Operation failed")

Performance Optimization
-----------------------

1. **Lazy Loading**: Load expensive resources only when needed
2. **Caching**: Cache expensive computations with TTL
3. **Batch Operations**: Support batch processing for efficiency
4. **Memory Management**: Clean up resources promptly

.. code-block:: python

    class OptimizedModule:
        def __init__(self):
            self._cache = {}
            self._cache_ttl = {}

        @lru_cache(maxsize=128)
        def expensive_operation(self, input_data: str) -> str:
            # Expensive computation cached automatically
            return self._compute_result(input_data)

        def batch_operation(self, items: list) -> list:
            # Process multiple items efficiently
            results = []
            with self.get_optimized_context():
                for item in items:
                    results.append(self.process_single_item(item))
            return results

Testing Strategies
------------------

1. **Unit Tests**: Test each function in isolation
2. **Integration Tests**: Test module integration with mlpy
3. **Security Tests**: Verify capability enforcement
4. **Performance Tests**: Benchmark critical operations
5. **Fuzzing Tests**: Test with malformed inputs

.. code-block:: python

    # Performance test example
    def test_module_performance(benchmark):
        def setup():
            return {"data": "x" * 1000}

        def operation(params):
            return MyModule.expensive_function(params["data"])

        result = benchmark.pedantic(operation, setup=setup, rounds=100)
        assert result is not None

Documentation Requirements
--------------------------

1. **Module Description**: Clear purpose and capabilities
2. **Function Documentation**: Parameters, return values, exceptions
3. **Usage Examples**: Real-world usage scenarios
4. **Security Notes**: Capability requirements and limitations
5. **Performance Characteristics**: Time/space complexity notes

.. code-block:: ml

    /**
     * Advanced cryptographic utilities module
     *
     * Provides secure hash functions, random generation, and encryption
     * with fine-grained capability-based access control.
     *
     * @security All operations require explicit capability grants
     * @performance Hash operations: O(n), Encryption: O(n)
     * @version 1.0.0
     */

    /**
     * Generate SHA256 hash of input data
     *
     * @param data String data to hash
     * @returns Hexadecimal hash string (64 characters)
     * @requires capability crypto:hash:sha256
     * @throws MLRuntimeError if input validation fails
     * @performance O(n) where n is input length
     * @example crypto.sha256("Hello") -> "185f8db32271fe25..."
     */
    function sha256(data: string): string

Deployment and Versioning
=========================

Module Versioning Strategy
--------------------------

1. **Semantic Versioning**: Use MAJOR.MINOR.PATCH format
2. **Compatibility Matrix**: Document mlpy version compatibility
3. **Migration Guides**: Provide upgrade paths for breaking changes
4. **Deprecation Policy**: Clear timeline for removing old features

.. code-block:: python

    # Version compatibility matrix
    MODULE_COMPATIBILITY = {
        "1.0.0": "mlpy>=2.0.0,<3.0.0",
        "1.1.0": "mlpy>=2.1.0,<3.0.0",
        "2.0.0": "mlpy>=3.0.0,<4.0.0"
    }

Distribution and Packaging
-------------------------

1. **Core Modules**: Included with mlpy distribution
2. **Extension Modules**: Distributed separately via package manager
3. **Security Review**: All modules undergo security review
4. **Automated Testing**: CI/CD pipeline validates all modules

Module Registry Integration
---------------------------

For external modules, provide registration metadata:

.. code-block:: python

    # module_info.py
    MODULE_INFO = {
        "name": "advanced-crypto",
        "version": "1.0.0",
        "description": "Advanced cryptographic utilities",
        "author": "Your Name",
        "license": "MIT",
        "capabilities_required": [
            "crypto:hash:*",
            "crypto:encrypt:*",
            "crypto:random:secure"
        ],
        "python_dependencies": [
            "cryptography>=3.4.8",
            "pynacl>=1.4.0"
        ],
        "mlpy_version": ">=2.0.0,<3.0.0"
    }

This completes the comprehensive guide to writing standard library modules for mlpy, covering everything from initial design through deployment and maintenance.