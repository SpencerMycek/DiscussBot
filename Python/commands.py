"""
A file to contain all commands and handle command delegations
Author: Spencer Mycek
"""
import requests


"""
Master method that redirects different message inputs to different commands
"""
def master_command(bot_token, user_token , bot_id, channel_id, message):
    if message['channel'] == channel_id:
        pass
    else:
        pass

