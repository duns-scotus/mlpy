// Data analysis pipeline test program (corrected ML syntax)
function analyzeData(data) {
    sum = 0;
    count = 0;
    i = 0;

    while (i < 5) {
        value = data[i];
        sum = sum + value;
        count = count + 1;
        i = i + 1;
    }

    mean = sum / count;
    return mean;
}

function processDataSet(dataset) {
    // Pre-allocate array with nulls for known size
    results = [null, null, null];
    i = 0;

    while (i < 3) {
        item = dataset[i];
        if (item > 10) {
            processed = item * 2;
            results[i] = processed;
        } else {
            results[i] = item + 1;
        }
        i = i + 1;
    }

    return results;
}

function findMinMax(values) {
    min = values[0];
    max = values[0];
    i = 1;

    while (i < 4) {
        current = values[i];
        if (current < min) {
            min = current;
        }
        if (current > max) {
            max = current;
        }
        i = i + 1;
    }

    return [min, max];
}

// Sample data processing
rawData = [1, 5, 10, 15, 20];
mean = analyzeData(rawData);
processed = processDataSet([3, 12, 8]);
minMax = findMinMax([4, 2, 9, 1]);