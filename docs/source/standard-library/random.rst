random - Random Number Generation
===================================

.. module:: random
   :synopsis: Random number generation and sampling

The ``random`` module provides comprehensive random number generation, including uniform and statistical distributions, list sampling, and reproducible sequences through seeding.

Philosophy: Controlled Randomness
----------------------------------

True randomness is impossible in deterministic systems, but pseudo-random number generators provide:

- **Unpredictability**: Sequences appear random for practical purposes
- **Reproducibility**: Same seed produces same sequence (critical for testing)
- **Statistical Properties**: Distributions match mathematical models
- **Practical Applications**: Simulations, games, sampling, testing

This module balances true randomness with reproducible testing needs.

Seeding and Reproducibility
----------------------------

setSeed()
~~~~~~~~~

.. code-block:: ml

   setSeed(seed) -> number

Set random seed for reproducible sequences.

**Parameters:**

- ``seed``: Integer seed value

**Returns:** The seed value set

**Example:**

.. code-block:: ml

   import random;

   // Set seed for reproducible results
   random.setSeed(42);

   // Generate sequence
   values = [];
   i = 0;
   while (i < 5) {
       values = values + [random.randomInt(1, 100)];
       i = i + 1;
   }

   // Same seed produces same sequence
   random.setSeed(42);
   values2 = [];  // Will match values

getSeed()
~~~~~~~~~

.. code-block:: ml

   getSeed() -> number

Get current random seed value.

**Returns:** Current seed

**Example:**

.. code-block:: ml

   import random;

   currentSeed = random.getSeed();
   console.log("Current seed: " + str(currentSeed));

nextInt()
~~~~~~~~~

.. code-block:: ml

   nextInt() -> number

Generate next random integer in sequence (0 to 2^32-1).

**Returns:** Random 32-bit integer

**Example:**

.. code-block:: ml

   import random;

   largeNumber = random.nextInt();
   // Result: e.g., 2147483647

Basic Random Generation
-----------------------

random()
~~~~~~~~

.. code-block:: ml

   random() -> number

Generate random float between 0 and 1.

**Returns:** Random float in range [0, 1)

**Example:**

.. code-block:: ml

   import random;

   value = random.random();
   // Result: e.g., 0.7231

randomFloat()
~~~~~~~~~~~~~

.. code-block:: ml

   randomFloat(min, max) -> number

Generate random float in specified range.

**Parameters:**

- ``min``: Minimum value (default 0)
- ``max``: Maximum value (default 1)

**Returns:** Random float in range [min, max]

**Example:**

.. code-block:: ml

   import random;

   temperature = random.randomFloat(15, 30);
   // Result: e.g., 22.5 degrees

randomInt()
~~~~~~~~~~~

.. code-block:: ml

   randomInt(min, max) -> number

Generate random integer in range.

**Parameters:**

- ``min``: Minimum value (inclusive, default 0)
- ``max``: Maximum value (exclusive, default 100)

**Returns:** Random integer in range [min, max)

**Example:**

.. code-block:: ml

   import random;

   diceRoll = random.randomInt(1, 7);
   // Result: 1, 2, 3, 4, 5, or 6

randomBool()
~~~~~~~~~~~~

.. code-block:: ml

   randomBool() -> boolean

Generate random boolean (50/50 probability).

**Returns:** Random boolean

**Example:**

.. code-block:: ml

   import random;

   coinFlip = random.randomBool();
   if (coinFlip) {
       console.log("Heads");
   } else {
       console.log("Tails");
   }

randomBoolWeighted()
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ml

   randomBoolWeighted(probability) -> boolean

Generate random boolean with specified probability of true.

**Parameters:**

- ``probability``: Probability of returning true (0.0 to 1.0)

**Returns:** Random boolean based on probability

**Example:**

.. code-block:: ml

   import random;

   // 70% chance of rain
   willRain = random.randomBoolWeighted(0.7);

   // 20% chance of critical hit
   isCritical = random.randomBoolWeighted(0.2);

