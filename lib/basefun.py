
# 
def isElemInList(Elem, List):
    if Elem in List:
        return True
    else:
        return False


# Invert dictionary by presering duplicates as lists
# { a:e, b:f, c:e, d:g } -> { e:[a,c], f:b, g:d }
def invDict(Dictionary):
    invDict = dict()
    for key, value in Dictionary.items():
        invDict.setdefault(value, list()).append(key)
    return invDict