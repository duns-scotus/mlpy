// Statistics Collection and Analysis
// Demonstrates ML's functional programming, data analysis, and statistical computations

// Data point structure for time series analysis
type DataPoint = {
    time: number;
    predator_count: number;
    prey_count: number;
    average_predator_energy: number;
    average_prey_energy: number;
    resource_availability: number;
    environmental_pressure: number;
}

// Statistical summary structure
type StatisticalSummary = {
    mean: number;
    median: number;
    std_deviation: number;
    min: number;
    max: number;
    count: number;
}

// Main statistics container
type Statistics = {
    data_points: DataPoint[];
    population_peaks: {
        predator_peak: { time: number, count: number };
        prey_peak: { time: number, count: number };
    };
    extinction_events: {
        predator_extinction: number | null;
        prey_extinction: number | null;
    };
    stability_metrics: {
        predator_stability: number;
        prey_stability: number;
        system_stability: number;
    };
}

// Statistics factory and analysis functions
export const Statistics = {
    // Create new statistics collector
    create: function(): Statistics {
        return {
            data_points: [],
            population_peaks: {
                predator_peak: { time: 0, count: 0 },
                prey_peak: { time: 0, count: 0 }
            },
            extinction_events: {
                predator_extinction: null,
                prey_extinction: null
            },
            stability_metrics: {
                predator_stability: 0,
                prey_stability: 0,
                system_stability: 0
            }
        }
    },

    // Record a new data point and update statistics
    recordDataPoint: function(stats: Statistics, data: DataPoint): Statistics {
        new_data_points = [...stats.data_points, data]

        // Update population peaks
        new_predator_peak = stats.population_peaks.predator_peak
        if (data.predator_count > new_predator_peak.count) {
            new_predator_peak = { time: data.time, count: data.predator_count }
        }

        new_prey_peak = stats.population_peaks.prey_peak
        if (data.prey_count > new_prey_peak.count) {
            new_prey_peak = { time: data.time, count: data.prey_count }
        }

        // Check for extinction events
        new_extinction_events = { ...stats.extinction_events }
        if (data.predator_count == 0 && stats.extinction_events.predator_extinction == null) {
            new_extinction_events.predator_extinction = data.time
        }
        if (data.prey_count == 0 && stats.extinction_events.prey_extinction == null) {
            new_extinction_events.prey_extinction = data.time
        }

        // Calculate stability metrics (every 100 data points for performance)
        new_stability_metrics = stats.stability_metrics
        if (new_data_points.length % 100 == 0 && new_data_points.length > 200) {
            new_stability_metrics = calculateStabilityMetrics(new_data_points)
        }

        return {
            data_points: new_data_points,
            population_peaks: {
                predator_peak: new_predator_peak,
                prey_peak: new_prey_peak
            },
            extinction_events: new_extinction_events,
            stability_metrics: new_stability_metrics
        }
    },

    // Generate comprehensive analysis report
    generateReport: function(stats: Statistics): object {
        if (stats.data_points.length == 0) {
            return { error: "No data points available" }
        }

        // Population statistics
        predator_stats = calculateColumnStatistics(stats.data_points, "predator_count")
        prey_stats = calculateColumnStatistics(stats.data_points, "prey_count")
        predator_energy_stats = calculateColumnStatistics(stats.data_points, "average_predator_energy")
        prey_energy_stats = calculateColumnStatistics(stats.data_points, "average_prey_energy")

        // Correlation analysis
        correlations = calculateCorrelations(stats.data_points)

        // Trend analysis
        trends = analyzeTrends(stats.data_points)

        // Ecosystem health metrics
        health_metrics = calculateEcosystemHealth(stats.data_points)

        return {
            simulation_summary: {
                duration: stats.data_points[stats.data_points.length - 1].time,
                total_data_points: stats.data_points.length,
                population_peaks: stats.population_peaks,
                extinction_events: stats.extinction_events
            },
            population_statistics: {
                predators: predator_stats,
                prey: prey_stats
            },
            energy_statistics: {
                predator_energy: predator_energy_stats,
                prey_energy: prey_energy_stats
            },
            correlations: correlations,
            trends: trends,
            ecosystem_health: health_metrics,
            stability_metrics: stats.stability_metrics
        }
    },

    // Export data for visualization tools
    exportTimeSeriesData: function(stats: Statistics): object[] {
        return stats.data_points.map(point => ({
            time: point.time,
            predators: point.predator_count,
            prey: point.prey_count,
            predator_energy: point.average_predator_energy,
            prey_energy: point.average_prey_energy,
            resources: point.resource_availability,
            pressure: point.environmental_pressure
        }))
    }
}

