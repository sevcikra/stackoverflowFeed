try:
    import urllib.request as urllib2
except:
    import urllib2
import io
import gzip
import json

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

import os
script_dir = os.path.dirname(__file__)
abs_file_path = os.path.join(script_dir, "auth/key.txt")

with open (abs_file_path, "r") as myfile:
    myKey = myfile.read().split('\n')

stackoverflowTag = "adobe-analytics"
url = "https://api.stackexchange.com/2.1/search?order=desc&sort=creation&tagged="+stackoverflowTag+"&site=stackoverflow"

req = urllib2.Request(url)
req.add_header('Accept-encoding', 'gzip')
response = urllib2.urlopen(req)

a = []

if response.info().get('Content-Encoding') == 'gzip':
    buf = io.BytesIO(response.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read().decode("utf-8")
    websiteData = json.loads(data)
    for i in range(1,5):
        a.append("http://stackoverflow.com/q/"+str(websiteData["items"][i]["question_id"]))

    htmlList = ""
    for item in a:
        htmlList += "<li>%s</li>\n" % item 

    html = """\
    <html>
      <head></head>
      <body>
        <ul>
          """+htmlList+"""
        </ul>
      </body>
    </html>
    """

msg = MIMEText(html, 'html')  

msg['Subject'] = 'StackOverflow: Adobe Analytics Weekly Feed'
msg['From'] = "from@example.com"
msg['To'] = "to@example.com"

# Send the message via local SMTP server.
s = smtplib.SMTP("smtp.gmail.com",587)
s.set_debuglevel(1)

s.ehlo()
s.starttls()
s.ehlo

try:
    s.login(myKey[0], myKey[1])
except SMTPAuthenticationError:
    print("SMTPAuthenticationError")

# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
