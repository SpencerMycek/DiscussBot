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
    pass


"""
Handles all messages in all channels not "discussion"
"""
def commands_elsewhere(bot_token, user_token, message):
    pass


"""
Master method that redirects different message inputs to different commands
"""
def master_command(bot_token, user_token , bot_id, channel_id, message):
    if message['channel'] == channel_id:
        format_discussion(bot_token, user_token,  message)
    else:
        matches = re.match(MENTION_REGEX, message['text'])
        if matches.group(1) == bot_id:
            commands_elsewhere(bot_token, user_token, message)