// Calculate statistical summary for a column of data
function calculateColumnStatistics(data_points: DataPoint[], column: string): StatisticalSummary {
    // Extract column values using functional programming
    values = data_points.map(point => point[column]).filter(val => val != null && !isNaN(val))

    if (values.length == 0) {
        return {
            mean: 0, median: 0, std_deviation: 0,
            min: 0, max: 0, count: 0
        }
    }

    // Sort for median calculation
    sorted_values = [...values].sort((a, b) => a - b)

    // Calculate basic statistics
    sum = values.reduce((acc, val) => acc + val, 0)
    mean = sum / values.length
    min = sorted_values[0]
    max = sorted_values[sorted_values.length - 1]

    // Calculate median
    median_index = Math.floor(sorted_values.length / 2)
    median = sorted_values.length % 2 == 0 ?
        (sorted_values[median_index - 1] + sorted_values[median_index]) / 2 :
        sorted_values[median_index]

    // Calculate standard deviation
    variance = values.reduce((acc, val) => {
        diff = val - mean
        return acc + (diff * diff)
    }, 0) / values.length
    std_deviation = Math.sqrt(variance)

    return {
        mean: mean,
        median: median,
        std_deviation: std_deviation,
        min: min,
        max: max,
        count: values.length
    }
}

// Calculate correlation coefficients between different variables
function calculateCorrelations(data_points: DataPoint[]): object {
    // Extract time series for correlation analysis
    predator_counts = data_points.map(p => p.predator_count)
    prey_counts = data_points.map(p => p.prey_count)
    predator_energies = data_points.map(p => p.average_predator_energy)
    prey_energies = data_points.map(p => p.average_prey_energy)
    resources = data_points.map(p => p.resource_availability)

    return {
        predator_prey_correlation: calculatePearsonCorrelation(predator_counts, prey_counts),
        predator_count_energy: calculatePearsonCorrelation(predator_counts, predator_energies),
        prey_count_energy: calculatePearsonCorrelation(prey_counts, prey_energies),
        prey_resource_correlation: calculatePearsonCorrelation(prey_counts, resources),
        predator_resource_correlation: calculatePearsonCorrelation(predator_counts, resources),
        energy_balance_correlation: calculatePearsonCorrelation(predator_energies, prey_energies)
    }
}

// Calculate Pearson correlation coefficient
function calculatePearsonCorrelation(x_values: number[], y_values: number[]): number {
    if (x_values.length != y_values.length || x_values.length < 2) {
        return 0
    }

    n = x_values.length
    sum_x = x_values.reduce((sum, val) => sum + val, 0)
    sum_y = y_values.reduce((sum, val) => sum + val, 0)
    sum_xy = x_values.reduce((sum, x_val, i) => sum + (x_val * y_values[i]), 0)
    sum_x_squared = x_values.reduce((sum, val) => sum + (val * val), 0)
    sum_y_squared = y_values.reduce((sum, val) => sum + (val * val), 0)

    numerator = (n * sum_xy) - (sum_x * sum_y)
    denominator_x = (n * sum_x_squared) - (sum_x * sum_x)
    denominator_y = (n * sum_y_squared) - (sum_y * sum_y)
    denominator = Math.sqrt(denominator_x * denominator_y)

    if (denominator == 0) {
        return 0
    }

    return numerator / denominator
}

