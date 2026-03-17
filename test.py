string = "SELECT me, you, name FROM royal WHERE age > 18 AND city = 'New York'"
words = string.split()

i = 0
while i < len(words):
    if words[i] == "SELECT":
        i += 1
        while i < len(words) and words[i] != "FROM":
            clean_word = words[i].strip(",")
            print(f"select: {clean_word}")
            i += 1

    elif words[i] == "FROM":
        i += 1
        if i < len(words):
            print(f"from: {words[i]}")
        i += 1

    elif words[i] == "WHERE":
        i += 1
        condition = []
        while i < len(words):
            if words[i] in ("AND", "OR"):
                print(f"where: {' '.join(condition)}")
                condition = []
            else:
                condition.append(words[i])
            i += 1
        if condition:
            print(f"where: {' '.join(condition)}")
        break
    else:
        i += 1