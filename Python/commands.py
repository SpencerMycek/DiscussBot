"""
A file to contain all commands and handle command delegations
Author: Spencer Mycek
"""
import requests, re


MENTION_REGEX="^<@(|[WU][^>]+)>(.*)"

"""
Handles all messages in the "discussion" channel
and formats the discussion with the user_token
"""
def format_discussion(bot_token, user_token, message):
    commands={
        1: '.',
        2: '->',
        3: 'thumbs up',
        4: 'help',
        5: 'topic',
        6: 'topics',
        7: 'new-topic',
    }


"""
Handles all messages in all channels not "discussion"
Commands coming into this channel start with @DiscussBot
"""
def commands_elsewhere(bot_token, message):
    if 'help' in message['text'].lower():
        help_message = "Out of channel DiscussBot commands\n" \
                       "Help - Print this help message\n" \
                       "Current - Print the current discussion topic\n" \
                       "Topics - Print the list of upcoming topics\n"
        requests.post('https://slack.com/api/chat.postEphemeral', data={
            'token':bot_token,
            'channel':message['channel'],
            'user':message['user'],
            'text':help_message
        })
    elif 'current' in message['text'].lower():
        requests.post('https://slack.com/api/chat.postMessage', data={
            'token': bot_token,
            'channel': message['channel'],
            'text': "Current Topic: "
        })
    elif 'topics' in message['text'].lower():
        requests.post('https://slack.com/api/chat.postMessage', data={
            'token': bot_token,
            'channel': message['channel'],
            'text': "Upcoming Topics: "
        })
    else:
        requests.post('https://slack.com/api/chat.postEphemeral', data={
            'token':bot_token,
            'channel':message['channel'],
            'user':message['user'],
            'text':"I don't know that, try: *{}*".format("Help")
        })


"""
Master method that redirects different message inputs to different commands
Commands coming into this channel
"""
def master_command(bot_token, user_token , bot_id, channel_id, message):
    if message['type'] == 'message':
        if message['channel'] == channel_id:
            format_discussion(bot_token, user_token,  message)
        else:
            matches = re.match(MENTION_REGEX, message['text'])
            if matches.group(1) == bot_id:
                commands_elsewhere(bot_token, message)
