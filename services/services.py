from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from datetime import datetime,date,time
import json

def edit_user_db(id: str, data: dict|list):
   db = json.load(open('db/db.json','r'))
   db[str(id)] = data
   json.dump(db, open('db/db.json','w'),indent='\t')


def get_day_frommsg(text):
  days= ['пн','вт',"ср",'чт',"пт","сб","вс"]
  text = text.strip()
  for day in days:
     if text.find(day) != -1:
        return day
  return None


def format_list(a: list)->str:
    output: str=''
    j = 1
    for i in a:
        output += f'{j}. {i.capitalize()}\n'
        j += 1
    return output
    
def are_equal(inst1,inst2):
    if inst1.__dict__.keys() != inst2.__dict__.keys():
        raise Exception('Instances must have same attributes')
    return inst1.__dict__.items() == inst2.__dict__.items()

def values(d: dict):
   return [i for i in d.values()]

def keys(d: dict):
   return [i for i in d.keys()]

def flatten_list(l):
   flattened=[]
   for i in l:
      for j in i:
         flattened.append(j)
   return flattened

def get_time_frommsg(text:str) -> tuple[int,int]:
   hour, minute = None, None
   colonpos = text.find(':')

   if text[colonpos-2].isdigit():
      hour = int(text[colonpos-2:colonpos])
   elif text[colonpos-1].isdigit():
      hour = int(text[colonpos-1])

   if text[colonpos+2].isdigit():
      minute = int(text[colonpos+1: colonpos+3])
   elif text[colonpos+1].isdigit(): 
      minute = int(text[colonpos-1])

   if hour is None and minute is None:
      return (None, None)
   else:
      return (int(hour), int(minute))


def normalize_duedate(dueday) -> tuple:
    days_en_ru = {'Mon':"пн",
                 'Tue':"вт",
                 'Wed':"ср",
                 'Thu':"чт",
                 'Fri':"пт",
                 'Sat':"сб",
                 'Sun':"вс"}
    day_to_num = {"пн":0,
                 "вт":1,
                 "ср":2,
                 "чт":3,
                 "пт":4,
                 "сб":5,
                 "вс":6}
    month_to_nday ={1: 31,
                     2: 29,
                     3: 31,
                     4: 30,
                     5: 31,
                     6: 30,
                     7: 31,
                     8: 31,
                     9: 30,
                     10:31,
                     11:30,
                     12: 31
                     }
    curr_weekday = date.strftime(datetime.today(),'%a')
    curr_weekday = day_to_num[days_en_ru[curr_weekday]]
    due_weekday = day_to_num[dueday]
    norm_dueday = int(date.today().strftime('%d')) - curr_weekday + due_weekday + 7*(due_weekday <= curr_weekday)

    curr_month = int(date.today().strftime('%m'))
    norm_duemonth = curr_month + (norm_dueday > month_to_nday[curr_month])

    curr_year = int(date.today().strftime('%y'))
    norm_dueyear = curr_year + (norm_duemonth > 12)

    norm_dueday %= month_to_nday[curr_month]
    norm_duemonth %= 12

    return (norm_dueyear,norm_duemonth,norm_dueday)

def find_and_replace(string, target, new):
  if string.find(target) != -1:
    string = string.replace(target, new)

  return string