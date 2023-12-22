def getlist_frommsg(text):
    list = text.split(sep='\n')
    return list

def statecheck(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('activate'):
            result = func(*args, **kwargs)
            return result
        else:
            return None
    return wrapper