from exlsql.app import Query
import os

def run(label, sql, type="dict"):
    print(f"\n{'='*50}")
    print(f"TEST: {label}")
    print(f"SQL:  {sql}")
    print(f"{'='*50}")
    try:
        q = Query(sql, excel_file="file_example_XLSX_100.xlsx")
        parsed = q.parse()
        print(f"PARSED: {parsed}")
        result = q.to_excel(parsed, type=type)
        if type == "dict":
            print(f"ROWS RETURNED: {len(result)}")
            print(f"FIRST ROW: {result[0] if result else 'empty'}")
        elif type == "list":
            print(f"RESULT: {result}")
        elif type == "file":
            print(f"FILE WRITTEN: {result}")
            print(f"FILE EXISTS: {os.path.exists(result)}")
    except Exception as e:
        print(f"ERROR: {e}")

# SELECT specific columns
run("Select specific columns",
    "SELECT 'First Name', 'Last Name', Age, Country FROM Sheet1")

# SELECT *
run("Select all columns",
    "SELECT * FROM Sheet1")

# SELECT DISTINCT
run("Distinct countries",
    "SELECT DISTINCT Country FROM Sheet1")

# WHERE with number comparison
run("WHERE Age > 30",
    "SELECT 'First Name', 'Last Name', Age FROM Sheet1 WHERE Age > 30")

# WHERE with string equality
run("WHERE Country = France",
    "SELECT 'First Name', Country FROM Sheet1 WHERE Country = 'France'")

# WHERE with AND
run("WHERE Age > 30 AND Country = France",
    "SELECT 'First Name', 'Last Name', Age, Country FROM Sheet1 WHERE Age > 30 AND Country = 'France'")

# WHERE with OR
run("WHERE Country = France OR Country = United States",
    "SELECT 'First Name', Country FROM Sheet1 WHERE Country = 'France' OR Country = 'United States'")

# WHERE with IN
run("WHERE Country IN list",
    "SELECT 'First Name', Country FROM Sheet1 WHERE Country IN ('France', 'United States', 'China')")

# ORDER BY ASC
run("ORDER BY Age ASC",
    "SELECT 'First Name', Age FROM Sheet1 ORDER BY Age ASC")

# ORDER BY DESC
run("ORDER BY Age DESC",
    "SELECT 'First Name', Age FROM Sheet1 ORDER BY Age DESC")

# WHERE + ORDER BY
run("WHERE Age > 25 ORDER BY Age DESC",
    "SELECT 'First Name', Age, Country FROM Sheet1 WHERE Age > 25 ORDER BY Age DESC")

# Output to file
run("Output to file",
    "SELECT 'First Name', 'Last Name', Age FROM Sheet1 WHERE Age > 30",
    type="file")

# Output as list
run("Output as list",
    "SELECT Country FROM Sheet1 WHERE Age < 25",
    type="list")

# INVALID: bad file type
print(f"\n{'='*50}")
print("TEST: Invalid file type (expect ValueError)")
print(f"{'='*50}")
try:
    q = Query("SELECT * FROM Sheet1", excel_file="data.csv")
except ValueError as e:
    print(f"Caught expected error: {e}")

# INVALID: bad type parameter
run("Invalid type param (expect ValueError)",
    "SELECT * FROM Sheet1",
    type="json")