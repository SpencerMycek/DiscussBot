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
    name = requests.get('https://slack.com/api/users.info', params={'token':token, 'user':author}).json()
    name = name['user']['profile']['display_name'] if not "" else name['user']['profile']['real_name']
    match = re.search("(\\\\.{5})", text)
    if match is not None:
        match = match.groups()
    else:
        match = [""]
    for string in match:
        if "\\u" in string:
            text = text.replace(string, "")
    payload={
        'token': token,
        'channel': channel,
        'text': "Discussion: New Point",
        'blocks':[
            {
                'type': 'section',
                'text': {
                    'type':'mrkdwn',
                    'text': 'New Point by {}\n\n'.format(name)
                }
            },
            {
                'type':'divider'
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '{}\n\n'.format(text)
                }
            },
            {
                'type': 'divider'
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '\nCurrent Topic: {}'.format(current_topic)
                }
            },
            {
                'type': 'divider'
            },
            {
                'type': 'divider'
            },
            {
                'type': 'divider'
            }
        ]
    }
    headers = {"Content-Type": "application/json; charset=utf-8",
               "Authorization": "Bearer " + token}
    r = requests.post('https://slack.com/api/chat.postMessage', data=json.dumps(payload), headers=headers)
    discussion_list[current_topic].append([[], author, r.json()['message']['ts']])


def add_direct_response(author, token, channel, target, text):
    """Add a direct response to the target new point based on the author"""
    global discussion_list
    for point in discussion_list[current_topic]:
        if target == point[1]:
            ts = point[2]
    ts = ts if not None else 0
    match = re.search("(\\\\.{5})", text)
    if match is not None:
        match = match.groups()
    else:
        match = [""]
    for string in match:
        if "\\u" in string:
            text = text.replace(string, "")
    name = requests.get('https://slack.com/api/users.info', params={'token': token, 'user': author}).json()
    name = name['user']['profile']['display_name'] if not "" else name['user']['profile']['real_name']
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + token,
               "charset":"utf-8"}
    payload={
        'token': token,
        'channel': channel,
        'text': "Discussion: Direct Response",
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'Response from: {}'.format(name)
                }
            },
            {
                'type': 'divider'
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '{}'.format(text)
                }
            },
            {
                'type': 'divider'
            }
        ],
        'thread_ts': ts,
    }
    r = requests.post('https://slack.com/api/chat.postMessage', data=json.dumps(payload), headers=headers)


def get_topics():
    """Returns a list of topics in the discussion as a string"""
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
    """Returns the current discusion"""
    global discussion_list
    return discussion_list[current_topic]


def next_topic(token, channel):
    """Changes the topic to the next in the discussion_list"""
    global discussion_list, current_topic
    print(topic_queue)
    print(discussion_list.keys())
    discussion_list.pop(topic_queue.pop(0))
    current_topic = topic_queue[0]
    print(discussion_list.keys())
    print(topic_queue)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + token,
               "charset": "utf-8"}
    payload={
        'token': token,
        'channel': channel,
        'text': "Discussion: New Topic",
        'blocks': [
            {
                'type': 'divider'
            },
            {
                'type': 'divider'
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'New Topic: {}\n'.format(current_topic)
                }
            },
            {
                'type': 'divider'
            },
            {
                'type': 'divider'
            }
        ],
    }
    requests.post('https://slack.com/api/chat.postMessage', data=json.dumps(payload), headers=headers)

