"""Generated Python code from mlpy ML transpiler."""

# This code was automatically generated from ML source
# Modifications to this file may be lost on regeneration

# ML Standard Library imports
from mlpy.stdlib.console_bridge import console
from mlpy.stdlib import getCurrentTime, processData, typeof

def analyzeData(data):
    sum = 0
    count = 0
    i = 0
    while (i < 5):
        value = data[i]
        sum = (sum + value)
        count = (count + 1)
        i = (i + 1)
    mean = (sum / count)
    return mean

def processDataSet(dataset):
    results = [None, None, None]
    i = 0
    while (i < 3):
        item = dataset[i]
        if (item > 10):
            processed = (item * 2)
            results[i] = processed
        else:
            results[i] = (item + 1)
        i = (i + 1)
    return results

def findMinMax(values):
    min = values[0]
    max = values[0]
    i = 1
    while (i < 4):
        current = values[i]
        if (current < min):
            min = current
        if (current > max):
            max = current
        i = (i + 1)
    return [min, max]

rawData = [1, 5, 10, 15, 20]

mean = analyzeData(rawData)

processed = processDataSet([3, 12, 8])

minMax = findMinMax([4, 2, 9, 1])

# End of generated code