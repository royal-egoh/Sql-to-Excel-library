from exlsql.app import Query
import os


q = Query("SELECT Age FROM Sheet1 WHERE Age > 30", excel_file="file_example_XLSX_100.xlsx")
x=q.parse()
q.to_excel(x)
