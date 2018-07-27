# Subreddit User Analysis Tool  

This was made for a family member to assist in academic research and is not intended for any other 
use public or private. I'm developing it in a public repository in order to make it easy for the 
intended user to grab it. As an unlicensed piece of code, I reserve all rights regarding it, largely
because I'm not of the opinion that it is robust enough for more general use and I don't want to
imply a commitment to make it so.

## How To Use

**Initial Setup**:

1. Ensure you have Python 3.7 installed
2. If you don't already have virtualenv installed, open your console and type: `pip install virtualenv`
3. Go to the directory this readme is in on the console and type: `virtualenv venv`
4. When the virtual environment has been created, type the following in your console: `venv\Scripts\activate.bat`
5. Type `pip install -r requirements`

**Setting Up Your Creds**
1. Start by [creating an app](https://ssl.reddit.com/prefs/apps/) on Reddit, and getting its ID
and its secret.
2. Make sure you know the username and password of the Reddit account you used to make the app
3. Create a user-agent string consisting of "python:SubredditUserAnalysisTool:v1.0.0 (by /u/{YOUR_REDDIT_NAME})"
4. Run: `python Engine\Credentials.py --id {YOUR_APP_ID} --secret {YOUR_APP_SECRET} --username {YOUR_REDDIT_NAME} 
--password {YOUR_REDDIT_PASSWORD} --user_agent {YOUR_USER_AGENT_STRING}`
5. This will create a file called `credentials.json` in your root directory for the project

**Gathering Data**
1. Determine what subreddit you want to gather data of, how many posts worth of commentators you want to get data on,
where you want to write your data to, the number of comments a post must have for you to want commenters from it, and 
how much user history you want in either days or months. 
2. Run: `python Engine\SubredditUserAnalyzer.py --subreddit {THE_SUBREDDIT_TO_GET_DATA_ON} --posts {NUMBER_OF_POSTS 
--target_directory {WHERE_YOU_WANT_THE_DATA} --comment_threshold {NUMBER_OF_COMMENTS_FOR_POST_TO_COUNT} 
--{days|months} {NUM_DAYS_OR_MONTHS_OF_History}`
3. Runs can take a while on large data sets, so get comfy.
4. When the run is complete, you will have a new directory in the target directory you provided, which will give the
timestamp of the analysis and the name of the subreddit in its title. Within it, you will find two directories: Users,
which will contain the user data gathered, and Posts, which will have data and comment-chains from the posts used to
get users to do analysis upon.

## Output Data Schemas:

### Post
```
{
    'title': str,
    'permalink': str,
    'timestamp': int,
    'commenters': List[str],
    'comment_count': int,
    'comment_tree': List[Comment]
}
```

### Comment
```
{
    'permalink': str,
    'datetime': int,
    'subreddit': str,
    'content': str,
    'author': str,
    'children': List[Comment]
}
```