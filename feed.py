from random import shuffle
from data_models import *
import itertools as it

def intersection(l1, l2):
    return bool([x for x in l1 if x in l2])

def generate_feed(user):   # TODO: order properly
    # TODO: make more efficient?
    # u = User("dev", "dev@gb.org", "1717171717", hash("asdffdsa"), ["climate"], "I am developer")
    # return [Post(u, "sample", "Jan 10 2022", ["climate"]), u]
    l = (list(it.chain(Post.all_posts(), User.all_users(), Event.all_events())))
    shuffle(l)
    return l
    return shuffle(
            [x for x in Post.all_posts() if intersection(x.tags, user.interests)] +
            [x for x in User.all_users() if intersection(x.interests, user.interests)] +
            [x for x in Organizations.all_orgs() if intersection(x.topics, user.interests)] +
            [x for x in Event.all_events() if intersection(x.organization.topics, user.interests)]
    )
