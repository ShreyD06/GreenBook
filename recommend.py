# TODO: use AI
from feed import intersection

def recommendations(user):
    return [e for e in Event.all_events() if intersection(e.tags, user.interests)]
