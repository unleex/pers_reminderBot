from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from my_typing.typing import TasksCallbackFactory,Homework
def getlist_frommsg(text):
    list = text.split(sep='\n')
    return list

days= ['пн','вт',"ср",'чт',"пт","сб","вс"]
def extractday(text:str):
  text = text.strip()
  for day in days:
    if day in text:
      text = text.replace(day, "")
      return day, text
  return None, text


def getdict_frommsg(text:str):
  day, text= extractday(text)
  subject = text[:text.find("-")].strip().capitalize()
  task = text[text.find("-")+1:].strip().capitalize()
  return [{subject: task}, day]


def format_list(a: list)->str:
    output: str=''
    j = 1
    for i in a:
        output += f'{j}. {i.capitalize()}\n'
        j += 1
    return output

def gen_tasks_inline_kb(tasks: list[Homework]) -> list[InlineKeyboardButton]:
    butts: list[InlineKeyboardButton]
    butts=[]#target 
    for task in tasks:#gets list of hw
      butt = InlineKeyboardButton(
         text=list(task.subject_task.items())[0],#gets subject_task
         callback_data= TasksCallbackFactory(
            subject = list(task.subject_task.keys())[0],
            task = list(task.subject_task.values())[0],
            due = task.due,
            prefix='tasks'
         ).pack()#<tasks:subject:task:due
         )
      butts += butt
    return butts
   