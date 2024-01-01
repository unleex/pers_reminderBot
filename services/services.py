def getlist_frommsg(text):
    list = text.split(sep='\n')
    return list
days=['пн','вт','ср','чт','пт','сб','вс']

def popday_frommsg(days:list,msg:str) -> str:
    for day in days:
        if day in msg:
            msg = msg.replace(day,'')
            return day,msg
    return None, msg
        
def getdict_frommsg(text:str) -> list[dict,str]:
    day,text=popday_frommsg(days,text)
    subject = text[:text.find('-')].strip()
    task = text[text.find('-')+1:].strip()
    return {subject: task},day
def format_list(a: list)->str:
    output: str=''
    j = 1
    for i in a:
        output += f'{j}. {i.capitalize()}\n'
        j += 1
    return output

