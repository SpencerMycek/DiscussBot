"""
A Slack application bot user that formats discussion
Author: Spencer Mycek
"""

import os
import time
import re
from slackclient import SlackClient

# instantiate Slack client
# You must import the Slack Bot User OAuth Access Token
bot_token = os.environ.get('SLACK_BOT_TOKEN')
print(bot_token)
slack_client = SlackClient(bot_token)
# Discussbot's user ID in Slack: Value is assigned after the bot starts up
discussbot_id = None

# Constants
RTM_READ_DELAY = 1 # 1 Second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentiond. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this cuntion returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == discussbot_id:
                return message, event["channel"], event["user"] if event["user"] else None
    return None, None, None


def handle_command(command, channel, user):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes given command, filling in response
    response = None
    # This is where to implement commands
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure, will do!"

    # Sends response back to the channel
    if user is not None:
        slack_client.api_call(
            "chat.postEphemeral",
            channel=channel,
            text=response or default_response,
            user=user
        )
    else:
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
            )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user UD by calling Web API method auth.test
        discussbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel, user = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel, user)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

