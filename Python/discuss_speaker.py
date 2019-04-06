"""
A file to maintain speaking order and topic list
Author: Spencer Mycek
"""

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
    discussion_list[str(topic).strip] = []  # Creates the first new point with the creator of the topic as the author


def add_new_point(author, ts):
    """Add a new point to the current topic"""
    global discussion_list
    discussion_list[current_topic].append([[], author, ts])


def add_direct_response(author, target):
    """Add a direct response to the target new point based on the author"""
    global discussion_list
    for x in discussion_list[current_topic]:
        print(x[1])

def get_topics():
    """Returns a list of topics in the discussion as a string"""
    global discussion_list
    result = ""
    result += "Current Topic: " + current_topic + '\n'
    i = 1
    for topic in discussion_list.keys():
        if topic is current_topic:
            continue
        result += "Topic {}: {}\n".format(str(i+1), topic)
        i+=1

    return result

def get_discussion():
    """Returns the current discusion"""
    global discussion_list
    return discussion_list[current_topic]