// Analyze population trends using linear regression
function analyzeTrends(data_points: DataPoint[]): object {
    // Calculate trends for the last 25% of data (recent trends)
    recent_start = Math.floor(data_points.length * 0.75)
    recent_data = data_points.slice(recent_start)

    if (recent_data.length < 2) {
        return { error: "Insufficient data for trend analysis" }
    }

    // Extract time series for trend analysis
    times = recent_data.map(p => p.time)
    predator_counts = recent_data.map(p => p.predator_count)
    prey_counts = recent_data.map(p => p.prey_count)

    // Calculate linear regression slopes
    predator_trend = calculateLinearTrend(times, predator_counts)
    prey_trend = calculateLinearTrend(times, prey_counts)

    return {
        analysis_period: {
            start_time: recent_data[0].time,
            end_time: recent_data[recent_data.length - 1].time,
            data_points: recent_data.length
        },
        predator_trend: {
            slope: predator_trend.slope,
            direction: predator_trend.slope > 0.1 ? "increasing" :
                     predator_trend.slope < -0.1 ? "decreasing" : "stable",
            r_squared: predator_trend.r_squared
        },
        prey_trend: {
            slope: prey_trend.slope,
            direction: prey_trend.slope > 0.1 ? "increasing" :
                     prey_trend.slope < -0.1 ? "decreasing" : "stable",
            r_squared: prey_trend.r_squared
        }
    }
}

// Calculate linear regression trend
function calculateLinearTrend(x_values: number[], y_values: number[]): { slope: number, r_squared: number } {
    if (x_values.length != y_values.length || x_values.length < 2) {
        return { slope: 0, r_squared: 0 }
    }

    n = x_values.length
    sum_x = x_values.reduce((sum, val) => sum + val, 0)
    sum_y = y_values.reduce((sum, val) => sum + val, 0)
    sum_xy = x_values.reduce((sum, x_val, i) => sum + (x_val * y_values[i]), 0)
    sum_x_squared = x_values.reduce((sum, val) => sum + (val * val), 0)
    sum_y_squared = y_values.reduce((sum, val) => sum + (val * val), 0)

    // Calculate slope
    slope = ((n * sum_xy) - (sum_x * sum_y)) / ((n * sum_x_squared) - (sum_x * sum_x))

    // Calculate R-squared
    y_mean = sum_y / n
    ss_total = y_values.reduce((sum, y) => sum + Math.pow(y - y_mean, 2), 0)
    ss_residual = y_values.reduce((sum, y, i) => {
        predicted = slope * x_values[i] + (sum_y - slope * sum_x) / n
        return sum + Math.pow(y - predicted, 2)
    }, 0)

    r_squared = ss_total > 0 ? 1 - (ss_residual / ss_total) : 0

    return { slope: slope, r_squared: r_squared }
}

// Calculate stability metrics using coefficient of variation
function calculateStabilityMetrics(data_points: DataPoint[]): object {
    // Use recent data for stability calculation (last 200 points)
    recent_data = data_points.slice(-200)

    predator_counts = recent_data.map(p => p.predator_count)
    prey_counts = recent_data.map(p => p.prey_count)

    predator_stability = calculateCoefficientOfVariation(predator_counts)
    prey_stability = calculateCoefficientOfVariation(prey_counts)

    // System stability is inverse of average CV (lower CV = more stable)
    system_stability = 1.0 / (1.0 + (predator_stability + prey_stability) / 2.0)

    return {
        predator_stability: 1.0 / (1.0 + predator_stability),  // Inverse CV for intuitive scoring
        prey_stability: 1.0 / (1.0 + prey_stability),
        system_stability: system_stability
    }
}

// Calculate coefficient of variation (std_dev / mean)
function calculateCoefficientOfVariation(values: number[]): number {
    if (values.length < 2) {
        return 0
    }

    mean = values.reduce((sum, val) => sum + val, 0) / values.length
    if (mean == 0) {
        return 0
    }

    variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length
    std_deviation = Math.sqrt(variance)

    return std_deviation / mean
}

