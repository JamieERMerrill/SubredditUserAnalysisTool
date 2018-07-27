class Comment:
    def __init__(self, permalink, datetime, subreddit, content):
        self.permalink = permalink
        self.datetime = datetime
        self.subreddit = subreddit
        self.content = content

    def to_dict(self):
        return_dict = dict()
        return_dict['permalink'] = self.permalink
        return_dict['datetime'] = self.datetime
        return_dict['subreddit'] = self.subreddit
        return_dict['content'] = self.content
        return return_dict