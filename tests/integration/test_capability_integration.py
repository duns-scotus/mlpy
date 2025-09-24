"""Integration tests for the complete capability system."""

import pytest
import tempfile
import os
from pathlib import Path
from src.mlpy.runtime.capabilities import (
    create_capability_token, get_capability_manager,
    CapabilityNotFoundError, requires_capability
)
from src.mlpy.runtime.capabilities.bridge import CallbackBridge
from src.mlpy.runtime.capabilities.manager import file_capability_context
from src.mlpy.runtime.system_modules.file_safe import file_safe
from src.mlpy.runtime.system_modules.math_safe import math_safe


class TestEndToEndCapabilityScenarios:
    """Test complete end-to-end capability scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = get_capability_manager()
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test.txt")
        with open(self.test_file, "w") as f:
            f.write("Test content")

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

    def test_complete_file_processing_workflow(self):
        """Test a complete file processing workflow with capabilities."""
        # Step 1: Create file capabilities
        file_token = create_capability_token(
            capability_type="file",
            resource_patterns=[f"{self.temp_dir}/*.txt"],
            allowed_operations={"read", "write"}
        )

        # Step 2: Process file with capability context
        with self.manager.capability_context("file_processing", [file_token]):
            # Read original content
            content = file_safe.read_text(self.test_file)
            assert content == "Test content"

            # Process content
            processed_content = content.upper()

            # Write processed content
            output_file = os.path.join(self.temp_dir, "output.txt")
            file_safe.write_text(output_file, processed_content)

            # Verify output
            result = file_safe.read_text(output_file)
            assert result == "TEST CONTENT"

    def test_cross_capability_scenario(self):
        """Test scenario requiring multiple different capabilities."""
        # Create multiple capability tokens
        file_token = create_capability_token(
            capability_type="file",
            resource_patterns=[f"{self.temp_dir}/*.txt"],
            allowed_operations={"read", "write"}
        )

        math_token = create_capability_token(
            capability_type="math",
            description="Mathematical operations"
        )

        # Define a function that needs both capabilities
        @requires_capability("math")
        @requires_capability("file")
        def analyze_numeric_file(file_path):
            """Analyze numbers in a file using math operations."""
            content = file_safe.read_text(file_path)
            numbers = [float(x.strip()) for x in content.split(',') if x.strip()]

            # Perform math operations
            total = sum(numbers)
            avg = total / len(numbers) if numbers else 0
            sqrt_avg = math_safe.sqrt(avg) if avg >= 0 else 0

            return {
                "count": len(numbers),
                "total": total,
                "average": avg,
                "sqrt_average": sqrt_avg
            }

        # Create test data file
        data_file = os.path.join(self.temp_dir, "numbers.txt")
        with open(data_file, "w") as f:
            f.write("1.0, 4.0, 9.0, 16.0")

        # Test with both capabilities
        with self.manager.capability_context("analysis", [file_token, math_token]):
            result = analyze_numeric_file(data_file)
            assert result["count"] == 4
            assert result["total"] == 30.0
            assert result["average"] == 7.5
            assert abs(result["sqrt_average"] - 2.738) < 0.01

        # Test failure without math capability
        with self.manager.capability_context("file_only", [file_token]):
            with pytest.raises(CapabilityNotFoundError):
                analyze_numeric_file(data_file)

        # Test failure without file capability
        with self.manager.capability_context("math_only", [math_token]):
            with pytest.raises(CapabilityNotFoundError):
                analyze_numeric_file(data_file)

    def test_bridge_with_capability_forwarding(self):
        """Test bridge communication with capability forwarding."""
        bridge = CallbackBridge()

        # ML side handler that requires file capability
        def ml_file_processor(file_path, operation):
            if operation == "read":
                return file_safe.read_text(file_path)
            elif operation == "exists":
                return file_safe.exists(file_path)
            else:
                raise ValueError(f"Unknown operation: {operation}")

        # System side handler that provides file operations
        def system_file_handler(file_path):
            return f"System accessed: {file_path}"

        bridge.register_ml_handler("file_process", ml_file_processor)
        bridge.register_system_handler("system_file", system_file_handler)
        bridge.start()

        try:
            # Create file capability
            file_token = create_capability_token(
                capability_type="file",
                resource_patterns=[f"{self.temp_dir}/*.txt"],
                allowed_operations={"read"}
            )

            # Test ML function call with capability forwarding
            with self.manager.capability_context("bridge_test", [file_token]):
                result = bridge.call_ml_function(
                    "file_process",
                    {"file_path": self.test_file, "operation": "read"},
                    required_capabilities=["file"]
                )
                assert result == "Test content"

                # Test exists operation
                exists_result = bridge.call_ml_function(
                    "file_process",
                    {"file_path": self.test_file, "operation": "exists"},
                    required_capabilities=["file"]
                )
                assert exists_result == True

            # Test system function call (no capability required)
            system_result = bridge.call_system_function(
                "system_file",
                {"file_path": self.test_file}
            )
            assert "System accessed" in system_result

        finally:
            bridge.stop()

    def test_hierarchical_capability_contexts(self):
        """Test hierarchical capability contexts with inheritance."""
        # Parent capabilities
        parent_file_token = create_capability_token(
            capability_type="file",
            resource_patterns=[f"{self.temp_dir}/public/*.txt"],
            allowed_operations={"read"}
        )

        # Child capabilities (more specific)
        child_file_token = create_capability_token(
            capability_type="file",
            resource_patterns=[f"{self.temp_dir}/public/safe/*.txt"],
            allowed_operations={"read", "write"}
        )

        math_token = create_capability_token(
            capability_type="math",
            description="Math operations"
        )

        # Create directory structure
        public_dir = os.path.join(self.temp_dir, "public")
        safe_dir = os.path.join(public_dir, "safe")
        os.makedirs(safe_dir, exist_ok=True)

        public_file = os.path.join(public_dir, "public.txt")
        safe_file = os.path.join(safe_dir, "safe.txt")

        with open(public_file, "w") as f:
            f.write("Public content")
        with open(safe_file, "w") as f:
            f.write("Safe content")

        # Test hierarchical contexts
        with self.manager.capability_context("parent", [parent_file_token]):
            # Should be able to read public file
            content = file_safe.read_text(public_file)
            assert content == "Public content"

            # Should NOT be able to read safe file (pattern doesn't match)
            with pytest.raises(CapabilityNotFoundError):
                file_safe.read_text(safe_file)

            # Nested context with additional capabilities
            with self.manager.capability_context("child", [child_file_token, math_token]):
                # Should still be able to read public file (inherited)
                content = file_safe.read_text(public_file)
                assert content == "Public content"

                # Should now be able to read safe file (child capability)
                content = file_safe.read_text(safe_file)
                assert content == "Safe content"

                # Should be able to use math operations (child capability)
                result = math_safe.sqrt(16)
                assert result == 4.0

                # Should be able to write to safe file (child capability)
                file_safe.write_text(safe_file, "Modified safe content")

            # After exiting child context, should lose child capabilities
            assert self.manager.has_capability("file")  # Parent capability
            assert not self.manager.has_capability("math")  # Child capability gone

    def test_capability_with_resource_limits(self):
        """Test capabilities with resource limits and constraints."""
        from datetime import datetime, timedelta

        # Create capability with various constraints
        limited_token = create_capability_token(
            capability_type="file",
            resource_patterns=[f"{self.temp_dir}/*.txt"],
            allowed_operations={"read"},
            max_usage_count=3,
            expires_in=timedelta(seconds=60),
            max_file_size=1024  # 1KB limit
        )

        with self.manager.capability_context("limited", [limited_token]):
            # First read should work
            content1 = file_safe.read_text(self.test_file)
            assert content1 == "Test content"

            # Second read should work
            content2 = file_safe.read_text(self.test_file)
            assert content2 == "Test content"

            # Third read should work
            content3 = file_safe.read_text(self.test_file)
            assert content3 == "Test content"

            # Fourth read should fail (usage limit exceeded)
            with pytest.raises(Exception):  # Usage limit error
                file_safe.read_text(self.test_file)

    def test_real_world_data_processing_pipeline(self):
        """Test a realistic data processing pipeline with capabilities."""
        # Create a realistic scenario: CSV data processing

        # Step 1: Create test data
        csv_file = os.path.join(self.temp_dir, "data.csv")
        with open(csv_file, "w") as f:
            f.write("name,age,score\n")
            f.write("Alice,25,85.5\n")
            f.write("Bob,30,92.0\n")
            f.write("Charlie,35,78.5\n")

        output_file = os.path.join(self.temp_dir, "processed.csv")

        # Step 2: Create necessary capabilities
        file_token = create_capability_token(
            capability_type="file",
            resource_patterns=[f"{self.temp_dir}/*.csv"],
            allowed_operations={"read", "write"}
        )

        math_token = create_capability_token(
            capability_type="math",
            description="Statistical calculations"
        )

        # Step 3: Define processing function
        @requires_capability("file")
        @requires_capability("math")
        def process_csv_data(input_file, output_file):
            """Process CSV data with statistical analysis."""
            # Read CSV data
            content = file_safe.read_text(input_file)
            lines = content.strip().split('\n')
            header = lines[0]
            data_lines = lines[1:]

            # Parse data
            records = []
            for line in data_lines:
                parts = line.split(',')
                records.append({
                    'name': parts[0],
                    'age': int(parts[1]),
                    'score': float(parts[2])
                })

            # Calculate statistics
            scores = [r['score'] for r in records]
            ages = [r['age'] for r in records]

            avg_score = sum(scores) / len(scores)
            avg_age = sum(ages) / len(ages)

            # Add computed fields
            for record in records:
                record['score_vs_avg'] = record['score'] - avg_score
                record['age_vs_avg'] = record['age'] - avg_age
                record['performance_rating'] = (
                    "High" if record['score'] > avg_score
                    else "Low"
                )

            # Write processed data
            output_lines = [header + ",score_vs_avg,age_vs_avg,performance_rating"]
            for record in records:
                line = f"{record['name']},{record['age']},{record['score']},"
                line += f"{record['score_vs_avg']:.1f},{record['age_vs_avg']:.1f},"
                line += record['performance_rating']
                output_lines.append(line)

            file_safe.write_text(output_file, '\n'.join(output_lines))

            return {
                'records_processed': len(records),
                'average_score': avg_score,
                'average_age': avg_age
            }

        # Step 4: Execute pipeline with capabilities
        with self.manager.capability_context("data_pipeline", [file_token, math_token]):
            result = process_csv_data(csv_file, output_file)

            assert result['records_processed'] == 3
            assert abs(result['average_score'] - 85.33) < 0.1
            assert abs(result['average_age'] - 30.0) < 0.1

            # Verify output file was created and contains expected data
            output_content = file_safe.read_text(output_file)
            assert "performance_rating" in output_content
            assert "Alice" in output_content
            assert "High" in output_content or "Low" in output_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])