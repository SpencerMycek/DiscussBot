"""
A file to maintain speaking order and topic list
Author: Spencer Mycek
"""
import requests, json

# A dictionary that keeps track of "topic":List of 'new points'
# Each new point will have a list of direct response authors at [0] and original author at [1] and a thread_ts at [2]
# Example:
#   { 'topic':[
#               [
#                   ['P1','P2'] , 'P3' , thread_ts
#               ],
#               [
#                   [ 'P3', 'P1' ] , 'P2' , thread_ts
#               ]
#           ]
#   {
#
discussion_list = {"Default Topic": []}
# A reference of the current topic to retrieve from discussion_list
current_topic = "Default Topic"


def add_topic(topic):
    """Create a new topic"""
    global discussion_list
    discussion_list[str(topic).strip] = [
    ]  # Creates the first new point with the creator of the topic as the author


def add_new_point(author, text, ts, token, channel):
    """Add a new point to the current topic"""
    global discussion_list
    discussion_list[current_topic].append([[], author, ts])
    name = requests.get('https://slack.com/api/users.info', params={'token':token, 'user':author}).json()
    name = name['user']['profile']['display_name'] if not "" else name['user']['profile']['real_name']
    point = "New Point by: {}\n\n".format(name)
    payload={
        'token': token,
        'channel': channel,
        'blocks':[
            {
                'type': 'section',
                'text': {
                    'type':'plain_text',
                    'text': 'New Point by {}\n\n'.format(name)
                }
            },
            {
                'type':'divider'
            },
            {
                'type': 'section',
                'text': {
                    'type': 'plain_text',
                    'text': '{}\n\n'.format(text)
                }
            },
            {
                'type': 'divider'
            },
            {
                'type': 'section',
                'text': {
                    'type': 'plain_text',
                    'text': '\nCurrent Topic'.format(current_topic)
                }
            }
        ]
    }
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + token}
    r = requests.post('https://slack.com/api/chat.postMessage', data=json.dumps(payload), headers=headers)
    print(r.json())


def add_direct_response(author, target):
    """Add a direct response to the target new point based on the author"""
    global discussion_list
    for x in discussion_list[current_topic]:
        r = requests.get(
            'https://slack.com/api/users.info',
            params={
                'token': target,
                'user': x[1]
            })
        name=r.json()['user']['profile']['display_name']
        if name:
            print(name)
        else:
            print(r.json()['user']['profile']['real_name'])



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
