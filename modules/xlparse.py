# -*- coding: utf-8 -*-
"""
Purpose of this module is to convert xls file to txt.
Working only via Python < 3.0
"""
import os
import sys
from xlrd import open_workbook, cellname
####################################################################
#need to going to module
from datetime import date
from calendar import monthrange

date_ = date.today()

#calculate latest day in last mounth
if date_.day == 1:
    mrange_ = monthrange(date_.year, date_.month - 1)
    date_ = date_.replace(month = date_.month - 1, day = mrange_[1])
    date_file = date_.strftime("%d.%m.%Y")
    date_dir = date_.strftime("%m.%Y")
#calculate yesterday's day
else:
    date_ = date_.replace(day = date_.day -1)
    date_file = date_.strftime("%d.%m.%Y")
    date_dir = date_.strftime("%m.%Y")
####################################################################

_date = sys.argv[1]
file_name = 'Укрнедраресурсы-' + _date + '.07.2011'
book = open_workbook('path_to_xls_dir' + file_name + '.xls')
sheet0 = book.sheet_by_index(0)

def parse (row_num):
    _list = []
    a = sheet0.row_values(row_num, 25, 26)
    for i in a:
        b = int(i)
        _list.append(b)
    c = sheet0.row_values(row_num, 1, 25)
    for i in c:
        d = int(i)
        _list.append(d)
    return _list

file_out = '/home/user/path_to_program_folder/' + file_name + '.txt'
os.system('touch ' + file_out)

f_out = open(file_out,'w')
def iter_write_section(f_out, _list,):
    for i in _list:
       f_out.write(str(i))
       f_out.write(':')
    f_out.write('0:')
    f_out.write('\r\n')    

#need to going to conf file
begin = ['(100)', '(111)', '(112)', '(121)', '(122)', '(201)', '(202)', '(301)', '(302)', '(400)']
f_out.write('((//30902:1107:36627473:++\r\n')

i = 0
num = 2    
while i < 10:
    _list = [begin[i]] + [_date] + parse(num)
    iter_write_section(f_out, _list)
    i += 1
    num += 1 

f_out.write('==))')

f_out.close()
