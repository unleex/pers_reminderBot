import re
from aiogram.types import Message
from aiogram.filters import BaseFilter
class IsTaskFormat(BaseFilter):
    def __call__(self, msg: Message):
        text: str = msg.text
        text = text.replace(' ','')
        time = re.findall(r'\d{1,2}:\d{1,2}',text)
        if len(time) > 1:
            return False
        if len(time) == 1:
            text = text.replace(time[0],'')
        
        return re.fullmatch(r'.[^:\-\n]+-.[^:\-\n]+',text) != None
    
class IsDayScheduleFormat(BaseFilter):
    def __call__(self, msg: Message):
        splitted = msg.text.split('\n')
        return sum([i.isalpha() for i in splitted]) == len(splitted)