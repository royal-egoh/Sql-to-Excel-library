# exlsql

Query Excel files using SQL syntax. Pass a SQL string and an `.xlsx` file — get a filtered, queried Excel file back.

---

## Installation

```bash
pip install exlsql
```

---

## Usage

```python
from exlsql import Query

q = Query("SELECT name, age FROM Sheet1 WHERE age > 30", excel_file="data.xlsx")
parsed = q.parse()
output = q.to_excel(parsed, type="dict")

print(output)  # data_output.xlsx
```

---

## Supported Syntax

| Feature | Example |
|---|---|
| Select columns | `SELECT name, age FROM Sheet1` |
| Select all | `SELECT * FROM Sheet1` |
| Filter rows | `WHERE age > 30` |
| Multiple conditions | `WHERE age > 30 AND city = 'Lagos'` |
| Column names with spaces | `SELECT "first name" FROM Sheet1` |

---

## Notes

- `FROM` refers to the **sheet name** inside the Excel file
- Only `.xlsx` files are supported
- The output is written to a new file — e.g. `data.xlsx` → `data_output.xlsx`
- String values in `WHERE` must be wrapped in single quotes: `city = 'New York'`

---

## Requirements

- pandas
- openpyxl