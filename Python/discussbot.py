"""
A Slack application bot user that formats discussion
Author: Spencer Mycek
"""

import os, time, re, websocket
from Python.commands import *
try:
    import thread
except ImportError:
    import _thread as thread


bot_token = os.environ.get('SLACK_BOT_TOKEN')
user_token = os.environ.get('SLACK_USER_TOKEN')
print(str(bot_token) + '\n' + str(user_token))
discuss_bot_id = None
discussion_chat_id = None


"""
    Translates the message received from the server into a dictionary
"""
def message_to_dict(message):
    message_dict = {}
    if isinstance(message, str):
        tmp = re.sub("[{}\"]", '', message).split(',')
        for string in tmp:
            var = string.split(':')
            message_dict[var[0]] = var[1]
    return message_dict


"""
Gathers all relevant data and sends it to master_command
"""
def handle_response(message_dict):
    master_command(bot_token, user_token, discuss_bot_id, discussion_chat_id, message_dict)



"""
    Sends messages from the websocket to a command handler
"""
def on_message(ws, message):
    print(message)
    message_dict = message_to_dict(message)
    handle_response(message_dict)


"""
    Displays websocket errors when they occur
"""
def on_error(ws, error):
    print(error)


"""
    Closes the websocket upon ending the program or signal interrupt
"""
def on_close(ws):
    ws.close()
    print("### closed ###")

"""
    Upon beginning the websocket waits for the trace to begin
"""
def on_open(ws):
    time.sleep(1)
    print("### open ###")


def main():
    global  discuss_bot_id, discussion_chat_id
    r = requests.get('https://slack.com/api/rtm.connect', {'token':bot_token})
    discuss_bot_id = r.json()['self']['id']
    url = r.json()['url']
    r = requests.get('https://slack.com/api/conversations.list', {'token':bot_token})
    for channel in r.json()['channels']:
        if channel['name'] == 'discussion':
            discussion_chat_id = channel['id']
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url=url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()

