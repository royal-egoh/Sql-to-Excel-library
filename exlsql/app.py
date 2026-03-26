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
            output = {'select': [],'distinct':False, 'from': '', 'where': '', 'order':''}
            sql_string = self.sql
            # words = sql_string.split()
            words = re.findall(r'"[^"]*"|\'[^\']*\'|\S+', sql_string)
            i = 0
            while i < len(words):
                if words[i].upper() == "SELECT":
                    i += 1
                    if i >= len(words):
                        raise ValueError("Invalid SQL: incomplete SELECT clause")
                    if words[i].upper() == "DISTINCT":   #!TO BE ADDED
                        output['distinct'] = True
                        i+=1
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
                    parsed_where = []
                    sql_bool_map = {"AND": "and", "OR": "or", "NOT": "~"}
                    in_lists = {}  # store IN lists for df.query() @var syntax
                    while i < len(words):
                        word = words[i].upper()
                        if word == "IN":
                            col = condition.pop()
                            i += 1
                            if i >= len(words) or not words[i].startswith("("):
                                raise ValueError("Invalid IN syntax")
                            values = []
                            while True:
                                val = words[i].lstrip("(").rstrip(",)")
                                if val:
                                    values.append(val.strip('"').strip("'"))
                                if words[i].rstrip(",").endswith(")"):
                                    break
                                i += 1
                            var_name = f"_in_{col}"
                            in_lists[var_name] = values
                            parsed_where.append(f"{col} in @{var_name}")
                        elif word in sql_bool_map:
                            if condition:
                                parsed_where.append(' '.join(condition))
                                condition = []
                            parsed_where.append(sql_bool_map[word])
                        else:
                            condition.append(words[i])
                        i += 1
                    if condition:
                        parsed_where.append(' '.join(condition))
                    output['where'] = ' '.join(parsed_where)
                    output['in_lists'] = in_lists
                
                elif words[i].upper() == "ORDER":
                    i+=1
                    if i<len(words) and words[i].upper() == 'BY':
                        i+=1
                        if i >= len(words):
                            raise ValueError("ORDER BY missing column")
                        
                        col = words[i].rstrip(",").strip('"').strip("'")
                        i += 1
                        direction = 'ASC'
                        if i < len(words) and words[i].upper() in ('ASC', 'DESC'):
                            direction = words[i].upper()
                            i += 1
                        output['order'] = (col, direction)
                    else:
                        raise ValueError("Invalid syntax")

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
        # WHERE QUERY
        if parsed['where']:
            parsed['where'] = re.sub(
                r'(?<![<>!])=(?!=)', '==', parsed['where'])

            file = file.query(parsed['where'], local_dict=parsed.get('in_lists', {}))
            
        # SELECT QUERY
        if parsed['select'] == ['*'] or not parsed['select']:
            pass
        else:
            for i in parsed['select']:
                select_quer.append(f"{i}")
            file = file[select_quer]
            
        if parsed['distinct']:#?DISTINCT
            if parsed['select'] == ['*'] or not parsed['select']:
                file = file.drop_duplicates()
            else:
                file = file.drop_duplicates(subset=parsed['select'])
        
        if parsed['order']:#?Order by
            col, direction = parsed['order']
            ascending = True if direction == 'ASC' else False
            file = file.sort_values(by=col, ascending=ascending)
            
            
        #?Return types
        if type is None or type.lower().strip()=="dict":
            return file.to_dict(orient='records')
        elif type.lower().strip()=="file":
            name, ext = os.path.splitext(self.excel_file)
            output_path = f"{name}_output{ext}"
            file.to_excel(output_path, index=False)
            return output_path
        elif type.lower().strip()=="list":
            return f"{parsed['from']} = {file.to_dict(orient='list')}"
        else:
            raise ValueError("Invalid Parameter (list, dict, file)")
