import os
import re

tweets_path=r"D:\get_tweets\mutilated_catal_tweets.txt"
tweets_fail_path=r"D:\get_tweets\mutilated_catal_fail_tweets.txt"
# tweets_path=r"D:\get_tweets\cc.txt"

with open(tweets_path,"r",encoding="utf-8") as f:
    lines_s=f.read()


patt="Link:\s(https://twitter.com/mutilated_catal/status/\d+)\sTweet:\s+Link:"

fail_links=re.findall(patt,lines_s,re.S)

fail_links_s="\n".join(fail_links)

with open(tweets_fail_path,"a",encoding="utf-8") as f:
    f.write(fail_links_s)

