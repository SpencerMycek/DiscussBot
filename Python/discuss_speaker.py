"""
A file to maintain speaking order and topic list
Author: Spencer Mycek
"""

# A dictionary that keeps track of "topic":List of 'new points'
# Each new point will have a list of direct response authors at [0] and original author at [1]
# Example:
#   'topic':[ [ ['P1','P2'] , 'P3' ], [ [ 'P3', 'P1' ] , 'P2' ] ]
#
discussion_list = {"Default Topic": [], "Topic2":[]}
# A reference of the current topic to retrieve from discussion_list
current_topic = "Default Topic"


def add_topic(topic, author):
    """Create a new topic"""
    global discussion_list
    discussion_list[topic] = [
        [[], author]
    ]  # Creates the first new point with the creator of the topic as the author


def add_new_point(author):
    """Add a new point to the current topic"""
    global discussion_list
    discussion_list[current_topic].append([[[], author]])


def add_direct_response(author):
    """Add a direct response to the current new point in the current topic"""
    global discussion_list
    discussion_list[current_topic][0][0].append(
        author)  # Adds the author to the list of direct responses

def get_topics():
    """Returns a list of topics in the discussion as a string"""
    result = ""
    result += "Current Topic: " + current_topic + '\n'
    i = 1
    for topic in discussion_list.keys():
        if topic is current_topic:
            continue
        result += "Topic {}: {}\n".format(str(i+1), topic)
        i+=1

    return result

