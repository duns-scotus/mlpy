// ============================================
// Comprehensive Example: Monte Carlo Simulation
// Category: standard-library/random
// Demonstrates: Complete random module in statistical simulation
// ============================================

import console;
import random;

console.log("=== Monte Carlo Simulation System ===\n");

// Set seed for reproducibility
random.setSeed(2024);

// ============================================
// Simulation 1: Pi Estimation
// ============================================

console.log("=== Simulation 1: Estimate Pi (Monte Carlo) ===");

function estimatePi(samples) {
    insideCircle = 0;

    i = 0;
    while (i < samples) {
        // Random point in unit square
        x = random.uniform(-1, 1);
        y = random.uniform(-1, 1);

        // Check if inside unit circle
        distance = (x * x) + (y * y);
        if (distance <= 1) {
            insideCircle = insideCircle + 1;
        }

        i = i + 1;
    }

    // Pi approximation: 4 * (points in circle / total points)
    piEstimate = 4 * (insideCircle / samples);
    return piEstimate;
}

console.log("Estimating Pi with different sample sizes:");

sampleSizes = [100, 1000, 10000];
i = 0;
while (i < len(sampleSizes)) {
    samples = sampleSizes[i];
    estimate = estimatePi(samples);
    error = 3.14159 - estimate;
    if (error < 0) {
        error = -error;
    }
    console.log("  " + str(samples) + " samples: " + str(round(estimate, 5)) + " (error: " + str(round(error, 5)) + ")");
    i = i + 1;
}

// ============================================
// Simulation 2: Stock Price Random Walk
// ============================================

console.log("\n=== Simulation 2: Stock Price Random Walk ===");

function simulateStockPrice(initialPrice, days, volatility) {
    prices = [initialPrice];
    currentPrice = initialPrice;

    i = 0;
    while (i < days) {
        // Random daily change (normal distribution)
        changePercent = random.randomNormal(0, volatility);
        change = currentPrice * (changePercent / 100);
        currentPrice = currentPrice + change;

        // Prevent negative prices
        if (currentPrice < 1) {
            currentPrice = 1;
        }

        prices = prices + [currentPrice];
        i = i + 1;
    }

    return prices;
}

console.log("Simulating stock price (30 days, volatility=2%):");
initialPrice = 100;
stockPrices = simulateStockPrice(initialPrice, 30, 2);

// Show key days
console.log("  Day 1:  $" + str(round(stockPrices[0], 2)));
console.log("  Day 10: $" + str(round(stockPrices[9], 2)));
console.log("  Day 20: $" + str(round(stockPrices[19], 2)));
console.log("  Day 30: $" + str(round(stockPrices[29], 2)));

finalPrice = stockPrices[len(stockPrices) - 1];
change = finalPrice - initialPrice;
changePercent = (change / initialPrice) * 100;
console.log("  Total change: $" + str(round(change, 2)) + " (" + str(round(changePercent, 1)) + "%)");

// ============================================
// Simulation 3: Queue Wait Time Analysis
// ============================================

console.log("\n=== Simulation 3: Queue Wait Time Analysis ===");

function simulateQueue(customers, avgServiceTime) {
    waitTimes = [];

    currentTime = 0;
    i = 0;
    while (i < customers) {
        // Customer arrival (exponential-like using triangular)
        arrivalDelay = random.triangular(0, 5, 1);
        currentTime = currentTime + arrivalDelay;

        // Service time (normal distribution)
        serviceTime = random.randomNormal(avgServiceTime, avgServiceTime * 0.3);
        if (serviceTime < 0.5) {
            serviceTime = 0.5;
        }

        waitTimes = waitTimes + [serviceTime];
        currentTime = currentTime + serviceTime;

        i = i + 1;
    }

    return waitTimes;
}

console.log("Simulating customer queue (50 customers, avg service 3 min):");
waitTimes = simulateQueue(50, 3);

// Calculate statistics
sum = 0;
maxWait = waitTimes[0];
minWait = waitTimes[0];

i = 0;
while (i < len(waitTimes)) {
    time = waitTimes[i];
    sum = sum + time;

    if (time > maxWait) {
        maxWait = time;
    }
    if (time < minWait) {
        minWait = time;
    }

    i = i + 1;
}

avgWait = sum / len(waitTimes);

console.log("  Average wait: " + str(round(avgWait, 2)) + " minutes");
console.log("  Min wait: " + str(round(minWait, 2)) + " minutes");
console.log("  Max wait: " + str(round(maxWait, 2)) + " minutes");

// ============================================
// Simulation 4: A/B Test Simulation
// ============================================

console.log("\n=== Simulation 4: A/B Test Simulation ===");

function simulateABTest(visitors, conversionRateA, conversionRateB) {
    conversionsA = 0;
    conversionsB = 0;

    i = 0;
    while (i < visitors) {
        // Randomly assign to A or B
        assignToA = random.randomBool();

        if (assignToA) {
            // Test A
            converted = random.randomBoolWeighted(conversionRateA);
            if (converted) {
                conversionsA = conversionsA + 1;
            }
        } else {
            // Test B
            converted = random.randomBoolWeighted(conversionRateB);
            if (converted) {
                conversionsB = conversionsB + 1;
            }
        }

        i = i + 1;
    }

    return {
        conversionsA: conversionsA,
        conversionsB: conversionsB,
        visitorsPerGroup: visitors / 2
    };
}

console.log("Simulating A/B test (1000 visitors):");
console.log("  Version A: 5% conversion rate");
console.log("  Version B: 7% conversion rate");

