'''
A project by @George-Adams1 using Phillips Hue:
This script turns the Phillips Hue Lights on and off
if my Gmail email address receives an email.
This project could be configured to turn on and off
for anything on the internet!

Telegram: george_adams1
'''

from phue import Bridge
import time
import imaplib
from variables import BRIDGE_IP, EMAIL_ADDRESS, PASSWORD # Importing personal information from another file

# Connecting to Gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ADDRESS, PASSWORD)
raw_email = ''

# Initializing and accessing light controls
def accessing_lights():
    global b
    b = Bridge(BRIDGE_IP)
    light_names = b.get_light_objects('name')
    return light_names

# Function that will turn lights on and off
def email_lights():
    lights = accessing_lights() # Accesing Hue Bridge

    for light in lights:
        if b.get_light(light, 'on') == True: # If light ON
            for light in lights:
                lights[light].on = False

            time.sleep(5) # Change value depending on how long you want light to be off

            for light in lights:
                lights[light].on = True
                lights[light].hue = 7000
                lights[light].saturation = 100

        elif b.get_light(light, 'on') == False: # If light OFF
            for light in lights:
                lights[light].on = True
                lights[light].hue = 7000
                lights[light].saturation = 100

            time.sleep(5) # Change value depending on how long you want light to be on

            for light in lights:
                lights[light].on = False

first = True

# Loop checks for if email was received
while True:
    if first == True: # Dealing with first time exception
        mail.list()
        mail.select('inbox')

        result, data = mail.search(None, 'ALL')
        ids = data[0]
        id_list = ids.split()
        latest_email_id = id_list[-1]
        result, data = mail.fetch(latest_email_id, "(RFC822)")  # Fetch the email body (RFC822) for the given ID

        raw_email = data[0][1]
        first = False

    previous_raw_email = raw_email # Previous email content will now be previous_raw_email content
    time.sleep(5)
    mail.list()
    mail.select('inbox')

    result, data = mail.search(None, 'ALL')
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    result, data = mail.fetch(latest_email_id, "(RFC822)")  # fetch the email body (RFC822) for the given ID

    raw_email = data[0][1]

    # Checking if email is the same as the previous email
    if previous_raw_email == raw_email:
        print('Same email')
        continue

    elif previous_raw_email != raw_email:
        print('Not the same email!')
        email_lights()
        continue