// Calculate ecosystem health based on multiple indicators
function calculateEcosystemHealth(data_points: DataPoint[]): object {
    recent_data = data_points.slice(-100)  // Last 100 points

    if (recent_data.length == 0) {
        return { overall_health: 0, indicators: {} }
    }

    // Health indicators
    indicators = {
        population_balance: calculatePopulationBalance(recent_data),
        energy_sufficiency: calculateEnergySufficiency(recent_data),
        resource_sustainability: calculateResourceSustainability(recent_data),
        biodiversity_index: calculateBiodiversityIndex(recent_data)
    }

    // Overall health score (weighted average)
    weights = {
        population_balance: 0.3,
        energy_sufficiency: 0.25,
        resource_sustainability: 0.25,
        biodiversity_index: 0.2
    }

    overall_health =
        indicators.population_balance * weights.population_balance +
        indicators.energy_sufficiency * weights.energy_sufficiency +
        indicators.resource_sustainability * weights.resource_sustainability +
        indicators.biodiversity_index * weights.biodiversity_index

    return {
        overall_health: overall_health,
        health_rating: overall_health > 0.8 ? "Excellent" :
                      overall_health > 0.6 ? "Good" :
                      overall_health > 0.4 ? "Fair" :
                      overall_health > 0.2 ? "Poor" : "Critical",
        indicators: indicators
    }
}

// Calculate how balanced predator/prey populations are
function calculatePopulationBalance(data_points: DataPoint[]): number {
    ratios = data_points
        .filter(p => p.predator_count > 0 && p.prey_count > 0)
        .map(p => p.prey_count / p.predator_count)

    if (ratios.length == 0) {
        return 0  // No coexistence
    }

    // Optimal ratio is around 3-7 prey per predator
    optimal_min = 3
    optimal_max = 7

    balanced_ratios = ratios.filter(ratio => ratio >= optimal_min && ratio <= optimal_max)
    return balanced_ratios.length / ratios.length
}

// Calculate energy sufficiency for populations
function calculateEnergySufficiency(data_points: DataPoint[]): number {
    energy_scores = data_points.map(p => {
        predator_score = Math.min(1.0, p.average_predator_energy / 50.0)  // 50 is healthy energy
        prey_score = Math.min(1.0, p.average_prey_energy / 40.0)         // 40 is healthy energy
        return (predator_score + prey_score) / 2.0
    })

    return energy_scores.reduce((sum, score) => sum + score, 0) / energy_scores.length
}

// Calculate resource sustainability
function calculateResourceSustainability(data_points: DataPoint[]): number {
    if (data_points.length == 0) {
        return 0
    }

    // Check if resources are maintaining adequate levels
    resource_levels = data_points.map(p => Math.min(1.0, p.resource_availability / 500.0))  // 500 is adequate
    average_resource_level = resource_levels.reduce((sum, level) => sum + level, 0) / resource_levels.length

    // Penalize if resources are declining rapidly
    if (data_points.length > 1) {
        first_resources = data_points[0].resource_availability
        last_resources = data_points[data_points.length - 1].resource_availability

        if (first_resources > 0) {
            decline_factor = last_resources / first_resources
            average_resource_level *= Math.max(0.1, decline_factor)
        }
    }

    return average_resource_level
}

// Simple biodiversity index based on population presence and stability
function calculateBiodiversityIndex(data_points: DataPoint[]): number {
    // Check coexistence
    coexistence_points = data_points.filter(p => p.predator_count > 0 && p.prey_count > 0)
    coexistence_ratio = coexistence_points.length / data_points.length

    // Check population variability (some variability is good for genetic diversity)
    if (data_points.length < 2) {
        return coexistence_ratio
    }

    predator_cv = calculateCoefficientOfVariation(data_points.map(p => p.predator_count))
    prey_cv = calculateCoefficientOfVariation(data_points.map(p => p.prey_count))

    // Optimal CV is around 0.2-0.5 (some variation, not too much)
    predator_diversity_score = predator_cv > 0.2 && predator_cv < 0.5 ? 1.0 : 0.5
    prey_diversity_score = prey_cv > 0.2 && prey_cv < 0.5 ? 1.0 : 0.5

    return (coexistence_ratio * 0.5) + (predator_diversity_score * 0.25) + (prey_diversity_score * 0.25)
}

// Export types and main Statistics object
export { Statistics, DataPoint, StatisticalSummary }