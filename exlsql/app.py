class Query:
    def __init__(self, sql):
        self.sql = sql
        
        
    def parse(self):
        output = {'select': [], 'from': '', 'where': ''}
        sql_string = self.sql
        words = sql_string.split()
        i = 0
        while i < len(words):
            if words[i] == "SELECT":
                i += 1
                while i < len(words) and words[i] != "FROM":
                    clean_word = words[i].strip(",")
                    output['select'].append(clean_word)
                    i += 1

            elif words[i] == "FROM":
                i += 1
                if i < len(words):
                    output['from'] = words[i]
                i += 1

            elif words[i] == "WHERE":
                i += 1
                condition = []
                while i < len(words):
                    if words[i] in ("AND", "OR"):
                        output['where'].append(' '.join(condition))
                        condition = []
                    else:
                        condition.append(words[i])
                    i += 1
                if condition:
                    output['where'].append(' '.join(condition))
                break
            else:
                i += 1
                
                
    def to_excel(self, table_range, column):
        pass
    
    
    