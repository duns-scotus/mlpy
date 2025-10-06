"""Python bridge implementations for ML random module.

The random module provides random number generation and sampling utilities.
When imported in ML code as 'import random;', it creates a 'random' object
with methods for generating random numbers and sampling from lists.

Usage in ML:
    import random;

    // Random numbers
    value = random.random();           // Float between 0-1
    dice = random.randomInt(1, 7);     // Integer 1-6
    coin = random.randomBool();        // true/false

    // Sampling
    items = [1, 2, 3, 4, 5];
    picked = random.choice(items);     // Pick one
    shuffled = random.shuffle(items);  // Shuffle list
"""

import math
import random as py_random
from typing import Any
from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="random",
    description="Random number generation and sampling utilities",
    capabilities=["random.generate", "random.sample"],
    version="1.0.0"
)
class Random:
    """Random module interface for ML code.

    This class provides random number generation, boolean generation,
    list sampling, and statistical distributions.
    """

    def __init__(self):
        """Initialize random generator."""
        self._seed = 12345

    @ml_function(description="Set random seed", capabilities=["random.generate"])
    def setSeed(self, seed: int) -> int:
        """Set the random seed for reproducible results.

        Args:
            seed: Seed value for random generator

        Returns:
            The seed value set
        """
        py_random.seed(seed)
        return seed

    @ml_function(description="Get current seed", capabilities=["random.generate"])
    def getSeed(self) -> int:
        """Get current random seed (simplified).

        Returns:
            Current seed value
        """
        return py_random.getstate()[1][0]

    @ml_function(description="Generate random integer", capabilities=["random.generate"])
    def nextInt(self) -> int:
        """Generate next random integer (0 to 2^32-1).

        Returns:
            Random integer
        """
        return py_random.randint(0, 4294967295)  # 2^32 - 1

    @ml_function(description="Generate random float 0-1", capabilities=["random.generate"])
    def random(self) -> float:
        """Generate random float between 0 and 1.

        Returns:
            Random float [0, 1)
        """
        return py_random.random()

    @ml_function(description="Generate random float in range", capabilities=["random.generate"])
    def randomFloat(self, min_val: float = 0, max_val: float = 1) -> float:
        """Generate random float between min and max.

        Args:
            min_val: Minimum value (default 0)
            max_val: Maximum value (default 1)

        Returns:
            Random float in range [min_val, max_val]
        """
        return py_random.uniform(min_val, max_val)

    @ml_function(description="Generate random integer in range", capabilities=["random.generate"])
    def randomInt(self, min_val: int = 0, max_val: int = 100) -> int:
        """Generate random integer between min (inclusive) and max (exclusive).

        Args:
            min_val: Minimum value (inclusive, default 0)
            max_val: Maximum value (exclusive, default 100)

        Returns:
            Random integer in range [min_val, max_val)
        """
        return py_random.randint(min_val, max_val - 1)

    @ml_function(description="Generate random boolean", capabilities=["random.generate"])
    def randomBool(self) -> bool:
        """Generate random boolean (50/50).

        Returns:
            Random boolean value
        """
        return py_random.random() < 0.5

    @ml_function(description="Generate weighted random boolean", capabilities=["random.generate"])
    def randomBoolWeighted(self, probability: float) -> bool:
        """Generate random boolean with given probability of true.

        Args:
            probability: Probability of returning true (0.0 to 1.0)

        Returns:
            Random boolean based on probability
        """
        return py_random.random() < probability

    @ml_function(description="Choose random element", capabilities=["random.sample"])
    def choice(self, lst: list[Any]) -> Any:
        """Choose random element from list.

        Args:
            lst: List to choose from

        Returns:
            Random element from list, or None if empty
        """
        if not lst:
            return None
        return py_random.choice(lst)

    @ml_function(description="Shuffle list", capabilities=["random.sample"])
    def shuffle(self, lst: list[Any]) -> list[Any]:
        """Shuffle list (returns new shuffled list).

        Args:
            lst: List to shuffle

        Returns:
            New shuffled list
        """
        if not lst:
            return []
        shuffled = lst.copy()
        py_random.shuffle(shuffled)
        return shuffled

    @ml_function(description="Random sample from list", capabilities=["random.sample"])
    def sample(self, lst: list[Any], n: int) -> list[Any]:
        """Generate random sample of n elements from list.

        Args:
            lst: List to sample from
            n: Number of elements to sample

        Returns:
            List of n randomly sampled elements
        """
        if not lst:
            return []
        if n >= len(lst):
            return self.shuffle(lst)
        return py_random.sample(lst, n)

    @ml_function(description="Generate normal distribution value", capabilities=["random.generate"])
    def randomNormal(self, mean: float = 0, stddev: float = 1) -> float:
        """Generate random number from normal distribution.

        Args:
            mean: Mean of distribution (default 0)
            stddev: Standard deviation (default 1)

        Returns:
            Random value from normal distribution
        """
        return py_random.normalvariate(mean, stddev)

    @ml_function(description="Generate uniform value", capabilities=["random.generate"])
    def uniform(self, min_val: float, max_val: float) -> float:
        """Generate uniform random value (alias for randomFloat).

        Args:
            min_val: Minimum value
            max_val: Maximum value

        Returns:
            Random value in range
        """
        return self.randomFloat(min_val, max_val)

    @ml_function(description="Generate Gaussian value", capabilities=["random.generate"])
    def gaussian(self, mean: float = 0, stddev: float = 1) -> float:
        """Generate Gaussian random value (alias for randomNormal).

        Args:
            mean: Mean of distribution (default 0)
            stddev: Standard deviation (default 1)

        Returns:
            Random value from Gaussian distribution
        """
        return self.randomNormal(mean, stddev)

    @ml_function(description="Generate triangular distribution value", capabilities=["random.generate"])
    def triangular(self, low: float, high: float, mode: float = None) -> float:
        """Generate random value from triangular distribution.

        Args:
            low: Lower bound
            high: Upper bound
            mode: Mode (peak) of distribution (default is midpoint)

        Returns:
            Random value from triangular distribution
        """
        if mode is None:
            mode = (low + high) / 2.0
        return py_random.triangular(low, high, mode)

    @ml_function(description="Pick random indices", capabilities=["random.sample"])
    def randomIndices(self, length: int, count: int) -> list[int]:
        """Generate random indices for array access.

        Args:
            length: Length of array
            count: Number of indices to generate

        Returns:
            List of random indices
        """
        if count >= length:
            return list(range(length))
        return py_random.sample(range(length), count)

    # Snake_case aliases for convenience
    @ml_function(description="Set seed (snake_case alias)", capabilities=["random.generate"])
    def set_seed(self, seed: int) -> int:
        """Alias for setSeed()."""
        return self.setSeed(seed)

    @ml_function(description="Get seed (snake_case alias)", capabilities=["random.generate"])
    def get_seed(self) -> int:
        """Alias for getSeed()."""
        return self.getSeed()

    @ml_function(description="Next int (snake_case alias)", capabilities=["random.generate"])
    def next_int(self) -> int:
        """Alias for nextInt()."""
        return self.nextInt()

    @ml_function(description="Random float (snake_case alias)", capabilities=["random.generate"])
    def random_float(self, min_val: float = 0, max_val: float = 1) -> float:
        """Alias for randomFloat()."""
        return self.randomFloat(min_val, max_val)

    @ml_function(description="Random int (snake_case alias)", capabilities=["random.generate"])
    def random_int(self, min_val: int = 0, max_val: int = 100) -> int:
        """Alias for randomInt()."""
        return self.randomInt(min_val, max_val)

    @ml_function(description="Random bool (snake_case alias)", capabilities=["random.generate"])
    def random_bool(self) -> bool:
        """Alias for randomBool()."""
        return self.randomBool()

    @ml_function(description="Random normal (snake_case alias)", capabilities=["random.generate"])
    def random_normal(self, mean: float = 0, stddev: float = 1) -> float:
        """Alias for randomNormal()."""
        return self.randomNormal(mean, stddev)

    @ml_function(description="Random indices (snake_case alias)", capabilities=["random.sample"])
    def random_indices(self, length: int, count: int) -> list[int]:
        """Alias for randomIndices()."""
        return self.randomIndices(length, count)


# Global random instance for ML import
# When ML code does 'import random;', this creates the 'random' object
random = Random()


# Additional helper functions for ML bridge
def random_helper() -> float:
    """Helper function for basic random generation."""
    return random.random()


def random_int_helper(min_val: int, max_val: int) -> int:
    """Helper function for random integer generation."""
    return random.randomInt(min_val, max_val)


def choice_helper(lst: list[Any]) -> Any:
    """Helper function for random choice."""
    return random.choice(lst)


# Constants
pi = math.pi


# Export public API
__all__ = [
    "Random",
    "random",
    "random_helper",
    "random_int_helper",
    "choice_helper",
    "pi",
]
