from random import shuffle

def intersection(l1, l2):
    return bool([x for x in l1 if x in l2])

def generate_feed(user):   # TODO: order properly
    # TODO: make more efficient?
    return shuffle(
            [x for x in Post.all_posts() if intersection(x.tags, user.interests)] +
            [x for x in User.all_users() if intersection(x.interests, user.interests)] +
            [x for x in Organizations.all_orgs() if intersection(x.topics, user.interests)]
    )
