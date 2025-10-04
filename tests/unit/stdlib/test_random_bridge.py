"""Unit tests for random_bridge module migration."""

import pytest
from mlpy.stdlib.random_bridge import Random, random
from mlpy.stdlib.decorators import get_module_metadata, _MODULE_REGISTRY


class TestRandomModuleRegistration:
    """Test that Random module is properly registered with decorators."""

    def test_random_module_registered(self):
        """Test that random module is in global registry."""
        assert "random" in _MODULE_REGISTRY
        assert _MODULE_REGISTRY["random"] == Random

    def test_random_module_metadata(self):
        """Test random module metadata is correct."""
        metadata = get_module_metadata("random")
        assert metadata is not None
        assert metadata.name == "random"
        assert metadata.description == "Random number generation and sampling utilities"
        assert "random.generate" in metadata.capabilities
        assert "random.sample" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_random_has_function_metadata(self):
        """Test that random module has registered functions."""
        metadata = get_module_metadata("random")

        # Check key methods are registered
        assert "setSeed" in metadata.functions
        assert "random" in metadata.functions
        assert "randomInt" in metadata.functions
        assert "randomFloat" in metadata.functions
        assert "randomBool" in metadata.functions
        assert "choice" in metadata.functions
        assert "shuffle" in metadata.functions
        assert "sample" in metadata.functions

        # Should have many functions (20+)
        assert len(metadata.functions) >= 20


class TestRandomSeedManagement:
    """Test random seed management."""

    def test_set_seed(self):
        """Test setSeed() method."""
        result = random.setSeed(42)
        assert result == 42

    def test_get_seed(self):
        """Test getSeed() method."""
        random.setSeed(12345)
        seed = random.getSeed()
        assert isinstance(seed, int)

    def test_seed_reproducibility(self):
        """Test that same seed produces same results."""
        random.setSeed(42)
        val1 = random.random()

        random.setSeed(42)  # Reset with same seed
        val2 = random.random()

        assert val1 == val2


class TestRandomNumberGeneration:
    """Test random number generation methods."""

    def test_next_int(self):
        """Test nextInt() generates integer."""
        value = random.nextInt()
        assert isinstance(value, int)
        assert 0 <= value <= 4294967295

    def test_random_float_range(self):
        """Test random() generates float 0-1."""
        value = random.random()
        assert isinstance(value, float)
        assert 0 <= value < 1

    def test_random_float_custom_range(self):
        """Test randomFloat() with custom range."""
        value = random.randomFloat(10, 20)
        assert isinstance(value, float)
        assert 10 <= value <= 20

    def test_random_int_custom_range(self):
        """Test randomInt() with custom range."""
        value = random.randomInt(1, 7)  # Dice roll
        assert isinstance(value, int)
        assert 1 <= value <= 6  # max is exclusive

    def test_random_int_default_range(self):
        """Test randomInt() with default range."""
        value = random.randomInt()
        assert isinstance(value, int)
        assert 0 <= value < 100


class TestRandomBoolGeneration:
    """Test boolean random generation."""

    def test_random_bool(self):
        """Test randomBool() generates boolean."""
        value = random.randomBool()
        assert isinstance(value, bool)

    def test_random_bool_distribution(self):
        """Test randomBool() has ~50/50 distribution."""
        random.setSeed(42)
        samples = [random.randomBool() for _ in range(1000)]
        true_count = sum(samples)
        # Should be roughly 500 (allow some variance)
        assert 400 < true_count < 600

    def test_random_bool_weighted(self):
        """Test randomBoolWeighted() with probability."""
        # 100% probability
        value = random.randomBoolWeighted(1.0)
        assert value is True

        # 0% probability
        value = random.randomBoolWeighted(0.0)
        assert value is False

        # 75% probability
        random.setSeed(42)
        samples = [random.randomBoolWeighted(0.75) for _ in range(1000)]
        true_count = sum(samples)
        # Should be roughly 750
        assert 700 < true_count < 800


class TestRandomSampling:
    """Test list sampling methods."""

    def test_choice(self):
        """Test choice() picks from list."""
        items = [1, 2, 3, 4, 5]
        value = random.choice(items)
        assert value in items

    def test_choice_empty_list(self):
        """Test choice() with empty list."""
        value = random.choice([])
        assert value is None

    def test_shuffle(self):
        """Test shuffle() returns shuffled list."""
        items = [1, 2, 3, 4, 5]
        shuffled = random.shuffle(items)

        # Should have same elements
        assert sorted(shuffled) == sorted(items)
        # Should be a new list
        assert shuffled is not items
        # Original unchanged
        assert items == [1, 2, 3, 4, 5]

    def test_shuffle_empty_list(self):
        """Test shuffle() with empty list."""
        result = random.shuffle([])
        assert result == []

    def test_sample(self):
        """Test sample() returns random subset."""
        items = [1, 2, 3, 4, 5]
        sampled = random.sample(items, 3)

        assert len(sampled) == 3
        assert all(item in items for item in sampled)
        # Should be unique
        assert len(set(sampled)) == 3

    def test_sample_full_list(self):
        """Test sample() when n >= length."""
        items = [1, 2, 3]
        sampled = random.sample(items, 5)

        # Should return all elements shuffled
        assert sorted(sampled) == sorted(items)

    def test_sample_empty_list(self):
        """Test sample() with empty list."""
        result = random.sample([], 3)
        assert result == []


