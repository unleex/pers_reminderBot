from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from datetime import datetime
from my_typing.typing import TasksCallbackFactory,Homework
def getlist_frommsg(text):
    list = text.split(sep='\n')
    return list


def get_time_frommsg(text:str) -> tuple:
  hour, minute = 9, 0
  colonpos = text.find(':')

  if text[colonpos-2].isdigit():
    hour = int(text[colonpos-2:colonpos])
  elif text[colonpos-1].isdigit():
    hour = int(text[colonpos-1])

  if text[colonpos+2].isdigit():
     minute = int(text[colonpos+1: colonpos+3])
  elif text[colonpos+1].isdigit(): 
     minute = int(text[colonpos-1])
  return (int(hour), int(minute))

def get_subject_task_frommsg(text:str):

  subject = text[:text.find("-")].strip().capitalize()
  task = text[text.find("-")+1:].strip().capitalize()
  return (subject, task)


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
def _format_text(subject_task: dict) -> str:
   subject = list(subject_task.keys())[0]
   task = list(subject_task.values())[0]
   return f'{subject}: {task}'

def gen_tasks_inline_kb(tasks: list[Homework]) -> list[InlineKeyboardButton]:
    butts: list[InlineKeyboardButton]
    butts=[]
    for task in tasks:
      butt = InlineKeyboardButton(
         text=_format_text(task.subject_task),
         callback_data = TasksCallbackFactory(
            subject = list(task.subject_task.keys())[0],
            task = list(task.subject_task.values())[0],
            due = task.due
         ).pack()
         )
      butts.append(butt)
    return butts
    
def are_equal(inst1,inst2):
    if inst1.__dict__.keys() != inst2.__dict__.keys():
        raise Exception('Attributes must have same attributes')
    return inst1.__dict__.items() == inst2.__dict__.items()

def values(d: dict):
   return [i for i in d.values()]

def flatten_list(l):
   flattened=[]
   for i in l:
      for j in i:
         flattened.append(j)
   return flattened

def format_due(due):
   
   return due

def find_and_replace(string, target, new):
  if string.find(target) != -1:
    string = string.replace(target, new)

  return string