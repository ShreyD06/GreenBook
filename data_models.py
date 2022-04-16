from dataclasses import dataclass
import pickle

def make_db(path):
    class Db(dict):
        def __init__(self):
            self.path = path
        def __setitem__(self, key, value):
            dict.__setitem__(self, key, value)
            self.sync()
        def sync(self):
            with open(path, 'w') as f:
                pickle.dump(self, f)        # FIXME: check
    return Db()

userdb = make_db("./user.bin")
postdb = make_db("./posts.bin")
orgdb = make_db("./orgs.bin")

@dataclass
class User:
    handle: str
    email: str
    phone_number: str
    password_hash: int
    interests: list
    bio: str = ""
    posts: list = []
    stats: dict = {}

    @staticmethod
    def check_handle(potential_handle):
        return potential_handle in userdb.keys()

    def sync(self):
        userdb[self.handle] = self

@dataclass
class Post:
    author: User
    content: str
    date: str
    tags: list
    stats: dict = {}

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
    topics: list = []
    events: dict = {}

    def confirm_admin(self):
        pass   # TODO

    def sync(self):
        orgdb[name] = self

@dataclass
class Event:
    name: str
    organization: Organization
    admins: list
    participants: list
    tags: list = []

    def sync(self):
        organization.events[id(self)] = self
