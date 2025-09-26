// Environment and Resource Management
// Demonstrates ML's functional programming, resource modeling, and data transformations

import { Position, calculateDistance } from "./species"

// Resource types in the ecosystem
type ResourceType = "vegetation" | "water" | "shelter"

type Resource = {
    position: Position;
    type: ResourceType;
    amount: number;
    max_capacity: number;
    regeneration_rate: number;
    quality: number;
}

type Environment = {
    size: number;
    resources: Resource[];
    temperature: number;
    season: string;
    day_cycle: number;
}

// Environment factory and management functions
export const Environment = {
    // Create environment with procedurally generated resources
    create: function(size: number, total_capacity: number): Environment {
        resources = generateResources(size, total_capacity)

        return {
            size: size,
            resources: resources,
            temperature: 20.0,  // Celsius
            season: "spring",
            day_cycle: 0.0
        }
    },

    // Update resources based on natural regeneration and consumption
    updateResources: function(env: Environment, time_step: number): Environment {
        // Update each resource using functional programming
        updated_resources = env.resources.map(resource => {
            // Natural regeneration based on resource type
            regen_amount = calculateRegeneration(resource, env, time_step)
            new_amount = Math.min(
                resource.max_capacity,
                resource.amount + regen_amount
            )

            // Update resource quality based on environmental factors
            quality_change = calculateQualityChange(resource, env, time_step)
            new_quality = Math.max(0.1, Math.min(1.0, resource.quality + quality_change))

            return {
                ...resource,
                amount: new_amount,
                quality: new_quality
            }
        })

        // Update environmental parameters
        new_day_cycle = (env.day_cycle + time_step * 0.1) % 24.0
        new_temperature = calculateTemperature(env, new_day_cycle)
        new_season = calculateSeason(env.day_cycle)

        return {
            ...env,
            resources: updated_resources,
            temperature: new_temperature,
            season: new_season,
            day_cycle: new_day_cycle
        }
    },

    // Calculate total available resources
    getTotalResources: function(env: Environment): number {
        return env.resources.reduce((total, resource) => {
            return total + resource.amount
        }, 0)
    },

    // Find resources within range of a position
    getResourcesInRange: function(env: Environment, position: Position, range: number): Resource[] {
        return env.resources.filter(resource => {
            distance = calculateDistance(position, resource.position)
            return distance <= range && resource.amount > 0
        })
    },

    // Consume resources at a location
    consumeResource: function(env: Environment, position: Position, amount: number): Environment {
        updated_resources = env.resources.map(resource => {
            distance = calculateDistance(position, resource.position)

            if (distance <= 5 && resource.amount > 0) {
                // Consume from this resource
                consumed = Math.min(resource.amount, amount)
                return {
                    ...resource,
                    amount: resource.amount - consumed
                }
            }

            return resource
        })

        return {
            ...env,
            resources: updated_resources
        }
    },

    // Get environmental pressure (affects species behavior)
    getEnvironmentalPressure: function(env: Environment): number {
        // Calculate pressure based on resource scarcity and temperature
        total_resources = Environment.getTotalResources(env)
        max_possible = env.resources.reduce((total, resource) => {
            return total + resource.max_capacity
        }, 0)

        resource_pressure = 1.0 - (total_resources / max_possible)
        temperature_pressure = calculateTemperaturePressure(env.temperature)

        return (resource_pressure + temperature_pressure) / 2.0
    }
}

// Procedural resource generation
function generateResources(environment_size: number, total_capacity: number): Resource[] {
    resources: Resource[] = []

    // Generate vegetation patches - most abundant resource
    vegetation_count = Math.floor(total_capacity * 0.6 / 50)  // 60% of capacity in vegetation
    for (i = 0; i < vegetation_count; i = i + 1) {
        // Use clustered distribution for realistic vegetation patches
        cluster_center = {
            x: Math.random() * environment_size,
            y: Math.random() * environment_size
        }

        // Create 3-8 vegetation resources per cluster
        patch_size = 3 + Math.floor(Math.random() * 6)
        for (j = 0; j < patch_size; j = j + 1) {
            position = {
                x: cluster_center.x + (Math.random() - 0.5) * 40,
                y: cluster_center.y + (Math.random() - 0.5) * 40
            }

            // Keep within environment bounds
            position.x = Math.max(0, Math.min(environment_size, position.x))
            position.y = Math.max(0, Math.min(environment_size, position.y))

            resource = {
                position: position,
                type: "vegetation",
                amount: 30 + Math.random() * 40,
                max_capacity: 50 + Math.random() * 30,
                regeneration_rate: 0.5 + Math.random() * 0.5,
                quality: 0.7 + Math.random() * 0.3
            }
            resources.push(resource)
        }
    }

    // Generate water sources - critical but sparse
    water_count = Math.floor(environment_size / 100)  // Roughly 1 per 100x100 area
    for (i = 0; i < water_count; i = i + 1) {
        position = {
            x: Math.random() * environment_size,
            y: Math.random() * environment_size
        }

        resource = {
            position: position,
            type: "water",
            amount: 100 + Math.random() * 100,
            max_capacity: 150 + Math.random() * 50,
            regeneration_rate: 1.0 + Math.random() * 0.5,
            quality: 0.8 + Math.random() * 0.2
        }
        resources.push(resource)
    }

    // Generate shelter locations
    shelter_count = Math.floor(environment_size / 80)
    for (i = 0; i < shelter_count; i = i + 1) {
        position = {
            x: Math.random() * environment_size,
            y: Math.random() * environment_size
        }

        resource = {
            position: position,
            type: "shelter",
            amount: 10 + Math.random() * 5,
            max_capacity: 15,
            regeneration_rate: 0.1,
            quality: 0.6 + Math.random() * 0.4
        }
        resources.push(resource)
    }

    return resources
}

