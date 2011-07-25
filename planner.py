#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The purpose of the programm is to organize some repeatedly job's.
Such as sending message (now) or saving some generated file(need to release).
This python program allows us to send a mail with included files.
Now, this program calculate the current date and include to mail
file which contain yesterday's date.
It's can send mail to diff recipients and CC recipients.
But this program not universal now, it's for my use.
Program alow to use some open smtp sever.
Tested on python 3.2.
Not work on python < 3 because module email and configparser change
its syntax.
"""
from modules.send_mail import send_mail
from modules.conf_fetcher import fetcher

if __name__ == "__main__":
    a = fetcher() #take a dict with conf setting
    send_mail(**a)
