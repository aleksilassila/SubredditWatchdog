import praw, requests, os

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

    def sendMessage(self, title, content):
        requests.post(
            self.slackurl,
            data = json.dumps({"text": f"{title}:\n{content}"})
        )
        print(f"[+] Sent notification")

    def watch(self):
        for postId in reddit.subreddit(self.subredditName).stream.submissions():
            print(f"[+] Caught new post: {postId}")
            
            title = print(reddit.submission(postId).title)
            content = print(reddit.submission(postId).selftext)

            self.sendMessage(title, content)


if __name__ == "__main__":
    SubredditWatchdog(os.environ.get("REDDIT_ID"), os.environ.get("REDDIT_SECRET"), os.environ.get("SURL"), "TweakBounty")
