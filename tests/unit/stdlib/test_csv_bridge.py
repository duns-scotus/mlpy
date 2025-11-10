"""Unit tests for csv_bridge module."""

import os
import tempfile
import pytest

from mlpy.stdlib.csv_bridge import CSV


class TestCSVModule:
    """Test suite for CSV operations."""

    def setup_method(self):
        """Setup for each test method."""
        self.csv = CSV()
        self.temp_files = []

    def teardown_method(self):
        """Cleanup after each test method."""
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def create_temp_file(self, content: str = "") -> str:
        """Create temporary file for testing."""
        fd, path = tempfile.mkstemp(suffix='.csv', text=True)
        os.close(fd)
        self.temp_files.append(path)
        if content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        return path

    def test_write_and_read_with_headers(self):
        """Test writing and reading CSV with headers."""
        temp_file = self.create_temp_file()

        data = [
            {'name': 'Alice', 'age': '30', 'city': 'NYC'},
            {'name': 'Bob', 'age': '25', 'city': 'LA'}
        ]

        self.csv.write(temp_file, data)
        result = self.csv.read(temp_file)

        assert len(result) == 2
        assert result[0]['name'] == 'Alice'
        assert result[0]['age'] == '30'
        assert result[1]['name'] == 'Bob'

    def test_write_and_read_without_headers(self):
        """Test writing and reading CSV without headers."""
        temp_file = self.create_temp_file()

        data = [
            ['Name', 'Age', 'City'],
            ['Alice', '30', 'NYC'],
            ['Bob', '25', 'LA']
        ]

        self.csv.write(temp_file, data, headers=False)
        result = self.csv.read(temp_file, headers=False)

        assert len(result) == 3
        assert result[0] == ['Name', 'Age', 'City']
        assert result[1] == ['Alice', '30', 'NYC']

    def test_read_empty_file(self):
        """Test reading empty CSV file."""
        temp_file = self.create_temp_file("")
        result = self.csv.read(temp_file)
        assert result == []

    def test_write_empty_data(self):
        """Test writing empty data."""
        temp_file = self.create_temp_file()
        self.csv.write(temp_file, [])

        with open(temp_file, 'r') as f:
            content = f.read()
            assert content == ""

    def test_custom_delimiter(self):
        """Test CSV with custom delimiter (tab)."""
        temp_file = self.create_temp_file()

        data = [
            {'name': 'Alice', 'age': '30'},
            {'name': 'Bob', 'age': '25'}
        ]

        self.csv.write(temp_file, data, delimiter='\t')
        result = self.csv.read(temp_file, delimiter='\t')

        assert len(result) == 2
        assert result[0]['name'] == 'Alice'

    def test_read_string_with_headers(self):
        """Test parsing CSV from string with headers."""
        csv_string = "name,age,city\nAlice,30,NYC\nBob,25,LA"
        result = self.csv.read_string(csv_string)

        assert len(result) == 2
        assert result[0]['name'] == 'Alice'
        assert result[0]['age'] == '30'
        assert result[1]['name'] == 'Bob'

    def test_read_string_without_headers(self):
        """Test parsing CSV from string without headers."""
        csv_string = "Alice,30,NYC\nBob,25,LA"
        result = self.csv.read_string(csv_string, headers=False)

        assert len(result) == 2
        assert result[0] == ['Alice', '30', 'NYC']
        assert result[1] == ['Bob', '25', 'LA']

    def test_read_string_empty(self):
        """Test parsing empty CSV string."""
        result = self.csv.read_string("")
        assert result == []

    def test_write_string_with_headers(self):
        """Test converting data to CSV string with headers."""
        data = [
            {'name': 'Alice', 'age': '30'},
            {'name': 'Bob', 'age': '25'}
        ]

        result = self.csv.write_string(data)

        assert 'name,age' in result
        assert 'Alice,30' in result
        assert 'Bob,25' in result

    def test_write_string_without_headers(self):
        """Test converting data to CSV string without headers."""
        data = [
            ['Name', 'Age'],
            ['Alice', '30'],
            ['Bob', '25']
        ]

        result = self.csv.write_string(data, headers=False)

        assert 'Name,Age' in result
        assert 'Alice,30' in result

    def test_write_string_empty(self):
        """Test converting empty data to CSV string."""
        result = self.csv.write_string([])
        assert result == ""

    def test_count_rows(self):
        """Test counting rows in CSV file."""
        temp_file = self.create_temp_file(
            "name,age\nAlice,30\nBob,25\nCharlie,35"
        )

        count = self.csv.count_rows(temp_file)
        assert count == 3

    def test_count_rows_empty_file(self):
        """Test counting rows in empty file."""
        temp_file = self.create_temp_file("")
        count = self.csv.count_rows(temp_file)
        assert count == 0

    def test_count_rows_only_headers(self):
        """Test counting rows with only headers."""
        temp_file = self.create_temp_file("name,age\n")
        count = self.csv.count_rows(temp_file)
        assert count == 0

    def test_get_headers(self):
        """Test getting headers from CSV file."""
        temp_file = self.create_temp_file("name,age,city\nAlice,30,NYC")
        headers = self.csv.get_headers(temp_file)

        assert len(headers) == 3
        assert headers == ['name', 'age', 'city']

    def test_get_headers_empty_file(self):
        """Test getting headers from empty file."""
        temp_file = self.create_temp_file("")
        headers = self.csv.get_headers(temp_file)
        assert headers == []

    def test_append_dict_row(self):
        """Test appending dictionary row to CSV."""
        temp_file = self.create_temp_file("name,age\nAlice,30\n")

        new_row = {'name': 'Bob', 'age': '25'}
        self.csv.append(temp_file, new_row)

        result = self.csv.read(temp_file)
        assert len(result) == 2
        assert result[1]['name'] == 'Bob'
        assert result[1]['age'] == '25'

    def test_append_array_row(self):
        """Test appending array row to CSV."""
        temp_file = self.create_temp_file("Alice,30\n")

        new_row = ['Bob', '25']
        self.csv.append(temp_file, new_row)

        result = self.csv.read(temp_file, headers=False)
        assert len(result) == 2
        assert result[1] == ['Bob', '25']

    def test_append_to_empty_file(self):
        """Test appending to empty file."""
        temp_file = self.create_temp_file()

        new_row = {'name': 'Alice', 'age': '30'}
        self.csv.append(temp_file, new_row)

        # File should contain the row
        with open(temp_file, 'r') as f:
            content = f.read()
            assert 'Alice' in content

    def test_missing_keys_in_objects(self):
        """Test writing objects with missing keys."""
        temp_file = self.create_temp_file()

        data = [
            {'name': 'Alice', 'age': '30', 'city': 'NYC'},
            {'name': 'Bob', 'age': '25'},  # Missing 'city'
            {'name': 'Charlie', 'city': 'SF'}  # Missing 'age'
        ]

        self.csv.write(temp_file, data)
        result = self.csv.read(temp_file)

        assert len(result) == 3
        assert result[1].get('city', '') == ''  # Missing value becomes empty
        assert result[2].get('age', '') == ''

    def test_unicode_content(self):
        """Test CSV with Unicode characters."""
        temp_file = self.create_temp_file()

        data = [
            {'name': 'José', 'city': 'São Paulo'},
            {'name': '陈伟', 'city': '北京'}
        ]

        self.csv.write(temp_file, data)
        result = self.csv.read(temp_file)

        assert len(result) == 2
        assert result[0]['name'] == 'José'
        assert result[1]['name'] == '陈伟'

    def test_special_characters_in_values(self):
        """Test CSV with special characters (commas, quotes)."""
        temp_file = self.create_temp_file()

        data = [
            {'name': 'Alice, Jr.', 'description': 'Has "quotes"'},
            {'name': 'Bob\nNewline', 'description': 'Multiple\nlines'}
        ]

        self.csv.write(temp_file, data)
        result = self.csv.read(temp_file)

        assert len(result) == 2
        assert result[0]['name'] == 'Alice, Jr.'
        assert 'quotes' in result[0]['description']

    def test_large_dataset(self):
        """Test CSV with large dataset."""
        temp_file = self.create_temp_file()

        # Generate 1000 rows
        data = [
            {'id': str(i), 'name': f'User{i}', 'value': str(i * 10)}
            for i in range(1000)
        ]

        self.csv.write(temp_file, data)
        result = self.csv.read(temp_file)

        assert len(result) == 1000
        assert result[0]['id'] == '0'
        assert result[999]['id'] == '999'

    def test_write_mixed_array_types(self):
        """Test writing array with mixed value types."""
        temp_file = self.create_temp_file()

        data = [
            ['Alice', 30, True],
            ['Bob', 25, False]
        ]

        self.csv.write(temp_file, data, headers=False)
        result = self.csv.read(temp_file, headers=False)

        assert len(result) == 2
        assert result[0][0] == 'Alice'

    def test_semicolon_delimiter(self):
        """Test CSV with semicolon delimiter."""
        temp_file = self.create_temp_file()

        data = [
            {'name': 'Alice', 'age': '30'},
            {'name': 'Bob', 'age': '25'}
        ]

        self.csv.write(temp_file, data, delimiter=';')
        result = self.csv.read(temp_file, delimiter=';')

        assert len(result) == 2
        assert result[0]['name'] == 'Alice'


class TestCSVModuleMetadata:
    """Test module metadata and decorators."""

    def test_module_has_metadata(self):
        """Test that module has required metadata."""
        assert hasattr(CSV, '_ml_module_metadata')
        metadata = CSV._ml_module_metadata

        assert metadata.name == "csv"
        assert "file.read" in metadata.capabilities
        assert "file.write" in metadata.capabilities
        assert metadata.version == "1.0.0"

    def test_function_capabilities(self):
        """Test that functions have correct capability metadata."""
        csv_module = CSV()

        # Read operations
        assert hasattr(csv_module.read, '_ml_function_metadata')
        assert "file.read" in csv_module.read._ml_function_metadata.capabilities

        # Write operations
        assert hasattr(csv_module.write, '_ml_function_metadata')
        assert "file.write" in csv_module.write._ml_function_metadata.capabilities

        # Append requires both read and write
        assert hasattr(csv_module.append, '_ml_function_metadata')
        assert "file.read" in csv_module.append._ml_function_metadata.capabilities
        assert "file.write" in csv_module.append._ml_function_metadata.capabilities
