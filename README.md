```markdown
## exlsql

Query Excel files using SQL syntax (DQL). `exlsql` lets you run SQL-like queries directly on `.xlsx` files using Python. Under the hood, it uses `pandas`, but exposes a simple SQL interface for filtering, selecting, and sorting data.

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
    "SELECT 'First Name', Age FROM Sheet1 WHERE Age > 25 ORDER BY Age DESC",
    excel_file="data.xlsx"
)

parsed = q.parse()
result = q.to_excel(parsed)

print(result)  # [{'First Name': 'Alice', 'Age': 32}, ...]
```

---

## How It Works

Every query follows two simple steps:

```python
q = Query(sql_string, excel_file="yourfile.xlsx")
parsed = q.parse()
result = q.to_excel(parsed, type="dict")  # optional type parameter
```

---

## Supported SQL Syntax

| Feature | Example |
|---------|---------|
| **SELECT columns** | `SELECT 'First Name', Age, Country FROM Sheet1` |
| **SELECT all** | `SELECT * FROM Sheet1` |
| **DISTINCT** | `SELECT DISTINCT Country FROM Sheet1` |
| **WHERE comparisons** | `SELECT * FROM Sheet1 WHERE Age > 30` |
| **WHERE AND / OR** | `SELECT * FROM Sheet1 WHERE Age > 30 AND Country = 'France'` |
| **WHERE IN** | `SELECT * FROM Sheet1 WHERE Country IN ('France', 'USA', 'China')` |
| **ORDER BY** | `SELECT * FROM Sheet1 ORDER BY Age DESC` |
| **Combined** | `SELECT 'First Name', Age FROM Sheet1 WHERE Age > 25 ORDER BY Age DESC` |

---

## Output Types

| Type | Returns |
|------|---------|
| `"dict"` (default) | List of row dictionaries — `[{'Name': 'Alice', 'Age': 32}, ...]` |
| `"list"` | Column-oriented dict — `{'Name': ['Alice', 'Bob'], 'Age': [32, 25]}` |
| `"file"` | Writes result to `yourfile_output.xlsx`, returns the path |

```python
# Dict format (default)
q.to_excel(parsed)
q.to_excel(parsed, type="dict")

# List format
q.to_excel(parsed, type="list")

# Save to file
path = q.to_excel(parsed, type="file")
print(path)  # data_output.xlsx
```

---

## Requirements

- `pandas`
- `openpyxl`

---

## Important Notes

- `FROM` refers to the **sheet name** inside the Excel file, not the filename
- Only `.xlsx` files are supported — other formats raise a `ValueError`
- Column names with spaces must be wrapped in quotes: `'First Name'` or `"First Name"`
- String values in `WHERE` must use single quotes: `WHERE Country = 'France'`
- Output files are written alongside the input as `filename_output.xlsx`

---

## Error Handling

```python
try:
    q = Query(sql, excel_file="data.csv")
except ValueError as e:
    print(e)  # Wrong file type, must be .xlsx
```

| Error | Cause |
|-------|-------|
| `Wrong file type` | File is not `.xlsx` |
| `Invalid sql syntax` | Missing `FROM` clause |
| `ORDER BY missing column` | Incorrect `ORDER BY` syntax |
| `Invalid Parameter` | Wrong output type |

---

## Limitations

- No `JOIN` support (single sheet only)
- No `GROUP BY` or aggregations
- Case-sensitive column names (depending on Excel data)
- Limited SQL parsing (not a full SQL engine)

---

## Why exlsql?

If you:
- Work with Excel frequently
- Know SQL but don't want database overhead
- Need quick data querying in scripts

Then `exlsql` gives you a clean bridge between Excel and SQL thinking.

---

## Contributing

Pull requests, issues, and suggestions are welcome.
```