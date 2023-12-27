class SyntaxError(Exception):
    pass


keywords = {"auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "for", "goto",
            "if", "int", "long", "register", "return", "short", "signed",
            "sizeof", "static", "struct", "switch", "typedef", "union",
            "unsigned", "void", "volatile", "while", "printf", "scanf", "%d", "include", "stdio.h", "main"}

operators = {"+", "-", "*", "/", "<", ">", "=",
             "<=", ">=", "==", "!=", "++", "--", "%"}

delimiters = {'(', ')', '{', '}', '[', ']', '"', "'", ';', '#', ',', ''}


def detect_keywords(text):
    arr = []
    for word in text:
        if word in keywords:
            arr.append(word)
    return list(set(arr))


def detect_operators(text):
    arr = []
    for word in text:
        if word in operators:
            arr.append(word)
    return list(set(arr))


def detect_delimiters(text):
    arr = []
    for word in text:
        if word in delimiters:
            arr.append(word)
    return list(set(arr))


def detect_num(text):
    arr = []
    for word in text:
        try:
            a = int(word)
            arr.append(word)
        except:
            pass
    return list(set(arr))


def detect_identifiers(text):
    k = detect_keywords(text)
    o = detect_operators(text)
    d = detect_delimiters(text)
    n = detect_num(text)
    not_ident = k + o + d + n
    arr = []

    # Split words with attached parentheses
    split_text = [word.strip('(){}[]";,') for word in text]

    for word in split_text:
        if word and word not in not_ident:
            arr.append(word)

    return arr


def lexical_analysis(file_path):
    with open(file_path) as t:
        text = t.read().split()

    print("Lexical Analysis:")
    print("Keywords: ", detect_keywords(text))
    print("Operators: ", detect_operators(text))
    print("Delimiters: ", detect_delimiters(text))
    print("Identifiers: ", detect_identifiers(text))
    print("Numbers: ", detect_num(text))


def first_and_follow(grammar):
    rules = {}
    terms = []

    for i in grammar:
        temp = i.split("=")
        terms.append(temp[0])
        try:
            rules[temp[0]] += [temp[1]]
        except:
            rules[temp[0]] = [temp[1]]

    terms = list(set(terms))

    leads = {}
    trails = {}

    for i in terms:
        s = [0]
        for j in rules[i]:
            s += leading(j, rules, i, terms)
        s = set(s)
        s.remove(0)
        leads[i] = s
        s = [0]
        for j in rules[i]:
            s += trailing(j, rules, i, terms)
        s = set(s)
        s.remove(0)
        trails[i] = s

    for i in terms:
        print("LEADING("+i+"):", leads[i])
    for i in terms:
        print("TRAILING("+i+"):", trails[i])


def leading(gram, rules, term, terms):
    s = []
    if gram[0] not in terms:
        return gram[0]
    elif len(gram) == 1:
        return [0]
    elif gram[1] not in terms and gram[-1] is not term:
        for i in rules[gram[-1]]:
            s += leading(i, rules, gram[-1], terms)
            s += [gram[1]]
        return s


def trailing(gram, rules, term, terms):
    s = []
    if gram[-1] not in terms:
        return gram[-1]
    elif len(gram) == 1:
        return [0]
    elif gram[-2] not in terms and gram[-1] is not term:
        for i in rules[gram[-1]]:
            s += trailing(i, rules, gram[-1], terms)
            s += [gram[-2]]
        return s

    s = []
    if gram[-1] not in terms:
        return gram[-1]
    elif len(gram) == 1:
        return [0]
    elif gram[-2] not in terms and gram[-1] is not start:
        for i in rules[gram[-1]]:
            s += trailing(i, rules, gram[-1], start)
            s += [gram[-2]]
        return s


# Test the combined script
file_path = 'e1-example.txt'
grammar = ["E=E+T", "E=T", "T=T*F", "T=F", "F=(E)", "F=i"]

lexical_analysis(file_path)
print("\nFirst and Follow Set:")
first_and_follow(grammar)
