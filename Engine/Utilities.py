# Copyright (c) 2018 by James Merrill, all rights reserved

from praw.models.reddit import more as more


def flatten_more_comments(more_comments):
    comments = list()

    for comment in more_comments.comments(True):
        if isinstance(comment, more.MoreComments):
            for sub_comment in flatten_more_comments(comment):
                if isinstance(sub_comment, more.MoreComments):
                    comments.extend(flatten_more_comments(sub_comment))
                else:
                    comments.extend(flatten_comment_chain(sub_comment))
        else:
            comments.extend(flatten_comment_chain(comment))

    return comments


def flatten_comment_chain(root_comment):
    comments = list()
    comments.append(root_comment)

    for reply in root_comment.replies:
        if isinstance(reply, more.MoreComments):
            comments.extend(flatten_more_comments(reply))
        else:
            comments.extend(flatten_comment_chain(reply))

    return comments