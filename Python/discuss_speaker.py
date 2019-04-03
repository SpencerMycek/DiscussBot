"""
A file to maintain speaking order and topic list
Author: Spencer Mycek
"""

# A dictionary that keeps track of "topic":List of 'new points'
# Each new point will have a list of direct response authors at [0] and original author at [1]
# Example:
#   'topic':[ [ ['P1','P2'] , 'P3' ], [ [ 'P3', 'P1' ] , 'P2' ] ]
#
discussion_list = {"": []}
# A reference of the current topic to retrieve from discussion_list
current_topic = ""


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

def get_discussion():
    """Returns the current discussion_list"""
    global discussion_list
    return discussion_list