List Sampling
-------------

choice()
~~~~~~~~

.. code-block:: ml

   choice(list) -> element

Choose random element from list.

**Parameters:**

- ``list``: List to choose from

**Returns:** Random element, or null if list is empty

**Example:**

.. code-block:: ml

   import random;

   fruits = ["apple", "banana", "cherry", "date"];
   picked = random.choice(fruits);
   // Result: e.g., "banana"

shuffle()
~~~~~~~~~

.. code-block:: ml

   shuffle(list) -> list

Shuffle list (returns new shuffled list).

**Parameters:**

- ``list``: List to shuffle

**Returns:** New shuffled list (original unchanged)

**Example:**

.. code-block:: ml

   import random;

   deck = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"];
   shuffled = random.shuffle(deck);
   // Result: random order, e.g., ["5", "K", "2", "9", ...]

sample()
~~~~~~~~

.. code-block:: ml

   sample(list, n) -> list

Generate random sample of n elements from list.

**Parameters:**

- ``list``: List to sample from
- ``n``: Number of elements to sample

**Returns:** List of n randomly sampled elements (without replacement)

**Example:**

.. code-block:: ml

   import random;

   participants = ["Alice", "Bob", "Charlie", "Diana", "Eve"];
   winners = random.sample(participants, 3);
   // Result: e.g., ["Diana", "Bob", "Eve"]

randomIndices()
~~~~~~~~~~~~~~~

.. code-block:: ml

   randomIndices(length, count) -> list

Generate random indices for array access.

**Parameters:**

- ``length``: Length of array
- ``count``: Number of indices to generate

**Returns:** List of random indices (without duplicates)

**Example:**

.. code-block:: ml

   import random;

   // Pick 5 random items from array of 100
   indices = random.randomIndices(100, 5);
   // Result: e.g., [23, 67, 8, 91, 45]

Statistical Distributions
-------------------------

uniform()
~~~~~~~~~

.. code-block:: ml

   uniform(min, max) -> number

Generate uniform random value (alias for randomFloat).

**Parameters:**

- ``min``: Minimum value
- ``max``: Maximum value

**Returns:** Random value in range

**Example:**

.. code-block:: ml

   import random;

   value = random.uniform(0, 100);
   // Result: evenly distributed between 0-100

randomNormal()
~~~~~~~~~~~~~~

.. code-block:: ml

   randomNormal(mean, stddev) -> number

Generate random number from normal (Gaussian) distribution.

**Parameters:**

- ``mean``: Mean of distribution (default 0)
- ``stddev``: Standard deviation (default 1)

**Returns:** Random value from normal distribution

**Example:**

.. code-block:: ml

   import random;

   // Standard normal (mean=0, stddev=1)
   value = random.randomNormal(0, 1);

   // IQ scores (mean=100, stddev=15)
   iq = random.randomNormal(100, 15);

gaussian()
~~~~~~~~~~

.. code-block:: ml

   gaussian(mean, stddev) -> number

Generate Gaussian random value (alias for randomNormal).

**Parameters:**

- ``mean``: Mean of distribution (default 0)
- ``stddev``: Standard deviation (default 1)

**Returns:** Random value from Gaussian distribution

**Example:**

.. code-block:: ml

   import random;

   height = random.gaussian(175, 7);  // Men's height in cm

triangular()
~~~~~~~~~~~~

.. code-block:: ml

   triangular(low, high, mode) -> number

Generate random value from triangular distribution.

**Parameters:**

- ``low``: Lower bound
- ``high``: Upper bound
- ``mode``: Mode (peak) of distribution (default is midpoint)

**Returns:** Random value from triangular distribution

**Example:**

.. code-block:: ml

   import random;

   // Response time: most around 50ms, range 10-200ms
   responseTime = random.triangular(10, 200, 50);

Practical Patterns
------------------

Monte Carlo Simulation
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/random/05_comprehensive_example.ml
   :language: ml
   :lines: 20-42
   :caption: Estimate Pi using Monte Carlo method

