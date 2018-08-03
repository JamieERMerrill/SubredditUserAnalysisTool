# Copyright (c) 2018 by James Merrill, all rights reserved

import json
import argparse
import Engine.Session
import datetime
import Engine.Comment
from Engine import ConfigureLogging
from Engine import Sanitizer
import logging


class UserHistoryData:
    def __init__(self, user, days_of_history):
        self.now = datetime.datetime.now()
        self.past_hard_stop = self.now - datetime.timedelta(days=days_of_history)
        self.user = user
        self.comments = []
        self.subreddits = dict()

        self.load_comments()

    def inc_subreddit_count(self, subreddit_name):
        if subreddit_name not in self.subreddits:
            self.subreddits[subreddit_name] = 0

        self.subreddits[subreddit_name] += 1

    def load_comments(self):
        comment_block_one = self.user.comments.new(limit=None)
        for comment in comment_block_one:
            created = datetime.datetime.fromtimestamp(comment.created)
            if created < self.past_hard_stop:
                break

            self.comments.append(Engine.Comment.Comment.from_praw_comment(comment, False))
            self.inc_subreddit_count(comment.subreddit.display_name)

    def get_json(self):
        return_dict = dict()
        return_dict['comments'] = [comment.to_dict() for comment in self.comments]
        return_dict['subreddit_breakdown'] = self.subreddits
        return_dict['username'] = self.user.name
        return json.dumps(return_dict, indent=4, sort_keys=True)


class UserHistoryScraper:
    def __init__(self, username, length_of_history_in_days):
        logging.info("Getting {} days of posts from {}".format(length_of_history_in_days, username))
        self.user = Engine.Session.STATIC_SESSION.get_user(username)
        self.un = username
        self.uhd = UserHistoryData(self.user, length_of_history_in_days)

    def dump(self, output_folder):
        file_name = Sanitizer.sanitize_filename('{}.json'.format(self.un))
        dump_path = Sanitizer.trim_file_path("{}/{}".format(output_folder, file_name))
        logging.info("Writing {}".format(dump_path))
        with open(dump_path, 'w') as fp:
            fp.write(self.uhd.get_json())


if __name__ == "__main__":
    ConfigureLogging.configure_logging()

    logging.info("Running UserHistoryScraper.py")

    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True, help="Username to get data for")
    durations = parser.add_mutually_exclusive_group(required=True)
    durations.add_argument("--days", type=int, help="The length of history in days to get")
    durations.add_argument("--months", type=int, help="The length of history in months to get")
    parser.add_argument("--write_directory", required=True, help="The directory to write the user stats for")

    args = parser.parse_args()
    days = 0
    if args.days:
        days = args.days
    elif args.months:
        days = args.months * 30

    uhs = UserHistoryScraper(args.user, days)
    uhs.dump(args.write_directory)
