from pandas import DataFrame
class Schedule():
    editing: bool
    creating: bool
    d = {'Понедельник':[], 'Вторник':[],'Среда':[],'Четверг':[],'Пятница':[],'Суббота':[],'Воскресенье':[]}
    schedule = DataFrame(data=d)
class Scheduletmp():
    editing: bool
    creating: bool
    d = {'tmp1':[], 'tmp2':[],'tmp3':[],'tmp4':[],'tmp5':[],'tmp6':[],'tmp7':[]}
    tmpschedule = DataFrame(data=d)