// Calculate resource regeneration based on environmental factors
function calculateRegeneration(resource: Resource, env: Environment, time_step: number): number {
    // Base regeneration rate
    base_regen = resource.regeneration_rate * time_step

    // Environmental modifiers
    temperature_modifier = match env.temperature {
        temp when temp < 0 => 0.1;    // Very slow in freezing
        temp when temp < 10 => 0.5;   // Slow in cold
        temp when temp < 30 => 1.0;   // Optimal in moderate temperatures
        temp when temp < 40 => 0.7;   // Slower in heat
        _ => 0.3;                     // Much slower in extreme heat
    }

    season_modifier = match env.season {
        "spring" => 1.5;  // High growth in spring
        "summer" => 1.2;  // Good growth in summer
        "autumn" => 0.8;  // Slower in autumn
        "winter" => 0.3;  // Very slow in winter
        _ => 1.0;
    }

    // Resource type specific modifiers
    type_modifier = match resource.type {
        "vegetation" => 1.0;
        "water" => 1.2;      // Water regenerates faster
        "shelter" => 0.1;    // Shelter doesn't regenerate much
        _ => 1.0;
    }

    // Calculate final regeneration amount
    total_modifier = temperature_modifier * season_modifier * type_modifier
    regenerated = base_regen * total_modifier

    return regenerated
}

// Calculate quality changes based on environmental stress
function calculateQualityChange(resource: Resource, env: Environment, time_step: number): number {
    // Quality decreases under environmental stress
    pressure = Environment.getEnvironmentalPressure(env)

    // Higher pressure degrades quality faster
    degradation = pressure * 0.01 * time_step

    // Natural quality restoration when pressure is low
    restoration = (1.0 - pressure) * 0.005 * time_step

    return restoration - degradation
}

// Calculate temperature based on day cycle and season
function calculateTemperature(env: Environment, day_cycle: number): number {
    // Base temperature by season
    base_temp = match env.season {
        "spring" => 15.0;
        "summer" => 25.0;
        "autumn" => 12.0;
        "winter" => 2.0;
        _ => 15.0;
    }

    // Daily temperature variation (sine wave)
    daily_variation = Math.sin((day_cycle / 24.0) * 2 * Math.PI) * 8.0

    // Add some random weather variation
    weather_variation = (Math.random() - 0.5) * 4.0

    return base_temp + daily_variation + weather_variation
}

// Calculate season based on day cycle (simplified seasonal progression)
function calculateSeason(day_cycle: number): string {
    // Simplified: each season lasts 1000 time units
    season_cycle = Math.floor(day_cycle / 1000) % 4

    match season_cycle {
        0 => "spring";
        1 => "summer";
        2 => "autumn";
        3 => "winter";
        _ => "spring";
    }
}

// Calculate temperature-based environmental pressure
function calculateTemperaturePressure(temperature: number): number {
    // Optimal temperature range is 15-25°C
    if (temperature >= 15 && temperature <= 25) {
        return 0.0  // No pressure in optimal range
    } else if (temperature < 15) {
        // Cold pressure increases as temperature drops
        return Math.min(1.0, (15 - temperature) / 20.0)
    } else {
        // Heat pressure increases as temperature rises
        return Math.min(1.0, (temperature - 25) / 20.0)
    }
}

// Utility function for resource distribution analysis
export function analyzeResourceDistribution(env: Environment): object {
    vegetation_resources = env.resources.filter(r => r.type == "vegetation")
    water_resources = env.resources.filter(r => r.type == "water")
    shelter_resources = env.resources.filter(r => r.type == "shelter")

    return {
        total_resources: env.resources.length,
        vegetation: {
            count: vegetation_resources.length,
            total_amount: vegetation_resources.reduce((sum, r) => sum + r.amount, 0),
            avg_quality: vegetation_resources.reduce((sum, r) => sum + r.quality, 0) / vegetation_resources.length
        },
        water: {
            count: water_resources.length,
            total_amount: water_resources.reduce((sum, r) => sum + r.amount, 0),
            avg_quality: water_resources.reduce((sum, r) => sum + r.quality, 0) / water_resources.length
        },
        shelter: {
            count: shelter_resources.length,
            total_amount: shelter_resources.reduce((sum, r) => sum + r.amount, 0),
            avg_quality: shelter_resources.reduce((sum, r) => sum + r.quality, 0) / shelter_resources.length
        },
        environmental_conditions: {
            temperature: env.temperature,
            season: env.season,
            pressure: Environment.getEnvironmentalPressure(env)
        }
    }
}

// Export types and functions
export { Resource, ResourceType, Environment, analyzeResourceDistribution }