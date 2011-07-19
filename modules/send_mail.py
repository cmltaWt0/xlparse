from smtplib import SMTP
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from email.header import Header

def send_mail(**a):
  assert type(a['send_to'])==list
  assert type(a['files'])==list

  msg = MIMEMultipart()
  msg['From'] = a['send_from']
  msg['To'] = COMMASPACE.join(a['send_to'])
  msg['cc'] = COMMASPACE.join(a['send_cc'])
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = Header(a['subject'], 'utf-8')
  #need to add test to empty a[text] - causes crash
  msg.attach( MIMEText(a['text'].encode("utf-8"), _subtype='plain', _charset='utf-8') )

  for f in a['files']:
    part = MIMEBase('application', "octet-stream", charset='utf-8')
    part.set_payload( open(f,"rb").read() )
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', "%s" % os.path.basename(f)))  
    msg.attach(part)
  try:
    smtp = SMTP(a['server'])
    smtp.sendmail(a['send_from'], a['send_to']+a['send_cc'], msg.as_string())
    smtp.close()
  except SMTPException:
    pass
