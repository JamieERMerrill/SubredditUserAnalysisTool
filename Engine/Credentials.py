import json
import os
import argparse

HERE = os.path.dirname(__file__)
CREDS_FILE = os.path.abspath(os.path.join(HERE, "..", "credentials.json"))


class Credentials:
    def __init__(self, client_id=None, client_secret=None, client_username=None, client_password=None):
        raw = dict()
        if not client_id or not client_secret or not client_username or not client_password:
            with open(CREDS_FILE, 'r') as fp:
                raw = json.load(fp)

        self.id = client_id or raw["client_id"]
        self.secret = client_secret or raw["client_secret"]
        self.username = client_username or raw["client_username"]
        self.password = client_password or raw["client_password"]

    def dump_to_file(self):
        out_dict = dict()
        out_dict["client_id"] = self.id
        out_dict["client_secret"] = self.secret
        out_dict["client_username"] = self.username
        out_dict["client_password"] = self.password

        with open(CREDS_FILE, 'w') as fp:
            json.dump(fp, out_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", default=None, help="The Client ID to write to the credentials file.")
    parser.add_argument("--secret", default=None, help="The client secret to write to the credentials file.")
    parser.add_argument("--username", default=None, help="The username to write to the credentials file.")
    parser.add_argument("--password", default=None, help="The password to write to the credentials file.")
    args = parser.parse_args()

    creds = Credentials(args.id, args.secret, args.username, args.password)
    creds.dump_to_file()
