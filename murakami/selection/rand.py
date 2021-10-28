import random

class RandomSelection:
    def __init__(self):
        pass

    def get_servers(self, server_group):
        return set([random.choice(server_group)])