Reproducible Testing
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/random/02_seeding_reproducibility.ml
   :language: ml
   :lines: 43-68
   :caption: Reproducible test data generation

Random Sampling
~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/random/03_sampling.ml
   :language: ml
   :lines: 84-109
   :caption: Card dealing with shuffle and sample

Statistical Simulation
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../ml_snippets/standard-library/random/04_distributions.ml
   :language: ml
   :lines: 120-163
   :caption: Test score simulation with normal distribution

Common Use Cases
----------------

**Games and Entertainment:**

.. code-block:: ml

   import random;

   // Dice roll
   dice = random.randomInt(1, 7);

   // Card shuffle
   deck = createDeck();  // Your deck creation function
   shuffled = random.shuffle(deck);

   // Random enemy encounter (30% chance)
   encounterEnemy = random.randomBoolWeighted(0.3);

**Data Science and Statistics:**

.. code-block:: ml

   import random;

   // Random sampling for survey
   population = getAllUsers();  // Your data source
   sample = random.sample(population, 100);

   // Normal distribution for synthetic data
   testData = [];
   i = 0;
   while (i < 1000) {
       value = random.randomNormal(50, 10);
       testData = testData + [value];
       i = i + 1;
   }

**Testing and Simulation:**

.. code-block:: ml

   import random;

   // Reproducible test
   random.setSeed(42);
   testInput = random.randomInt(1, 1000);

   // A/B test simulation
   assignToGroupA = random.randomBool();

   // Load testing with random delays
   delay = random.triangular(100, 500, 200);

**Procedural Generation:**

.. code-block:: ml

   import random;

   // Random terrain
   function generateTerrain(seed) {
       random.setSeed(seed);

       terrain = [];
       i = 0;
       while (i < 100) {
           height = random.randomNormal(50, 15);
           terrain = terrain + [height];
           i = i + 1;
       }

       return terrain;
   }

Performance Considerations
--------------------------

**Seeding for Reproducibility:**

- Use setSeed() at start of tests for reproducible results
- Same seed always produces same sequence
- Essential for debugging and testing

**Distribution Selection:**

.. code-block:: ml

   // Good: Use appropriate distribution
   uniform = random.uniform(0, 100);        // Equal probability
   normal = random.randomNormal(50, 10);    // Bell curve
   triangular = random.triangular(0, 100, 75); // Skewed

**Sampling Efficiency:**

.. code-block:: ml

   // Good: Sample once
   winners = random.sample(participants, 10);

   // Avoid: Multiple random.choice() calls
   // (could pick same element twice)

**Random vs Deterministic:**

.. code-block:: ml

   // Production: Use random seed or current time
   random.setSeed(getCurrentTime());

   // Testing: Use fixed seed
   random.setSeed(42);

Statistical Properties
----------------------

**Uniform Distribution:**

- All values equally likely
- Use for: dice rolls, card shuffling, random selection

**Normal Distribution:**

- Bell curve centered on mean
- 68% within 1 stddev, 95% within 2 stddev
- Use for: heights, test scores, measurement errors

**Triangular Distribution:**

- Linear ramp up to mode, linear ramp down
- More realistic than uniform for many real-world cases
- Use for: response times, project estimates

See Also
--------

- :doc:`math` - Mathematical functions and constants
- :doc:`functional` - Functional programming utilities

Complete Examples
-----------------

See the following complete examples:

- ``docs/ml_snippets/standard-library/random/01_basic_random.ml`` - Basic random generation
- ``docs/ml_snippets/standard-library/random/02_seeding_reproducibility.ml`` - Seeding and reproducible sequences
- ``docs/ml_snippets/standard-library/random/03_sampling.ml`` - List sampling and shuffling
- ``docs/ml_snippets/standard-library/random/04_distributions.ml`` - Statistical distributions
- ``docs/ml_snippets/standard-library/random/05_comprehensive_example.ml`` - Monte Carlo simulations
