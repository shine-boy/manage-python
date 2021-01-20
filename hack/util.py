from hack.include.myIterator import MyIterator

# "%Y-%m-%d %H:%M:%S"
def isNull(obj):
    if obj is None:
        return True
    if obj=="":
        return True
    return False

def getKeys_dic(obj,keys=[]):
    result={}
    for key in keys:
        result[key]=obj[key]
    return result
