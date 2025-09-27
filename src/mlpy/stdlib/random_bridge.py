"""ML Random Standard Library - Python Implementation."""

import math
import random as py_random
from typing import Any


class Random:
    """ML random operations implemented in Python."""

    def __init__(self):
        self._seed = 12345

    @staticmethod
    def setSeed(seed: int) -> int:
        """Set the random seed."""
        py_random.seed(seed)
        return seed

    @staticmethod
    def getSeed() -> int:
        """Get current seed (simplified - returns current state)."""
        return py_random.getstate()[1][0]

    @staticmethod
    def nextInt() -> int:
        """Generate next random integer."""
        return py_random.randint(0, 4294967295)  # 2^32 - 1

    @staticmethod
    def random() -> float:
        """Generate random float between 0 and 1."""
        return py_random.random()

    @staticmethod
    def randomFloat(min_val: float = 0, max_val: float = 1) -> float:
        """Generate random float between min and max."""
        return py_random.uniform(min_val, max_val)

    @staticmethod
    def randomInt(min_val: int = 0, max_val: int = 100) -> int:
        """Generate random integer between min (inclusive) and max (exclusive)."""
        return py_random.randint(min_val, max_val - 1)

    @staticmethod
    def randomBool() -> bool:
        """Generate random boolean."""
        return py_random.random() < 0.5

    @staticmethod
    def randomBoolWeighted(probability: float) -> bool:
        """Generate random boolean with given probability of true."""
        return py_random.random() < probability

    @staticmethod
    def choice(lst: list[Any]) -> Any:
        """Choose random element from list."""
        if not lst:
            return None
        return py_random.choice(lst)

    @staticmethod
    def shuffle(lst: list[Any]) -> list[Any]:
        """Shuffle list (returns new shuffled list)."""
        if not lst:
            return []
        shuffled = lst.copy()
        py_random.shuffle(shuffled)
        return shuffled

    @staticmethod
    def sample(lst: list[Any], n: int) -> list[Any]:
        """Generate random sample of n elements from list."""
        if not lst:
            return []
        if n >= len(lst):
            return Random.shuffle(lst)
        return py_random.sample(lst, n)

    @staticmethod
    def randomNormal(mean: float = 0, stddev: float = 1) -> float:
        """Generate random number from normal distribution."""
        return py_random.normalvariate(mean, stddev)

    # Math helper functions for ML compatibility
    @staticmethod
    def ln(x: float) -> float:
        """Natural logarithm."""
        if x <= 0:
            return -999  # Error case as in ML version
        return math.log(x)

    @staticmethod
    def sin(x: float) -> float:
        """Sine function."""
        return math.sin(x)

    @staticmethod
    def cos(x: float) -> float:
        """Cosine function."""
        return math.cos(x)

    @staticmethod
    def sqrt(x: float) -> float:
        """Square root function."""
        if x < 0:
            return 0  # Error case as in ML version
        return math.sqrt(x)

    @staticmethod
    def abs(x: float) -> float:
        """Absolute value function."""
        return abs(x)

    @staticmethod
    def length(lst: list[Any]) -> int:
        """Get length of list."""
        return len(lst) if lst is not None else 0


# Global random instance for ML programs
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
