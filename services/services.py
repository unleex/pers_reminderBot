def getlist_frommsg(text):
    list = text.split(sep='\n')
    return list

def format_list(a: list)->str:
    output: str=''
    j = 1
    for i in a:
        output += f'{j}. {i.capitalize()}\n'
        j += 1
    return output

