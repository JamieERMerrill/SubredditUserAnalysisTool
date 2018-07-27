from Engine.Comment import Comment
from praw.models.reddit.more import MoreComments
import json
import os
import logging


class Post:
    def __init__(self, title, permalink, timestamp, commenters, flattened_comments, comments_as_tree):
        self.title = title
        self.permalink = permalink
        self.timestamp = timestamp
        self.commenters = commenters

        self.flattened_comments = flattened_comments
        self.comments_as_tree = comments_as_tree
        self.comment_count = len(flattened_comments)

    def to_dict(self):
        return_dict = dict()
        return_dict['title'] = self.title
        return_dict['permalink'] = self.permalink
        return_dict['timestamp'] = self.timestamp
        return_dict['commenters'] = list(self.commenters)
        return_dict['comment_count'] = self.comment_count
        return_dict['comment_tree'] = [root_comment.to_dict() for root_comment in self.comments_as_tree]
        return return_dict

    def dump(self, target_dir):
        filename = "{}.json".format(self.title.replace(' ', '_').replace(',', '').replace(':', ''))
        target_file = os.path.join(target_dir, filename)

        logging.info("Writing {}".format(target_file))
        with open(target_file, 'w') as fp:
            text = json.dumps(self.to_dict(), indent=4, sort_keys=True)
            fp.write(text)

    @classmethod
    def from_dict(cls, post_dict):
        comments = [Comment.from_dict(comment) for comment in post_dict['comment_tree']]
        flattened = list()

        for comment in comments:
            flattened.extend(comment.get_flattened_child_list())

        return cls(post_dict['title'], post_dict['permalink'], post_dict['timestamp'],
                   post_dict['commenters'], flattened, comments)

    @classmethod
    def from_praw_post(cls, praw_post):
        comments = list()

        for praw_comment in praw_post.comments:
            if isinstance(praw_comment, MoreComments):
                for child in praw_comment.children:
                    comments.append(Comment.from_praw_comment(child, True))

            comments.append(Comment.from_praw_comment(praw_comment, True))

        flattened = list()
        authors = set()
        for comment in comments:
            flattened.extend(comment.get_flattened_child_list())
            authors = authors.union(comment.get_unique_commenters_at_node_and_lower())

        return cls(praw_post.title, praw_post.permalink, praw_post.created, authors, flattened, comments)
