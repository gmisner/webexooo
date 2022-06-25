import base64
import json
import re
import sys
import time
from threading import Thread

import requests
from pyngrok import conf
from twilio.rest import Client

# Suppress error messages 
sys.stderr = open(os.devnull, "w")

# Create log file
log_file = open("/tmp/webexOOO.log", "w")
log_file.close()

# Authorization token(s)
webex_personal_token = "xxx1" # For option #1, #2 and #3
# webex_bot_token = "xxx2" # For option #1 and #2
# webex_integration_token = "xxx3" # For option #1 and #3
twilio_account_sid = "yyy"
twilio_auth_token = "zzz"
customer_email = "a@b.c"

def log_event_callback(log):
    with open('/tmp/logFile.log', 'a') as f:
        print(log, file=f) 
conf.get_default().log_event_callback = log_event_callback

def func0():
    url = "https://webexapis.com/v1/messages/direct?personEmail=" + customer-email
    headers = {
    'Authorization': 'Bearer ' + webex_personal_token, # For option #1, #2 and #3
# 'Authorization': 'Bearer ' + webex_bot_token, # For option #2
# 'Authorization': 'Bearer ' + webex_integration token, # For option #3
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    r_json = response.json()
    message = r_json["items"][1]["html"]
    TAG_RE = re.compile(r'<[^>]+>')
    message_parsed = TAG_RE.sub('', message)

    # Twilio Integration
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.api.account.messages.create(
        to="+1xxxxxxxxx",
        from_="+1yyyyyyyyy",
        body=message_parsed,
        media_url=['https://images.contentstack.io/v3/assets/bltd14fd2a03236233f/bltab28bd9a758b3f81/60d617644763af56bad5a0d5/download'])
  
def func1():
    #print("\n| --> Create ngrok tunnel")
    #ngrok.connect(5000, bind_tls=True)
    #tunnels = ngrok.get_tunnels()
    #tunnel_IP = re.findall(r'\"(.+?)\"', str(tunnels))[0]

    # Create webex webhook
    print("| --> Create webex webhook")
    url = "https://webexapis.com/v1/webhooks"
    payload = json.dumps({
    "resource": "messages",
    "event": "created",
    "filter": "roomType=direct",
    "targetUrl": tunnel_IP,
    "name": "Webex OOO"
    })
    headers = {
    'Authorization': 'Bearer ' + webex_personal_token,
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    r_json = response.json()
    print("| --> Listening...")
  
 def func2():
    while True:
        time.sleep(5)
        # Check webhook for new messages
        with open("/tmp/logFile.log", "r+") as file:
            result = (list(file)[-1])
            if "localhost:5000" in result:
                file.truncate(0)
                file.write(str('rolloverLine'))
                url = "http://localhost:4040/api/requests/http?limit=1"
                response = requests.request("GET", url)
                r_json = response.json()
                for i in range(0, len(r_json['requests'])):
                    encrypted_response = r_json["requests"][i]["request"]["raw"]
                    base64_bytes = encrypted_response.encode("ascii")
                    sample_string_bytes = base64.b64decode(base64_bytes)
                    sample_string = sample_string_bytes.decode("ascii")
                    match = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', sample_string)

                    if str(match).strip("[']") == customer_email:
                        func0()
                    elif str(match).strip("[']") in open('/tmp/webexOOO.log').read():
                        continue
                    else:
                        log_file = open("/tmp/webexOOO.log", "a")
                        log_file.write(str(match).strip("[']")+ "\n")
                        log_file.close()
                        with open("/tmp/webexOOO.log") as f:
                            personEmail = f.readlines()[-1]
                        url = "https://webexapis.com/v1/messages"
                        payload = json.dumps({
                        "toPersonEmail": "" + str(personEmail) + "",
                        "markdown": "** Webex OutOfOffice Auto Reply **\n\nThank you for your message. I’m out of the office and will be back at (Date of Return). During this period, I will have limited access to Webex chat.\n\nFor project X, please contact (Contacts Name) at (Contacts Email Address).\nFor project Y, please contact (Contacts Name) at (Contacts Email Address).\n\nIf you need immediate assistance, please contact me on my cell phone at (cell phone number).\n\nBest regards\nYossi M."
                        })
                        headers = {
                        'Authorization': 'Bearer ' + webex_personal_token, # For option #1, #2 and #3
                        # 'Authorization': 'Bearer ' + webex_bot_token, # For option #2
                        # 'Authorization': 'Bearer ' + webex_integration token, # For option #3
                        'Content-Type': 'application/json'
                        }
                        response = requests.request("POST", url, headers=headers, data=payload)
            else:
                pass
if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()
