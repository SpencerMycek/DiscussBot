"""
A file to maintain speaking order and topic list
Author: Spencer Mycek
"""
import requests, json, re

# A dictionary that keeps track of "topic":List of 'new points'
# Each new point will have the original author at [0] and a thread_ts at [1]
# Example:
#   { 'topic':[
#               [
#                   'Author1' , thread_ts
#               ],
#               [
#                   'Author2' , thread_ts
#               ]
#           ]
#   {
#
discussion_list = {"Default Topic": []}
# A queue of topics to keep order as dicts have unpredicatable ordering
topic_queue = ["Default Topic"]
# A reference of the current topic to retrieve from discussion_list
current_topic = "Default Topic"


def add_topic(topic):
    """Create a new topic"""
    global discussion_list
    print(topic)
    discussion_list[str(topic).strip()] = []
    topic_queue.append(str(topic).strip())


def add_new_point(author, text, ts, token, channel):
    """Add a new point to the current topic"""
    global discussion_list
    # A user can have a display name or realname. Attempts to use display before real
    name = requests.get(
        'https://slack.com/api/users.info',
        params={
            'token': token,
            'user': author
        }).json()
    name = name['user']['profile']['display_name'] if not "" else name['user'][
        'profile']['real_name']
    # Removes any unicode in the form '\uXXXX'
    # Originally used to fix slack changing apostrophes (') to \u2019
    match = re.search("(\\\\.{5})", text)
    if match is not None:
        match = match.groups()
    else:
        match = [""]
    for string in match:
        if "\\u" in string:
            text = text.replace(string, "")
    # Payload for new point message, has required json fields and uses Slack message block format
    payload = {
        'token':
        token,
        'channel':
        channel,
        'text':
        "Discussion: New Point",
        'blocks': [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': 'New Point by {}\n\n'.format(name)
            }
        }, {
            'type': 'divider'
        },
                   {
                       'type': 'section',
                       'text': {
                           'type': 'mrkdwn',
                           'text': '{}\n\n'.format(text)
                       }
                   }, {
                       'type': 'divider'
                   },
                   {
                       'type': 'section',
                       'text': {
                           'type': 'mrkdwn',
                           'text': '\nCurrent Topic: {}'.format(current_topic)
                       }
                   }, {
                       'type': 'divider'
                   }, {
                       'type': 'divider'
                   }, {
                       'type': 'divider'
                   }]
    }
    # Required JSON headers for Slack
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer " + token
    }
    r = requests.post(
        'https://slack.com/api/chat.postMessage',
        data=json.dumps(payload),
        headers=headers)
    # We need to save the a reference of the message we just sent to slack for proper threading
    discussion_list[current_topic].append([author, r.json()['message']['ts']])


def add_direct_response(author, token, channel, target, text):
    """Add a direct response to the target new point based on the author"""
    global discussion_list
    # Try to find the TS of the target New point based on author
    # ts - Timestamp required for threading
    for point in discussion_list[current_topic]:
        if target == point[0]:
            ts = point[1]
    ts = ts if not None else 0
    # Removes any unicode in the form '\uXXXX'
    # Originally used to fix slack changing apostrophes (') to \u2019
    match = re.search("(\\\\.{5})", text)
    if match is not None:
        match = match.groups()
    else:
        match = [""]
    for string in match:
        if "\\u" in string:
            text = text.replace(string, "")
    # A user can have a display name or realname. Attempts to use display before real
    name = requests.get(
        'https://slack.com/api/users.info',
        params={
            'token': token,
            'user': author
        }).json()
    name = name['user']['profile']['display_name'] if not "" else name['user'][
        'profile']['real_name']
    # Payload for new point message, has required json fields and uses Slack message block format
    payload = {
        'token':
        token,
        'channel':
        channel,
        'text':
        "Discussion: Direct Response",
        'blocks': [{
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': 'Response from: {}'.format(name)
            }
        }, {
            'type': 'divider'
        },
                   {
                       'type': 'section',
                       'text': {
                           'type': 'mrkdwn',
                           'text': '{}'.format(text)
                       }
                   }, {
                       'type': 'divider'
                   }],
        'thread_ts':
        ts,
    }
    # Required JSON headers for Slack
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "charset": "utf-8"
    }
    r = requests.post(
        'https://slack.com/api/chat.postMessage',
        data=json.dumps(payload),
        headers=headers)


def get_topics():
    """
    Returns a list of topics in the discussion as a string
    :return: String of current topics formatted for a Slack message
    """
    global discussion_list
    result = ""
    result += "Current Topic: " + current_topic + '\n'
    i = 1
    for topic in discussion_list.keys():
        if topic is current_topic:
            continue
        result += "Topic {}: {}\n".format(str(i + 1), topic)
        i += 1

    return result


def get_discussion():
    """
    Returns the current discusion
    :return: A list of strings: Name of topic
    """
    global discussion_list
    return discussion_list[current_topic]


def next_topic(token, channel):
    """Changes the topic to the next in the discussion_list"""
    global discussion_list, current_topic
    # Remove the current topic from the queue (index 0)
    #   and sets the current topic to the new topic_queue[0]
    discussion_list.pop(topic_queue.pop(0))
    current_topic = topic_queue[0]
    # Payload for new point message, has required json fields and uses Slack message block format
    payload = {
        'token':
        token,
        'channel':
        channel,
        'text':
        "Discussion: New Topic",
        'blocks': [{
            'type': 'divider'
        }, {
            'type': 'divider'
        },
                   {
                       'type': 'section',
                       'text': {
                           'type': 'mrkdwn',
                           'text': 'New Topic: {}\n'.format(current_topic)
                       }
                   }, {
                       'type': 'divider'
                   }, {
                       'type': 'divider'
                   }],
    }
    # Required JSON headers for Slack
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token,
        "charset": "utf-8"
    }

    requests.post(
        'https://slack.com/api/chat.postMessage',
        data=json.dumps(payload),
        headers=headers)
