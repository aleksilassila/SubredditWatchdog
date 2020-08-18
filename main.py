import praw, requests, os, json
from datetime import datetime
from time import sleep

class SubredditWatchdog:
    def __init__(self, redditId, secret, slackurl, subredditName):
        self.id = redditId
        self.secret = secret
        self.slackurl = slackurl

        self.subredditName = subredditName

        self.reddit = praw.Reddit(
            client_id=self.id,
            client_secret=self.secret,
            user_agent="linux:me.aleksilassila.subredditwatchdog:v1 (by u/0x3A7F14)")

    def sendMessage(self, title, content, time, link):
        requests.post(
            self.slackurl,
            data = json.dumps({"text": f"{datetime.utcfromtimestamp(time).strftime('%d.%m %H:%M')}\n{title}:\n{content}\nSource: {link}\n\n"})
        )
        print(f"[+] Sent notification")

    def watch(self):
        while True:
            try:
                for postId in self.reddit.subreddit(self.subredditName).stream.submissions():
                    print(f"[+] Caught new post: {postId}")

                    submission = self.reddit.submission(postId)

                    title = submission.title
                    content = submission.selftext
                    time = submission.created_utc
                    link = submission.url

                    self.sendMessage(title, content, time, link)
            except: sleep(60)


if __name__ == "__main__":
    watchdog = SubredditWatchdog(os.environ.get("REDDIT_ID"), os.environ.get("REDDIT_SECRET"), os.environ.get("SURL"), "TweakBounty")
    watchdog.watch()
