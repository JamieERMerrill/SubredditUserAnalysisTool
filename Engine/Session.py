# Copyright (c) 2018 by James Merrill, all rights reserved

import Engine.Credentials
import praw


class Session:
    def __init__(self):
        self.creds = Engine.Credentials.Credentials()
        self.session = praw.Reddit(client_id=self.creds.id, client_secret=self.creds.secret,
                                   user_agent=self.creds.user_agent)

    def get_user(self, username):
        return self.session.redditor(username)

    def get_subreddit(self, subreddit_name):
        return self.session.subreddit(subreddit_name)

    def get_comment(self, comment_id):
        return self.session.comment(id=comment_id)


STATIC_SESSION = Session()
