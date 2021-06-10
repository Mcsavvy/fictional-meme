import requests

url = "https://email-sender1.p.rapidapi.com/"

querystring = {
    "txt_msg": "This api works!",
    "to": "phishink5@gmail.com",
    "from": "Verified-Sec",
    "subject": "READ THIS NOW!!",
    "reply_to": "blvck.phish@gmail.com",
    "html_msg": "<html><body><b>test of the body</b></body></html>"}

headers = {
    'x-rapidapi-key': "15da5c2c18msha5bb6b2e33cae79p14d09djsn32b3ddb52ef6",
    'x-rapidapi-host': "email-sender1.p.rapidapi.com"
}

response = requests.request("POST", url, headers=headers, params=querystring)

print(response.text)
