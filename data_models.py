from dataclasses import dataclass
import pickle
import itertools as it
import operator as op
from phash import phash

def make_db(path):     # TODO: handle already-created database
    class Db(dict):
        def __setitem__(self, key, value):
            dict.__setitem__(self, key, value)
            self.sync()
        def sync(self):
            with open(path, 'wb') as f:
                pickle.dump(dict(self), f)        # FIXME: check
        def clear(self):
            with open(path, 'wb') as f:
                f.write(b'', f)                 # FIXME: check
    try:
        with open(path, 'rb') as f:
            return Db(pickle.load(f))
    except Exception as e:
        print(e)
    return Db()

@dataclass
class User:
    handle: str
    email: str
    phone_number: str
    password_hash: int
    interests: list
    bio: str = ""
    posts: list = None
    stats: dict = None

    @staticmethod
    def check_handle(potential_handle):
        return potential_handle in userdb.keys()

    @staticmethod
    def auth(handle, password):
        return userdb[handle].password_hash == phash(password)

    def sync(self):
        userdb[self.handle] = self

@dataclass
class Post:
    author: User
    content: str
    date: str
    tags: list
    stats: dict = None

    def _add_to_author(self):
        author.posts.append(id(self))
        userdb.sync()

    def sync(self):
        postdb[id(self)] = self

    @staticmethod
    def all_posts():
        return postdb.values()

@dataclass
class Organization:
    name: str
    admin: User
    description: str
    topics: list = None
    events: dict = None

    def confirm_admin(self):
        pass   # TODO

    def sync(self):
        orgdb[name] = self

    @staticmethod
    def all_orgs(self):
        return orgdb.values()

@dataclass
class Event:
    name: str
    organization: Organization
    admins: list
    participants: list
    tags: list = None

    def sync(self):
        organization.events[id(self)] = self

    @staticmethod
    def all_events(self):
        return it.chain.from_iterable(map(lambda x: x.events.values(), orgdb))

    @staticmethod
    def all_events(self):
        return it.chain.from_iterable(map(op.itemgetter('events'), Organization.all_orgs()))

    @staticmethod
    def from_id(self, eventid):
        return [x for x in Event.all_events() if phash(x.name) == eventid][0]

userdb = make_db("./user.bin")
postdb = make_db("./posts.bin")
orgdb = make_db("./orgs.bin")

