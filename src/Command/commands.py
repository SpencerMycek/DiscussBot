"""
A file to contain all commands and handle command delegations
Author: Spencer Mycek
"""
import requests, re
import Discussion.discuss_speaker as d

MENTION_REGEX = "^<@(|[WU][^>]+)>(.*)"

admin = ""
moderators = []


def admin_commands(bot_token, user_token, message):
    """Runs admin commands"""
    global moderators
    if "next_topic" == message['text']:
        d.next_topic(bot_token, message['channel'])
    elif "add_mod" in message['text']:
        moderators.append(message['user'])


def format_discussion(bot_token, user_token, message):
    """
    Handles all messages in the "discussion" channel
    and formats the discussion with the user_token
    """
    # Gets rid of command post in Discussion channel
    global admin, moderators
    requests.post(
        'https://slack.com/api/chat.delete',
        data={
            'token': user_token,
            'channel': message['channel'],
            'ts': message['ts'],
            'as_user': 'true'
        })

    # Dict of public commands for discussion channel
    # thumps-up is unused but remains in case it needs to be implemented
    commands = {
        1: '.',  # New Point. Follow with the what you want to say
        2:
        '-&gt;',  # ->, Direct Response. Follow with who you are responding too and what you want to say
        3: 'thumbs-up',  # Thumbs up
        4: 'help',  # Display Help Message
        5: 'topic',  # Topic management
    }
    # Help string to tell end user public commands
    help_message = 'HELP: DiscussBot Commands. Post in Chat:\n' + \
            '*{}* - Prints this help message\n'.format(commands[4]) + \
            '*{}* - Signal you have a new point to add to discussion. Follow with what you want to say\n'.format(commands[1]) + \
            '*{}* - Signal you have a direct response to the last new point. ' \
                'Follow with who you are replying too: @user, and what your want to say\n'.format(commands[2]) + \
            '*{}* - Prints the current topic list, or takes a New Topic and puts it into the topic list\n'.format(commands[5])

    # Takes message and checks it for required command
    # If user is admin or mod it allows them to run admin commands
    if admin == "" and "set_admin" == message['text']:
        admin = message['user']
    elif (admin == message['user'] or
          message['user'] in moderators) and "next_topic" == message['text']:
        admin_commands(bot_token, user_token, message)
    elif commands[1] in message['text'].lower():
        text = re.match('^(. )(.*)', message['text'])
        d.add_new_point(message['user'], text.group(2), message['ts'],
                        bot_token, message['channel'])
    elif commands[2] in message['text'].lower():
        text = re.match('^(-&gt;) <@([U][^>]+)> (.*)', message['text'])
        d.add_direct_response(message['user'], bot_token, message['channel'],
                              text.group(2), text.group(3))
    elif commands[3] in message['text'].lower():
        print(message['text'])  # Not an accepted command
    elif message['text'] != 'next_topic' and commands[5] in message[
            'text'].lower() and message['text']:
        if commands[5] == message['text'].lower():
            r = requests.post(
                'https://slack.com/api/chat.postEphemeral',
                data={
                    'token': bot_token,
                    'channel': message['channel'],
                    'user': message['user'],
                    'text': d.get_topics()
                })
        else:
            matches = re.match("^([Tt]opic )(.*)", message['text'])
            d.add_topic(matches.group(2))
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
                'text': "I don't know that, try *help*"
            })


def commands_elsewhere(bot_token, message):
    """
    Handles all messages in all channels not "discussion"
    Commands coming into this method must start with @DiscussBot
    """
    if 'help' in message['text'].lower():
        help_message = "Out of channel DiscussBot commands\n" \
                       "Help - Print this help message\n" \
                       "Topics - Print the list of upcoming topics\n"
        requests.post(
            'https://slack.com/api/chat.postEphemeral',
            data={
                'token': bot_token,
                'channel': message['channel'],
                'user': message['user'],
                'text': help_message
            })
    elif 'topics' in message['text'].lower():
        requests.post(
            'https://slack.com/api/chat.postEphemeral',
            data={
                'token': bot_token,
                'channel': message['channel'],
                'text': d.get_topics()
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


def master_command(bot_token, user_token, bot_id, channel_id, message):
    """
    Master method that redirects different message inputs to different commands
    Commands coming into this channel
    """
    # Checks to make sure event from slack is a message, does not have a subtype, and the user is not the Bot user
    if message['type'] == 'message' and not 'subtype' in message and message[
            'user'] != bot_id:
        if message['channel'] == channel_id:
            format_discussion(bot_token, user_token, message)
        else:
            matches = re.match(MENTION_REGEX, message['text'])
            if matches.group(1) == bot_id:
                commands_elsewhere(bot_token, message)
