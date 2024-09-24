import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication 
from bs4 import BeautifulSoup

load_dotenv()

sender = os.getenv('user')
#send_to = 'gmauthority@motrolix.com'
send_to = ['jesusmanuelv1989@gmail.com','jesusvergara890109@gmail.com']
topic = 'Application for Front-End Developer Position'

msg = MIMEMultipart()
msg['subject'] = topic
msg['from'] = sender
msg['To'] = ', '.join(send_to) 


with open('email.html', 'r') as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')


images = ['691deedb-42f3-4ada-ae6d-4d53b2fa8c43.png', 'linkedin.png',
          'icons8-notion-250.png', 'icons8-docker-240.png',
          'icons8-github-480.png', 'prog.png', 'Beefree-logo.png']

for image_name in images:
    image_path = os.path.join('images', image_name)
    with open(image_path, 'rb') as img_file:
        img_data = img_file.read()
        img_mime = MIMEImage(img_data, name=image_name)
        img_mime.add_header('Content-ID', f'<{image_name}>')
        msg.attach(img_mime)

        img_tag = soup.find('img', src=f'images/{image_name}')
        if img_tag:
            img_tag['src'] = f'cid:{image_name}' 


html_updated = str(soup)
msg.attach(MIMEText(html_updated, 'html'))


pdf_filename = 'Jesus_Vergara_CV.pdf'  
pdf_path = os.path.join('', pdf_filename)  

with open(pdf_path, 'rb') as pdf_file:
    pdf_mime = MIMEApplication(pdf_file.read(), name=pdf_filename)
    pdf_mime['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    msg.attach(pdf_mime)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender, os.getenv('pass'))
server.sendmail(sender, send_to, msg.as_string())
server.quit()
