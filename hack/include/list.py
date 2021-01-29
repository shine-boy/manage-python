
def find(lis, target):
    try:
        lis.index(target)
        return True
    except ValueError as v:
        return False
    return False


def findIndex(lis, target):
    index = -1
    try:
        index = lis.index(target)
    except ValueError as v:
        return index
    return index