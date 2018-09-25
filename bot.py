import json 
import requests
import time
import urllib
import api

TOKEN = "310204025:AAF1VsEFz-5iBv_VHnQxTfxRRTAAUS9cQFU"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

# def getDate():
#     now = datetime.datetime.now()
#     year = now.year
#     month = now.month
#     if month < 10:
#         month = "0"+str(month)
#     day = now.day
#     if day < 10:
#         day = "0"+str(day)
#     date = "{}-{}-{}".format(year, month, day)
#     return date


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]

            command = text.split(' ', 2)[0]
            arg1 = ''
            arg2 = ''

            if command[0] != '/':
                break;

            if command == "/score":
                arg1 = text.split(' ', 2)[1]
                try:
                    arg2 = text.split(' ', 2)[2]
                    if arg2 == "last":
                        text = api.teamLastScore(arg1)
                    else:
                        text = api.historicalTeamScore(arg1, arg2)
                except IndexError:
                    text = api.teamScore(arg1)

            if command == "/recap":
                try:
                    arg1 = text.split(' ',1)[1]
                    date = arg1
                    text = api.historicalDailySummary(date)
                except IndexError:
                    text = api.dailySummary()

            if command == "/goal":
                arg1 = text.split(' ',2)[1]
                print arg1
                arg2 = text.split(' ', 2)[2]
                print arg2
                if arg2.lower() == "last":
                    try:
                        text = api.goalHighlight(arg1, str(arg2))
                    except:
                        text = "No video for that goal found"
                else:
                    try:
                        text = api.goalHighlight(arg1, int(arg2))
                    except:
                        text = "No video for that goal found"
                chat = update["message"]["chat"]["id"]
                send_message(text, chat)
                break

            if command == "/standings":
                arg1 = text.split(' ', 1)[1]
                text = api.standings(arg1)
                chat = update["message"]["chat"]["id"]
                send_message_standings(text, chat)
                break

            if command == "/help":
                try:
                    arg1 = text.split(' ', 1)[1]
                    if arg1 == "goal":
                        text = api.goalHelp()
                except IndexError:
                    text = api.help()


            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message_standings(text, chat_id):
    # text = urllib.quote_plus(text)
    # text = text.encode("utf-8")
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def send_message(text, chat_id):
    # text = urllib.quote_plus(text)
    text = text.encode("utf-8")
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()