from config import CLIENT_SECRET
import praw
from random import choice
from config import *

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,)

TOPICS = [  # Default Topics When No Topic is given!!
    "dankmemes",
    "memes",
    "AdviceAnimals",
    "MemeEconomy"
]


def ScrapMemes(topic=0, num=1):
    '''
    topic: The Name Of Subreddit to search for memes.. If default will choose random topic from the TOPICS list

    Each subreddit has five different ways of organizing the topics created by redditors: .hot, .new, .controversial, .top, and .gilded. You can also use .search("SEARCH_KEYWORDS") to get only results matching an engine search.
    '''
    try:
        if num <= 0:
            return {
                "code": 400,
                "message": "Enter a positive Integer less than 200"
            }
        result = {}
        num = num % 200
        if topic == 0:
            topic = choice(TOPICS)
        if num == 1:
            subreddit = reddit.subreddit(topic)
            meme = subreddit.random()
            result = {
                "code":200,
                "post_link": meme.shortlink,
                "subreddit": topic,
                "title": meme.title,
                "url": meme.url,
                "ups": meme.ups,
                "author": meme.author.name,
                "spoilers_enabled": subreddit.spoilers_enabled,
                "nsfw": subreddit.over18,
                "image_previews": [i["url"] for i in meme.preview.get("images")[0].get("resolutions")]
            }
        else:
            subreddit = reddit.subreddit(topic)
            submissions = subreddit.random_rising(limit=num)
            result = {
                "code":200,
                "count": num,
                "memes": []
            }
            for meme in submissions:
                try:
                    _=meme.preview
                    item = {
                        
                        "post_link": meme.shortlink,
                        "subreddit": topic,
                        "title": meme.title,
                        "url": meme.url,
                        "ups": meme.ups,
                        "author": meme.author.name,
                        "spoilers_enabled": subreddit.spoilers_enabled,
                        "nsfw": subreddit.over18,
                        "image_previews": [i["url"] for i in meme.preview.get("images")[0].get("resolutions")]
                    }
                except Exception as e:
                    item = {
                        
                        "post_link": meme.shortlink,
                        "subreddit": topic,
                        "title": meme.title,
                        "url": meme.url,
                        "ups": meme.ups,
                        "author": meme.author.name,
                        "spoilers_enabled": subreddit.spoilers_enabled,
                        "nsfw": subreddit.over18,
                        "image_previews": ["No Preview Found For This Meme.. Sorry For That"]
                    }
                result.get("memes").append(item)
        return result

    except Exception as e:
        return {
            "code":400,
            "message":str(type(e))+str(e)
        }

# sub=reddit.subreddit("dankmemes")
# print(sub.spoilers_enabled)


if __name__ == "__main__":
    print(ScrapMemes(topic="ProgrammerHumor",num=3))
