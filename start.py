import requests
import os
import time
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1
from threading import Thread
from requests.utils import quote
from subprocess import *
from credentials import *

auth = OAuth1(consumer_key, consumer_key_secret, access_token, access_token_secret)

def findAndKillNgrokProcess():
    pipe = Popen("ps ax | grep ngrok", shell=True, stdout=PIPE).stdout
    output = pipe.read()
    lines = output.splitlines()
    for line in lines:
        line = str(line)
        if line.__contains__('ngrok http'):
            line = line[3:]
            pid = ""
            i = 0
            while line[i].isdigit():
                pid += line[i]
                i += 1
            print("found ngrok thread with pid : " + pid)
            os.system('kill ' + pid)
            print('process killed')
            return
    print("no process found")

def findAndKillFlaskProcess():
    pipe = Popen("lsof -i:5000", shell=True, stdout=PIPE).stdout
    output = str(pipe.read())

    if(output.__contains__('Python')):
        output = output.split("Python  ",1)[1]
        pid = ""
        i = 0
        while(output[i].isdigit()):
            pid += output[i]
            i+=1
        print("found flask thread with pid : "+pid)
        os.system('kill ' + pid)
        print('process killed')
    else:
        print("no process found")

def start_thread_ngrok():
    os.system("./ngrok http 5000 > /dev/null &")

def start_thread_flask():
    os.system("env FLASK_APP=bot.py flask run &")    # & to run command in background

def tryLocalhostConnection():
    print("trying to connect to localhost...")
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
    except:
        return None
    return response.json()

threadNgrok = Thread(target=start_thread_ngrok)
threadFlask = Thread(target=start_thread_flask)

print('\nsearching for running flask processes...')     # killing old threads if present
findAndKillFlaskProcess()
print('\nsearching for running ngrok processes...')
findAndKillNgrokProcess()

print('\nstarting ngrok thread...')
threadNgrok.start()
print('\nstarting flask thread...')
threadFlask.start()

response = None
while response is None or not response['tunnels']:      # trying to connect to localhost to get the new ngrok url
    time.sleep(0.01)
    response = tryLocalhostConnection()

ngrok_url = response['tunnels'][0]['public_url']
print('ngrok url : '+ngrok_url)

threadNgrok.join()
threadFlask.join()

print('\ngetting bearer token...')
response = requests.post('https://api.twitter.com/oauth2/token', auth=HTTPBasicAuth(consumer_key, consumer_key_secret), data={'grant_type':'client_credentials'})

bearer_token = response.json()['access_token']
print("bearer token : "+bearer_token)

print('\nverifying active webhooks...')
response = requests.get('https://api.twitter.com/1.1/account_activity/all/webhooks.json',headers={'Authorization': 'Bearer ' + bearer_token})

if response.json()['environments'][0]['webhooks']:      # there are active webhooks
    webhook_id = response.json()['environments'][0]['webhooks'][0]['id']
    print("active webhook_id : "+webhook_id)

    response = requests.delete('https://api.twitter.com/1.1/account_activity/all/'+env_name+'/webhooks/'+str(webhook_id)+'.json',auth=auth)
    print("deleted webhook")
else:
    print("no active webhooks")


ngrok_url = quote(ngrok_url+'/webhooks/twitter', safe='')       # encoding of the ngrok_url
print('\nassociating the ngrok url to the account activity...')
response = requests.post('https://api.twitter.com/1.1/account_activity/all/'+env_name+'/webhooks.json?url='+ngrok_url,auth=auth)
webhook_id = response.json()['id']
print('\nnew registred webhood id : '+webhook_id)

response = requests.post('https://api.twitter.com/1.1/account_activity/all/'+env_name+'/subscriptions.json',auth=auth)      # subscribing the account activity to the webhook

if response.status_code>=200 and response.status_code<300:
    print("subscribed to webhook")
else:
    print("error in subscription")


user_input = ''
while user_input != 'exit':
    user_input = input('webhook is running (exit to close)\n')
findAndKillFlaskProcess()
findAndKillNgrokProcess()
