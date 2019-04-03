"""
A file to contain all commands and handle command delegations
Author: Spencer Mycek
"""
import requests, re
from discuss_speaker import *

MENTION_REGEX = "^<@(|[WU][^>]+)>(.*)"
"""
Handles all messages in the "discussion" channel
and formats the discussion with the user_token
"""


def format_discussion(bot_token, user_token, message):
    commands = {
        1: '.',  # New Point
        2: '-&gt;',  # ->, Direct Response
        3: 'thumbs-up',  # Thumbs up
        4: 'help',  # Display Help Message
        5: 'topic',  # Topic management
    }
    help_message = 'HELP: DiscussBot Commands. Post in Chat:\n' + \
            '*{}* - Prints this help message\n'.format(commands[4]) + \
            '*{}* - Signal you have a new point to add to discussion\n'.format(commands[1]) + \
            '*{}* - Signal you have a direct response to the last new point\n'.format(commands[2]) + \
            '*{}* - Thumbs Up the most recent new point or direct response\n'.format(commands[3]) + \
            '*{}* - Prints the current topic\n'.format(commands[5])
    if commands[1] in message['text'].lower():
        print(message['text'])
    elif commands[2] in message['text'].lower():
        print(message['text'])
    elif commands[3] in message['text'].lower():
        print(message['text'])
    elif commands[5] in message['text'].lower():
        print(message['text'])
    elif commands[4] in message['text'].lower():
        r = requests.post(
            'https://slack.com/api/chat.postEphemeral',
            data={
                'token': bot_token,
                'channel': message['channel'],
                'user': message['user'],
                'text': help_message
            })
    else:
        r = requests.post(
            'https://slack.com/api/chat.postEphemeral',
            data={
                'token': bot_token,
                'channel': message['channel'],
                'user': message['user'],
                'text': help_message
            })

    # Gets rid of command post in Discussion channel
    requests.post(
        'https://slack.com/api/chat.delete',
        data={
            'token': user_token,
            'channel': message['channel'],
            'ts': message['ts'],
            'as_user': 'true'
        })


"""
Handles all messages in all channels not "discussion"
Commands coming into this method must start with @DiscussBot
"""


def commands_elsewhere(bot_token, message):
    if 'help' in message['text'].lower():
        help_message = "Out of channel DiscussBot commands\n" \
                       "Help - Print this help message\n" \
                       "Current - Print the current discussion topic\n" \
                       "Topics - Print the list of upcoming topics\n"
        requests.post(
            'https://slack.com/api/chat.postEphemeral',
            data={
                'token': bot_token,
                'channel': message['channel'],
                'user': message['user'],
                'text': help_message
            })
    elif 'current' in message['text'].lower():
        requests.post(
            'https://slack.com/api/chat.postMessage',
            data={
                'token': bot_token,
                'channel': message['channel'],
                'text': "Current Topic: "
            })
    elif 'topics' in message['text'].lower():
        requests.post(
            'https://slack.com/api/chat.postMessage',
            data={
                'token': bot_token,
                'channel': message['channel'],
                'text': discuss_speaker.get_discussion()
            })
    else:
        requests.post(
            'https://slack.com/api/chat.postEphemeral',
            data={
                'token': bot_token,
                'channel': message['channel'],
                'user': message['user'],
                'text': "I don't know that, try: *{}*".format("Help")
            })


"""
Master method that redirects different message inputs to different commands
Commands coming into this channel
"""


def master_command(bot_token, user_token, bot_id, channel_id, message):
    if message['type'] == 'message' and not 'subtype' in message:
        if message['channel'] == channel_id:
            format_discussion(bot_token, user_token, message)
        else:
            matches = re.match(MENTION_REGEX, message['text'])
            if matches.group(1) == bot_id:
                commands_elsewhere(bot_token, message)
