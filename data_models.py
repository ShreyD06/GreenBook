from dataclasses import dataclass
import pickle
import itertools as it
import operator as op
from phash import phash
from ars import calculate_volunteer, calculate_organization

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
    reputation: int = 1
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

    def delta_rep(self, organization, hours):
        self.reputation += User.calculate_delta_rep(organization, hours)

    @staticmethod
    def all_users():
        return userdb.values()

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
    reputation: int = 1

    def confirm_admin(self):
        pass   # TODO

    def sync(self):
        orgdb[self.name] = self

    @staticmethod
    def all_orgs():
        return orgdb.values()

    @staticmethod
    def get_from_admin(user):
        try:
            return [x for x in Organization.all_orgs() if x.admin == user][0]
        except IndexError:
            return None

    @staticmethod
    def calculate_delta_rep(user):
        return calculate_organization(user.reputation)

    def delta_rep(self, user):
        self.reputation += Organization.calculate_delta_rep(user)

@dataclass
class Event:
    name: str
    organization: Organization
    admins: list
    participants: list
    tags: list = None

    def sync(self):
        if self.organization.events is None:
            self.organization.events = []
        self.organization.events.append(self)
        orgdb.sync()     # Some issues here, I think?

    @staticmethod
    def all_events():
        return it.chain.from_iterable(map(lambda x: x.events, orgdb.values()))

    @staticmethod
    def from_id(eventid):
        return [x for x in Event.all_events() if phash(x.name) == eventid][0]

userdb = make_db("./user.bin")
postdb = make_db("./posts.bin")
orgdb = make_db("./orgs.bin")

