# Copyright (c) 2018 by James Merrill, all rights reserved

from praw.models.reddit import more, comment

class Comment:
    def __init__(self, permalink, datetime, subreddit, content, children=None):
        self.permalink = permalink
        self.datetime = datetime
        self.subreddit = subreddit
        self.content = content
        self.children = children or list()

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        return_dict = dict()
        return_dict['permalink'] = self.permalink
        return_dict['datetime'] = self.datetime
        return_dict['subreddit'] = self.subreddit
        return_dict['content'] = self.content
        return_dict['children'] = [child.to_dict() for child in self.children]
        return return_dict

    @classmethod
    def from_dict(cls, the_dict):
        obj = cls(the_dict['permalink'], the_dict['datetime'], the_dict['subreddit'], the_dict['content'])
        if 'children' in the_dict:
            for child_dict in the_dict['children']:
                obj.add_child(cls.from_dict(child_dict))
        return obj

    @classmethod
    def from_praw_comment(cls, praw_comment, with_children=True):
        obj = cls(praw_comment.permalink, praw_comment.created, praw_comment.subreddit.display_name, praw_comment.body)
        if with_children:
            for reply in praw_comment.replies:
                if isinstance(reply, comment.Comment):
                    obj.add_child(cls.from_praw_comment(reply, True))
                elif isinstance(reply, more.MoreComments):
                    for child in reply.children:
                        obj.add_child(child, True)
        return obj