class TestRandomDistributions:
    """Test statistical distribution methods."""

    def test_random_normal(self):
        """Test randomNormal() generates from normal distribution."""
        value = random.randomNormal(0, 1)
        assert isinstance(value, float)

    def test_random_normal_custom(self):
        """Test randomNormal() with custom mean/stddev."""
        random.setSeed(42)
        values = [random.randomNormal(100, 15) for _ in range(1000)]

        # Mean should be around 100
        mean = sum(values) / len(values)
        assert 95 < mean < 105

    def test_uniform(self):
        """Test uniform() alias."""
        value = random.uniform(5, 15)
        assert isinstance(value, float)
        assert 5 <= value <= 15

    def test_gaussian(self):
        """Test gaussian() alias."""
        value = random.gaussian(10, 2)
        assert isinstance(value, float)


class TestRandomUtilities:
    """Test utility methods."""

    def test_random_indices(self):
        """Test randomIndices() generates random indices."""
        indices = random.randomIndices(10, 5)
        assert len(indices) == 5
        assert all(0 <= idx < 10 for idx in indices)
        # Should be unique
        assert len(set(indices)) == 5

    def test_random_indices_full(self):
        """Test randomIndices() when count >= length."""
        indices = random.randomIndices(5, 10)
        assert len(indices) == 5
        assert sorted(indices) == [0, 1, 2, 3, 4]


class TestRandomSnakeCaseAliases:
    """Test snake_case aliases for methods."""

    def test_set_seed_alias(self):
        """Test set_seed() alias."""
        result = random.set_seed(42)
        assert result == 42

    def test_get_seed_alias(self):
        """Test get_seed() alias."""
        random.set_seed(12345)
        seed = random.get_seed()
        assert isinstance(seed, int)

    def test_next_int_alias(self):
        """Test next_int() alias."""
        value = random.next_int()
        assert isinstance(value, int)

    def test_random_float_alias(self):
        """Test random_float() alias."""
        value = random.random_float(1, 10)
        assert 1 <= value <= 10

    def test_random_int_alias(self):
        """Test random_int() alias."""
        value = random.random_int(1, 10)
        assert 1 <= value < 10

    def test_random_bool_alias(self):
        """Test random_bool() alias."""
        value = random.random_bool()
        assert isinstance(value, bool)

    def test_random_normal_alias(self):
        """Test random_normal() alias."""
        value = random.random_normal(0, 1)
        assert isinstance(value, float)

    def test_random_indices_alias(self):
        """Test random_indices() alias."""
        indices = random.random_indices(10, 3)
        assert len(indices) == 3


class TestRandomInstance:
    """Test global random instance."""

    def test_random_is_instance_of_random_class(self):
        """Test that random is an instance of Random."""
        assert isinstance(random, Random)

    def test_random_has_decorated_methods(self):
        """Test that random instance has decorated methods with metadata."""
        assert hasattr(random, "random")
        assert hasattr(random, "randomInt")
        assert hasattr(random, "choice")

        # Check they have metadata
        assert hasattr(random.random, "_ml_function_metadata")
        assert hasattr(random.randomInt, "_ml_function_metadata")
        assert hasattr(random.choice, "_ml_function_metadata")


class TestRandomHelperFunctions:
    """Test helper functions for ML bridge."""

    def test_random_helper(self):
        """Test random_helper() function."""
        from mlpy.stdlib.random_bridge import random_helper

        value = random_helper()
        assert isinstance(value, float)
        assert 0 <= value < 1

    def test_random_int_helper(self):
        """Test random_int_helper() function."""
        from mlpy.stdlib.random_bridge import random_int_helper

        value = random_int_helper(1, 10)
        assert isinstance(value, int)
        assert 1 <= value < 10

    def test_choice_helper(self):
        """Test choice_helper() function."""
        from mlpy.stdlib.random_bridge import choice_helper

        items = [1, 2, 3]
        value = choice_helper(items)
        assert value in items


class TestRandomConstants:
    """Test module constants."""

    def test_pi_constant(self):
        """Test pi constant is available."""
        from mlpy.stdlib.random_bridge import pi
        import math

        assert pi == math.pi


class TestRandomStatefulBehavior:
    """Test random generator state management."""

    def test_state_affects_generation(self):
        """Test that generator state affects subsequent values."""
        random.setSeed(42)
        val1 = random.random()
        val2 = random.random()
        val3 = random.random()

        # Reset and verify sequence repeats
        random.setSeed(42)
        assert random.random() == val1
        assert random.random() == val2
        assert random.random() == val3

    def test_different_seeds_different_values(self):
        """Test different seeds produce different sequences."""
        random.setSeed(42)
        vals_42 = [random.random() for _ in range(5)]

        random.setSeed(123)
        vals_123 = [random.random() for _ in range(5)]

        # Sequences should be different
        assert vals_42 != vals_123
