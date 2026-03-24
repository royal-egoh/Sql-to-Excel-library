from exlsql.app import Query
import os


q = Query("SELECT 'First Name', 'Last Name' , 'Age', 'Country' FROM Sheet1 WHERE Age > 30 AND Country = 'France'", excel_file="file_example_XLSX_100.xlsx")
x=q.parse()
print(q.to_excel(x, type="dict"))
