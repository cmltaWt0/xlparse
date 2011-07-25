#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
xlparse.py have a GUI interface and give ability to choise xls file 
to transform it to txt file by prepared algoritm. By using
send_mail.py module xlparse allow to send mail with some attached file.
Can attach src (xls file) of result (txt file).
It's can send mail to diff recipients and CC recipients(config in 
conf/base.cfg file).
But this program not universal now, it's for my use.
Program alow to use some open smtp sever.
Xlparse tested on python <=2.7 because xlrd module not allowed for
python3 now.
"""
import os
from Tkinter import *
import tkFileDialog
import fileinput
from xlrd import open_workbook, cellname

day = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
for i in range(10,32):
    day.append(str(i))

begin = ['(100)', '(111)', '(112)', '(121)', '(122)', '(201)', '(202)', '(301)', '(302)', '(400)']
sheet0 = 0
op = ''

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

def iter_write_section(_list,):
    for i in _list:
       tex.insert(END,str(i))
       tex.insert(END,':')
    tex.insert(END,'0:')
    tex.insert(END,'\n')   

def transformation(event):
    _date = ent.get()
    
    if op:    
        if _date in day:
            book = open_workbook(op)
    
            global sheet0
            sheet0 = book.sheet_by_index(0)
   
            tex.delete(1.0,END)
  
            tex.insert(END,'((//30902:1107:36627473:++\n')
            i = 0
            num = 2
            while i < 10:
                _list = [begin[i]] + [_date] + parse(num)
                iter_write_section( _list)
                i += 1
                num += 1

            tex.insert(END,'==))')
        else:
            tex.delete(1.0,END)
            tex.insert(END,'Число должно быть в диапазоне от 01 до 31\nЧисла с 1-го по 9-е пишутся как 01, 02 и т.д.')
    
    else:
        tex.delete(1.0,END)
        tex.insert(END,'Сначала откройте исходный файл xls')

def mail_src(event):
    from modules.send_mail import send_mail
    from modules.conf_fetcher import fetcher
  
    a = fetcher() #take a dict with conf setting
    if op:
        a ['files'] = [op]
 
    send_mail(**a)

    tex.delete(1.0,END)
    tex.insert(END,'Файл ')
    tex.insert(END, op)
    tex.insert(END, ' отправлен')

def mail_res(event):
    from modules.send_mail import send_mail
    from modules.conf_fetcher import fetcher

    tmp = 'tmp/tmp_file.txt'
    a = fetcher() #take a dict with conf setting
    
    letter = tex.get(1.0,END)
    f = open(tmp, "w")
    f.write(letter)
    f.close()
    
    a ['files'] = [tmp]

    send_mail(**a)

    tex.delete(1.0, END)
    tex.insert(END, 'Результат сохранен во временный файл ')
    tex.insert(END, 'tmp/tmp_file.txt')
    tex.insert(END, ' и отправлен по почте')

def _open():
    global op
    op = tkFileDialog.askopenfilename()
    filename = os.path.basename(op)
    tex.delete(1.0,END)
    tex.insert(END,'Открыт файл ')
    tex.insert(END, filename)
    tex.insert(END, '.\nТеперь введите день, для которого будет выполнено преобразование')

def _save():
    sa = tkFileDialog.asksaveasfilename()
    letter = tex.get(1.0,END)
    f = open(sa,"w")
    f.write(letter)
    f.close()

def _close():
    root.destroy()

def _help():
     win = Toplevel(root)
     lab = Label(win, text="Вам необходимо ввести в поле день, отчет за какой необходимо преобразовать.\nЧисло необходимо вводить в следующем формате - '01, 02, 03 и т.д.'. После этого нажать на кнопку Преобразовать.\nЕсли вы правильно ввели число и файл в формате xls существует, то он будет преобразован в формат txt\nи результат преобразования появится на экране. Файл txt будет автоматически сохранен.")
     lab.pack()

def _about():
     win = Toplevel(root)
     lab = Label(win, text="Эта программа преобразовывает xls файл \n в txt формат специальной разметкой.")
     lab.pack()

root = Tk()

root.title('Xlparse')
m = Menu(root)
root.config(menu=m)
fm = Menu(m)
m.add_cascade(label="File", menu=fm)
fm.add_command(label="Open", command = _open)
fm.add_command(label="Save", command = _save)
fm.add_command(label="Exit", command = _close)
 
hm = Menu(m)
m.add_cascade(label="Help", menu=hm)
hm.add_command(label="Help", command = _help)
hm.add_command(label="About", command = _about)
 
 
fra1 = Frame(root, width=500, height=30, bd = 5)
fra2 = Frame(root, width=500, height=100, bd = 5)
fra3 = Frame(root, width=500, height=500, bd = 5)
 
lab1 = Label(fra1, text="Откройте xls файл, который хотите преобразовать\nВведите в поле справа день месяца, для которого\nформируется текстовый файл. Будьте внимательны\nвыбирайте файл и день месяца одинаковые.\nС 1-го по 9-е числа вводятся как 01, 02 и т.д.", font="Arial 10")
lab2 = Label(fra3, text="Если введённое чило не верно, его можно сменить и снова выполнить\nпреобразование кнопкой Transform, не открывая файл второй раз\nДля сохранения результата выберите File->Save.", font="Arial 10")
ent = Entry(fra1, width=4)
but1 = Button(fra1, text = "Преобразовать")
but2 = Button(fra3, text = "Отправить исходник")
but3 = Button(fra3, text = "Отправить результат")
tex = Text(fra2, width=60, height=12, font="12", wrap=WORD)
 
lab1.grid(row = 0, column = 0)
ent.grid(row = 0, column = 1, padx=20)
but1.grid(row = 1, column = 1, padx=20)
tex.grid(row = 0, column = 0)
lab2.grid(row = 0, column = 0)
but2.grid(row = 0, column = 1)
but3.grid(row = 1, column = 1)
 
fra1.pack()
fra2.pack()  
fra3.pack()

but1.bind("<Button-1>", transformation)
but2.bind("<Button-1>", mail_src)
but3.bind("<Button-1>", mail_res)
    
root.mainloop() 
