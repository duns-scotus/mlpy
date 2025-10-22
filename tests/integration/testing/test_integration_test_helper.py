"""Tests for IntegrationTestHelper class."""

import asyncio
import pytest

from mlpy.integration.testing.test_utilities import IntegrationTestHelper
from mlpy.runtime.capabilities.tokens import CapabilityToken, CapabilityConstraint
from mlpy.runtime.capabilities.exceptions import CapabilityNotFoundError


class TestIntegrationTestHelper:
    """Tests for IntegrationTestHelper."""

    def test_initialization(self):
        """Test helper initializes correctly."""
        helper = IntegrationTestHelper()

        assert len(helper.mock_repl_sessions) == 0
        assert len(helper.captured_async_executions) == 0
        assert len(helper.capability_violations) == 0

    def test_create_test_repl(self):
        """Test creating test REPL session."""
        helper = IntegrationTestHelper()

        session = helper.create_test_repl()

        assert session is not None
        assert len(helper.mock_repl_sessions) == 1
        helper.cleanup()

    def test_create_test_repl_with_capabilities(self):
        """Test creating REPL with capabilities parameter."""
        helper = IntegrationTestHelper()

        constraint = CapabilityConstraint(resource_patterns=["/data/*"])
        file_cap = CapabilityToken(capability_type="file", constraints=constraint)
        session = helper.create_test_repl(capabilities=[file_cap])

        # Verify session is created successfully
        # Note: Capabilities are not enforced in test mode (security_enabled=False)
        assert session is not None
        assert len(helper.mock_repl_sessions) == 1
        helper.cleanup()

    @pytest.mark.anyio
    async def test_assert_async_execution_success(self):
        """Test successful async execution assertion."""
        helper = IntegrationTestHelper()

        # Simple ML code that should work
        await helper.assert_async_execution(
            "result = 2 + 2;",
            expected_result=4
        )

        assert len(helper.captured_async_executions) == 1
        helper.cleanup()

    @pytest.mark.anyio
    async def test_assert_async_execution_mismatch(self):
        """Test async execution with mismatched result."""
        helper = IntegrationTestHelper()

        with pytest.raises(AssertionError, match="Expected 5, got 4"):
            await helper.assert_async_execution(
                "result = 2 + 2;",
                expected_result=5
            )

        helper.cleanup()

    def test_assert_callback_works(self):
        """Test callback assertion."""
        helper = IntegrationTestHelper()

        session = helper.create_test_repl()
        session.execute_ml_line("function double(x) { return x * 2; }")

        helper.assert_callback_works(
            session,
            "double",
            (5,),
            expected_result=10
        )

        helper.cleanup()

    def test_assert_callback_works_mismatch(self):
        """Test callback assertion with mismatched result."""
        helper = IntegrationTestHelper()

        session = helper.create_test_repl()
        session.execute_ml_line("function double(x) { return x * 2; }")

        with pytest.raises(AssertionError, match="Expected 15, got 10"):
            helper.assert_callback_works(
                session,
                "double",
                (5,),
                expected_result=15
            )

        helper.cleanup()

    def test_get_execution_history(self):
        """Test getting execution history."""
        helper = IntegrationTestHelper()

        # Add some executions
        helper.captured_async_executions.append({
            "ml_code": "test",
            "result": "result1",
            "execution_time": "id1"
        })

        history = helper.get_execution_history()

        assert len(history) == 1
        assert history[0]["ml_code"] == "test"
        helper.cleanup()

    def test_get_violation_history(self):
        """Test getting violation history."""
        helper = IntegrationTestHelper()

        # Add a mock violation
        violation = CapabilityNotFoundError("test_cap")
        helper.capability_violations.append(violation)

        history = helper.get_violation_history()

        assert len(history) == 1
        # CapabilityNotFoundError formats as "Capability 'test_cap' not found..."
        assert "test_cap" in str(history[0])
        helper.cleanup()

    def test_cleanup(self):
        """Test cleanup clears state."""
        helper = IntegrationTestHelper()

        # Add some state
        session = helper.create_test_repl()
        helper.captured_async_executions.append({"test": "data"})
        helper.capability_violations.append(CapabilityNotFoundError("test"))

        helper.cleanup()

        assert len(helper.mock_repl_sessions) == 0
        assert len(helper.captured_async_executions) == 0
        assert len(helper.capability_violations) == 0

    def test_reset(self):
        """Test reset is more aggressive than cleanup."""
        helper = IntegrationTestHelper()

        # Add some state
        session = helper.create_test_repl()
        helper.captured_async_executions.append({"test": "data"})

        helper.reset()

        assert len(helper.mock_repl_sessions) == 0
        assert len(helper.captured_async_executions) == 0

    @pytest.mark.anyio
    async def test_multiple_async_executions(self):
        """Test multiple async executions are tracked."""
        helper = IntegrationTestHelper()

        await helper.assert_async_execution("result = 1;", expected_result=1)
        await helper.assert_async_execution("result = 2;", expected_result=2)

        assert len(helper.captured_async_executions) == 2
        helper.cleanup()

    def test_multiple_repl_sessions(self):
        """Test multiple REPL sessions can be created."""
        helper = IntegrationTestHelper()

        session1 = helper.create_test_repl()
        session2 = helper.create_test_repl()

        assert len(helper.mock_repl_sessions) == 2
        assert session1 is not session2
        helper.cleanup()

    def test_callback_with_multiple_args(self):
        """Test callback with multiple arguments."""
        helper = IntegrationTestHelper()

        session = helper.create_test_repl()
        session.execute_ml_line("function add(a, b) { return a + b; }")

        helper.assert_callback_works(
            session,
            "add",
            (3, 7),
            expected_result=10
        )

        helper.cleanup()

    @pytest.mark.anyio
    async def test_execution_time_tracking(self):
        """Test that execution IDs are properly tracked."""
        helper = IntegrationTestHelper()

        await helper.assert_async_execution("result = 1;", expected_result=1)

        assert len(helper.captured_async_executions) == 1
        assert "execution_time" in helper.captured_async_executions[0]
        assert helper.captured_async_executions[0]["execution_time"] is not None

        helper.cleanup()

    @pytest.mark.anyio
    async def test_async_execution_with_timeout(self):
        """Test async execution with custom timeout."""
        helper = IntegrationTestHelper()

        await helper.assert_async_execution(
            "result = 100;",
            expected_result=100,
            timeout=10.0
        )

        assert len(helper.captured_async_executions) == 1
        helper.cleanup()

    def test_context_manager_compatibility(self):
        """Test helper works well as context-like object."""
        helper = IntegrationTestHelper()

        try:
            session = helper.create_test_repl()
            assert session is not None
        finally:
            helper.cleanup()

        assert len(helper.mock_repl_sessions) == 0
