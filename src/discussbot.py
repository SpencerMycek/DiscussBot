#!/bin/python
"""
A Slack application bot user that formats discussion
Author: Spencer Mycek
"""
import os, websocket, requests, re
import time, datetime
import Command.commands as c

# Get Slack OAuth tokens from environment
bot_token = os.environ.get('SLACK_BOT_TOKEN')
user_token = os.environ.get('SLACK_USER_TOKEN')
#print(str(bot_token) + '\n' + str(user_token))
# Required globals of useful constants
discuss_bot_id = None
discussion_chat_id = None


def message_to_dict(message):
    """
    Translates the message received from the server into a dictionary
    :return: A dictionary, similar to json format
    """
    message_dict = {}
    if isinstance(message, str):
        tmp = re.sub("[{}\"]", '', message).split(',')
        for string in tmp:
            var = string.split(':')
            message_dict[var[0]] = var[1]
    return message_dict


def handle_response(message_dict):
    """Gathers all relevant data and sends it to master_command"""
    c.master_command(bot_token, user_token, discuss_bot_id, discussion_chat_id,
                     message_dict)


def on_message(ws, message):
    """Sends messages from the websocket to a command handler"""
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    message_dict = message_to_dict(message)
    print('[' + st + '] Event in channel: ' + message_dict['channel'] +
          '. Created by user: ' + message_dict['user'] + '. Event Type: ' +
          str(message_dict['type']) + '.')
    handle_response(message_dict)


def on_error(ws, error):
    """Displays websocket errors when they occur"""
    print(error)


def on_close(ws):
    """Closes the websocket upon ending the program or signal interrupt"""
    ws.close()
    print("### closed ###")


def on_open(ws):
    """Upon beginning the websocket waits for the trace to begin"""
    time.sleep(1)
    print("### open ###")


def main():
    """
        Begins connection to Slack RTM API and opens a websocket to listen to
        chat events
        Runs until Interrupted
    """
    global discuss_bot_id, discussion_chat_id
    r = requests.get('https://slack.com/api/rtm.connect', {'token': bot_token})
    discuss_bot_id = r.json()['self']['id']
    url = r.json()['url']
    r = requests.get('https://slack.com/api/conversations.list',
                     {'token': bot_token})
    for channel in r.json()['channels']:
        if channel['name'] == 'discussion':
            discussion_chat_id = channel['id']
    print(discussion_chat_id)
    ws = websocket.WebSocketApp(
        url=url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()
