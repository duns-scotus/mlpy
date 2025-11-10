"""CSV file processing module for ML.

This module provides functions for reading and writing CSV (Comma-Separated Values) files,
supporting both dictionary and array formats with configurable delimiters.

Required Capabilities:
    - file.read: Read CSV files
    - file.write: Write CSV files

Example:
    ```ml
    import csv;

    // Read CSV as array of objects
    data = csv.read("users.csv");

    // Write CSV from objects
    csv.write("output.csv", data);
    ```
"""

import csv as py_csv
import io
from typing import Any, List, Dict, Optional, Union

from mlpy.stdlib.decorators import ml_module, ml_function


@ml_module(
    name="csv",
    description="CSV file reading and writing with support for headers",
    capabilities=["file.read", "file.write"],
    version="1.0.0"
)
class CSV:
    """CSV file operations."""

    @ml_function(description="Read CSV file", capabilities=["file.read"])
    def read(self, file_path: str, delimiter: str = ",",
             headers: bool = True, encoding: str = "utf-8") -> List[Any]:
        """Read CSV file and return as array of objects or arrays.

        Args:
            file_path: Path to CSV file
            delimiter: Field delimiter (default: ",")
            headers: If True, use first row as keys (default: True)
            encoding: File encoding (default: "utf-8")

        Returns:
            Array of objects (if headers=True) or array of arrays (if headers=False)

        Example:
            ```ml
            // Read with headers (returns array of objects)
            users = csv.read("users.csv");
            // [{name: "Alice", age: "30"}, {name: "Bob", age: "25"}]

            // Read without headers (returns array of arrays)
            data = csv.read("data.csv", headers=false);
            // [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]]
            ```
        """
        with open(file_path, 'r', encoding=encoding, newline='') as f:
            reader = py_csv.reader(f, delimiter=delimiter)

            if headers:
                # First row is headers
                header_row = next(reader, None)
                if header_row is None:
                    return []

                # Convert remaining rows to dictionaries
                result = []
                for row in reader:
                    if len(row) == 0:  # Skip empty rows
                        continue
                    obj = {}
                    for i, value in enumerate(row):
                        if i < len(header_row):
                            obj[header_row[i]] = value
                    result.append(obj)
                return result
            else:
                # Return as array of arrays
                return [row for row in reader if len(row) > 0]

    @ml_function(description="Write CSV file", capabilities=["file.write"])
    def write(self, file_path: str, data: List[Any], delimiter: str = ",",
              headers: bool = True, encoding: str = "utf-8") -> None:
        """Write data to CSV file.

        Args:
            file_path: Path to output CSV file
            data: Array of objects or array of arrays
            delimiter: Field delimiter (default: ",")
            headers: If True, write headers from object keys (default: True)
            encoding: File encoding (default: "utf-8")

        Example:
            ```ml
            // Write array of objects
            users = [{name: "Alice", age: 30}, {name: "Bob", age: 25}];
            csv.write("users.csv", users);

            // Write array of arrays without headers
            data = [["Name", "Age"], ["Alice", "30"], ["Bob", "25"]];
            csv.write("data.csv", data, headers=false);
            ```
        """
        if len(data) == 0:
            # Write empty file
            with open(file_path, 'w', encoding=encoding, newline='') as f:
                pass
            return

        with open(file_path, 'w', encoding=encoding, newline='') as f:
            writer = py_csv.writer(f, delimiter=delimiter)

            # Check if data contains objects or arrays
            first_item = data[0]

            if isinstance(first_item, dict):
                # Array of objects
                if headers and len(first_item) > 0:
                    # Write header row from keys
                    header_row = list(first_item.keys())
                    writer.writerow(header_row)

                # Write data rows
                for item in data:
                    if isinstance(item, dict):
                        row = [item.get(key, '') for key in (header_row if headers else item.keys())]
                        writer.writerow(row)
            else:
                # Array of arrays
                for row in data:
                    if isinstance(row, (list, tuple)):
                        writer.writerow(row)
                    else:
                        # Single value, wrap in array
                        writer.writerow([row])

    @ml_function(description="Read CSV as string", capabilities=["file.read"])
    def read_string(self, csv_string: str, delimiter: str = ",",
                    headers: bool = True) -> List[Any]:
        """Parse CSV from string.

        Args:
            csv_string: CSV content as string
            delimiter: Field delimiter (default: ",")
            headers: If True, use first row as keys (default: True)

        Returns:
            Array of objects or arrays

        Example:
            ```ml
            csv_text = "name,age\\nAlice,30\\nBob,25";
            data = csv.read_string(csv_text);
            ```
        """
        f = io.StringIO(csv_string)
        reader = py_csv.reader(f, delimiter=delimiter)

        if headers:
            header_row = next(reader, None)
            if header_row is None:
                return []

            result = []
            for row in reader:
                if len(row) == 0:
                    continue
                obj = {}
                for i, value in enumerate(row):
                    if i < len(header_row):
                        obj[header_row[i]] = value
                result.append(obj)
            return result
        else:
            return [row for row in reader if len(row) > 0]

    @ml_function(description="Write CSV to string", capabilities=[])
    def write_string(self, data: List[Any], delimiter: str = ",",
                     headers: bool = True) -> str:
        """Convert data to CSV string.

        Args:
            data: Array of objects or array of arrays
            delimiter: Field delimiter (default: ",")
            headers: If True, include headers from object keys (default: True)

        Returns:
            CSV formatted string

        Example:
            ```ml
            users = [{name: "Alice", age: 30}];
            csv_text = csv.write_string(users);
            ```
        """
        if len(data) == 0:
            return ""

        output = io.StringIO()
        writer = py_csv.writer(output, delimiter=delimiter)

        first_item = data[0]

        if isinstance(first_item, dict):
            if headers and len(first_item) > 0:
                header_row = list(first_item.keys())
                writer.writerow(header_row)

            for item in data:
                if isinstance(item, dict):
                    row = [item.get(key, '') for key in (header_row if headers else item.keys())]
                    writer.writerow(row)
        else:
            for row in data:
                if isinstance(row, (list, tuple)):
                    writer.writerow(row)
                else:
                    writer.writerow([row])

        return output.getvalue()

    @ml_function(description="Count rows in CSV file", capabilities=["file.read"])
    def count_rows(self, file_path: str, delimiter: str = ",",
                   encoding: str = "utf-8") -> int:
        """Count number of data rows in CSV file (excluding header).

        Args:
            file_path: Path to CSV file
            delimiter: Field delimiter (default: ",")
            encoding: File encoding (default: "utf-8")

        Returns:
            Number of data rows

        Example:
            ```ml
            count = csv.count_rows("large_file.csv");
            console.log("Total rows: " + str(count));
            ```
        """
        with open(file_path, 'r', encoding=encoding, newline='') as f:
            reader = py_csv.reader(f, delimiter=delimiter)
            # Skip header
            next(reader, None)
            # Count remaining rows
            return sum(1 for row in reader if len(row) > 0)

    @ml_function(description="Get CSV headers", capabilities=["file.read"])
    def get_headers(self, file_path: str, delimiter: str = ",",
                    encoding: str = "utf-8") -> List[str]:
        """Get header row from CSV file.

        Args:
            file_path: Path to CSV file
            delimiter: Field delimiter (default: ",")
            encoding: File encoding (default: "utf-8")

        Returns:
            Array of header names

        Example:
            ```ml
            headers = csv.get_headers("users.csv");
            // ["name", "age", "city"]
            ```
        """
        with open(file_path, 'r', encoding=encoding, newline='') as f:
            reader = py_csv.reader(f, delimiter=delimiter)
            header_row = next(reader, None)
            return header_row if header_row else []

    @ml_function(description="Append row to CSV file", capabilities=["file.read", "file.write"])
    def append(self, file_path: str, row: Union[Dict, List], delimiter: str = ",",
               encoding: str = "utf-8") -> None:
        """Append a single row to existing CSV file.

        Args:
            file_path: Path to CSV file
            row: Object or array to append
            delimiter: Field delimiter (default: ",")
            encoding: File encoding (default: "utf-8")

        Example:
            ```ml
            new_user = {name: "Charlie", age: 35};
            csv.append("users.csv", new_user);
            ```
        """
        with open(file_path, 'a', encoding=encoding, newline='') as f:
            writer = py_csv.writer(f, delimiter=delimiter)

            if isinstance(row, dict):
                # Need to get headers to maintain order
                # Read first row to get header order
                try:
                    with open(file_path, 'r', encoding=encoding, newline='') as rf:
                        reader = py_csv.reader(rf, delimiter=delimiter)
                        headers = next(reader, None)
                        if headers:
                            row_data = [row.get(h, '') for h in headers]
                            writer.writerow(row_data)
                        else:
                            # No headers, write values only
                            writer.writerow(list(row.values()))
                except:
                    # File doesn't exist or empty, write values only
                    writer.writerow(list(row.values()))
            else:
                # Array or other
                if isinstance(row, (list, tuple)):
                    writer.writerow(row)
                else:
                    writer.writerow([row])


# Create singleton instance for module-level access
csv = CSV()