result = simulateABTest(1000, 0.05, 0.07);

rateA = (result.conversionsA / result.visitorsPerGroup) * 100;
rateB = (result.conversionsB / result.visitorsPerGroup) * 100;
improvement = ((rateB - rateA) / rateA) * 100;

console.log("\nResults:");
console.log("  Version A: " + str(result.conversionsA) + " conversions (" + str(round(rateA, 2)) + "%)");
console.log("  Version B: " + str(result.conversionsB) + " conversions (" + str(round(rateB, 2)) + "%)");
console.log("  Improvement: " + str(round(improvement, 1)) + "%");

// ============================================
// Simulation 5: Dice Game Probability
// ============================================

console.log("\n=== Simulation 5: Dice Game Probability ===");

function playDiceGame(rolls) {
    // Win if sum of 2 dice >= 10
    wins = 0;

    i = 0;
    while (i < rolls) {
        die1 = random.randomInt(1, 7);
        die2 = random.randomInt(1, 7);
        sum = die1 + die2;

        if (sum >= 10) {
            wins = wins + 1;
        }

        i = i + 1;
    }

    return wins;
}

console.log("Dice game: Win if sum >= 10");
console.log("Running 1000 games:");

wins = playDiceGame(1000);
winRate = (wins / 1000) * 100;

console.log("  Wins: " + str(wins) + "/1000");
console.log("  Win rate: " + str(round(winRate, 1)) + "%");
console.log("  Theoretical: 16.67% (6 out of 36 combinations)");

// ============================================
// Simulation 6: Portfolio Diversification
// ============================================

console.log("\n=== Simulation 6: Portfolio Risk Analysis ===");

function simulatePortfolio(stocks, days, correlationFactor) {
    portfolio = [];

    // Initialize stocks with $100 each
    i = 0;
    while (i < stocks) {
        portfolio = portfolio + [100];
        i = i + 1;
    }

    // Simulate each day
    day = 0;
    while (day < days) {
        // Market factor (affects all stocks)
        marketChange = random.randomNormal(0, 1);

        // Update each stock
        i = 0;
        while (i < len(portfolio)) {
            // Stock-specific change
            specificChange = random.randomNormal(0, 1.5);

            // Combined change (correlation + specific)
            totalChange = (marketChange * correlationFactor) + (specificChange * (1 - correlationFactor));

            portfolio[i] = portfolio[i] * (1 + totalChange / 100);

            // Prevent negative
            if (portfolio[i] < 1) {
                portfolio[i] = 1;
            }

            i = i + 1;
        }

        day = day + 1;
    }

    return portfolio;
}

console.log("Simulating 5-stock portfolio (30 days):");

finalValues = simulatePortfolio(5, 30, 0.3);

totalValue = 0;
i = 0;
while (i < len(finalValues)) {
    value = finalValues[i];
    totalValue = totalValue + value;
    console.log("  Stock " + str(i + 1) + ": $" + str(round(value, 2)));
    i = i + 1;
}

initialTotal = 500;  // 5 stocks * $100
portfolioReturn = ((totalValue - initialTotal) / initialTotal) * 100;

console.log("\nPortfolio Summary:");
console.log("  Initial: $" + str(initialTotal));
console.log("  Final: $" + str(round(totalValue, 2)));
console.log("  Return: " + str(round(portfolioReturn, 2)) + "%");

// ============================================
// Simulation 7: Tournament Brackets
// ============================================

console.log("\n=== Simulation 7: Tournament Simulation ===");

function simulateTournament(teams) {
    console.log("Tournament with " + str(len(teams)) + " teams");

    // Shuffle teams for random brackets
    remaining = random.shuffle(teams);
    round = 1;

    while (len(remaining) > 1) {
        console.log("\nRound " + str(round) + ":");

        winners = [];
        i = 0;
        while (i < len(remaining) - 1) {
            team1 = remaining[i];
            team2 = remaining[i + 1];

            // Random match outcome (could add skill-based probability)
            team1Wins = random.randomBool();

            if (team1Wins) {
                console.log("  " + team1 + " defeats " + team2);
                winners = winners + [team1];
            } else {
                console.log("  " + team2 + " defeats " + team1);
                winners = winners + [team2];
            }

            i = i + 2;
        }

        remaining = winners;
        round = round + 1;
    }

    champion = remaining[0];
    console.log("\nChampion: " + champion);
    return champion;
}

teams = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta"];
champion = simulateTournament(teams);

// ============================================
// Summary Statistics
// ============================================

console.log("\n=== Monte Carlo Simulation Summary ===");

console.log("Completed 7 different simulations:");
console.log("  1. Pi estimation (geometric probability)");
console.log("  2. Stock price random walk (financial modeling)");
console.log("  3. Queue analysis (operations research)");
console.log("  4. A/B testing (statistical inference)");
console.log("  5. Dice probability (discrete random variables)");
console.log("  6. Portfolio risk (correlated random variables)");
console.log("  7. Tournament brackets (combinatorial sampling)");

console.log("\nRandom module capabilities demonstrated:");
console.log("  - Uniform distribution (geometric, queues)");
console.log("  - Normal distribution (stock prices, service times)");
console.log("  - Triangular distribution (asymmetric delays)");
console.log("  - Weighted probabilities (A/B tests, outcomes)");
console.log("  - List sampling (shuffling, tournament brackets)");
console.log("  - Reproducible simulations (seeding)");

console.log("\n=== Monte Carlo Simulation Complete ===");
