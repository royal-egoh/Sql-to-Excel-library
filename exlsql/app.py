import pandas as pd
import re
import os
import openpyxl


class Query:
    def __init__(self, sql, excel_file=None):
        if not excel_file or not excel_file.endswith(".xlsx") :
            raise ValueError("Wrong file type, must be .xlsx")
        self.sql = sql
        self.excel_file = excel_file

    def parse(self):
        try:
            output = {'select': [], 'from': '', 'where': ''}
            sql_string = self.sql
            # words = sql_string.split()
            words = words = re.findall(r'"[^"]*"|\'[^\']*\'|\S+', sql_string)
            i = 0
            while i < len(words):
                if words[i].upper() == "SELECT":
                    i += 1
                    if i >= len(words):
                        raise ValueError("Invalid SQL: incomplete SELECT clause")
                    if words[i] == "FROM":
                        output['select'].append("*")
                        break
                    while i < len(words) and words[i].upper() != "FROM":
                        if words[i] == "*":
                            output['select'].append(words[i])
                            break
                        column = words[i].rstrip(",")  # remove trailing comma
                        clean_word = column.strip('"').strip("'")
                        if clean_word:
                            output['select'].append(clean_word)
                        i += 1

                elif words[i].upper() == "FROM":
                    i += 1
                    if i < len(words):
                        output['from'] = words[i]
                        i += 1

                elif words[i].upper() == "WHERE":
                    i += 1
                    condition = []
                    while i < len(words):
                        if words[i] in ("AND", "OR"):
                            output['where'] += ' '.join(condition) + \
                                ' ' + words[i] + ' '
                            condition = []
                        else:
                            condition.append(words[i])
                        i += 1
                    if condition:
                        output['where'] += ' '.join(condition)
                    break
                # elif words[i] == "ORDER":
                #     while []
                #     i+=1

                else:
                    i += 1
            return output
        except Exception as e:
            raise ValueError(e)

    def to_excel(self, parsed, type=None):
        if not parsed['from']:
            raise ValueError("Invalid sql syntax")
        else:
            file = pd.read_excel(self.excel_file, sheet_name=parsed['from'])
        select_quer = []
        # SELECT QUERY
        if parsed['select'] == ['*'] or not parsed['select']:
            pass
        else:
            for i in parsed['select']:
                select_quer.append(f"{i}")
            file = file[select_quer]

        # WHERE QUERY
        if parsed['where']:
            parsed['where'] = re.sub(
                r'(?<![<>!])=(?!=)', '==', parsed['where'])

            file = file.query(parsed['where'])
            
        if type is None or type.lower().strip()=="dict":
            return file.to_dict(orient='records')
        elif type.lower().strip()=="file":
            name, ext = os.path.splitext(self.excel_file)
            output_path = f"{name}_output{ext}"
            file.to_excel(output_path, index=False)
            return output_path
        elif type.lower().strip()=="list":
            return file.to_dict(orient='list')
        else:
            raise ValueError("Invalid Parameter (list, dict, file)")
