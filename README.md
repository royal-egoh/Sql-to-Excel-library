# exlsql

Query Excel files using SQL syntax. No database, no server — just point it at a `.xlsx` file, write a SQL string, and get your data back.

---

## Installation

```bash
pip install exlsql
```

---

## Quick Start

```python
from exlsql import Query

q = Query(
    "SELECT 'First Name', 'Last Name', Age FROM Sheet1 WHERE Age > 30",
    excel_file="data.xlsx"
)

result = q.to_excel(q.parse(), type="dict")
```

---

## Usage

Every query follows the same two steps:

```python
q = Query(sql_string, excel_file="yourfile.xlsx")
parsed = q.parse()
result = q.to_excel(parsed, type="dict")  # or "list" or "file"
```

---

## Supported SQL Syntax

### SELECT columns
```sql
SELECT 'First Name', Age, Country FROM Sheet1
```

### SELECT all columns
```sql
SELECT * FROM Sheet1
```

### DISTINCT
```sql
SELECT DISTINCT Country FROM Sheet1
```

### WHERE — comparisons
```sql
SELECT * FROM Sheet1 WHERE Age > 30
SELECT * FROM Sheet1 WHERE Age >= 18
SELECT * FROM Sheet1 WHERE Country = 'France'
```

### WHERE — AND / OR
```sql
SELECT * FROM Sheet1 WHERE Age > 30 AND Country = 'France'
SELECT * FROM Sheet1 WHERE Country = 'France' OR Country = 'United States'
```

### WHERE — IN
```sql
SELECT * FROM Sheet1 WHERE Country IN ('France', 'United States', 'China')
```

### ORDER BY
```sql
SELECT 'First Name', Age FROM Sheet1 ORDER BY Age ASC
SELECT 'First Name', Age FROM Sheet1 ORDER BY Age DESC
```

### Combined
```sql
SELECT 'First Name', Age, Country FROM Sheet1
WHERE Age > 25 AND Country = 'France'
ORDER BY Age DESC
```

---

## Return Types

| type | Returns |
|---|---|
| `"dict"` (default) | List of row dicts — `[{'Name': 'Alice', 'Age': 32}, ...]` |
| `"list"` | Column-oriented dict — `{'Name': ['Alice', ...], 'Age': [32, ...]}` |
| `"file"` | Writes result to `yourfile_output.xlsx`, returns the path |

```python
# dict (default)
q.to_excel(parsed)
q.to_excel(parsed, type="dict")

# list
q.to_excel(parsed, type="list")

# file
path = q.to_excel(parsed, type="file")
print(path)  # data_output.xlsx
```

---

## Notes

- `FROM` refers to the **sheet name** inside the Excel file, not the filename
- Only `.xlsx` files are supported — passing any other format raises a `ValueError`
- Column names with spaces must be wrapped in single or double quotes: `'First Name'` or `"First Name"`
- String values in `WHERE` must be wrapped in single quotes: `WHERE Country = 'France'`
- Output files are always written alongside the input file as `filename_output.xlsx`

---

## Error Handling

```python
try:
    q = Query(sql, excel_file="data.csv")
except ValueError as e:
    print(e)  # Wrong file type, must be .xlsx
```

Common errors:
- Wrong file type → `ValueError: Wrong file type, must be .xlsx`
- Missing FROM → `ValueError: Invalid sql syntax`
- Bad ORDER BY → `ValueError: ORDER BY missing column`
- Invalid return type → `ValueError: Invalid Parameter (list, dict, file)`

---

## Requirements

- `pandas`
- `openpyxl`