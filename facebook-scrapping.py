
# coding: utf-8

# In[65]:

import urllib, json, pandas
import datetime


# In[89]:

access_token = "myaccesstoken"
page_ids = ["JeffreeStar", "hudabeauty", "itcosmetics", "PeachAndLily", "Ulta-Beauty-633386723515485"]
# page_ids = ["elfcosmetics"]


# In[ ]:

for page_id in page_ids:
    print(page_id)
    total_posts_received = 0
    top_250_posts = []
    posts_url = (
        "https://graph.facebook.com/v2.12/"
        + page_id
        + "/posts?pretty=0&limit=10&fields=created_time%2Cmessage%2Cid%2Cstory%2Clikes.summary(true),comments.limit(10000)%2Cshares"
        + "&access_token=" + access_token
    )
    print(posts_url)
    page_no = 1
    while(total_posts_received < 250):
        if(posts_url is not None):
            print("fetching page no. " + str(page_no))
            response = urllib.request.urlopen(posts_url).read()
            posts = json.loads(response.decode("utf-8"))
            total_posts_received += len(posts["data"])
#             print(posts.keys())
            for post in posts["data"]:
                post["likes"] = post["likes"]["summary"]["total_count"] if "likes" in post.keys() else 0
                post["shares"] = post["shares"]["count"] if "shares" in post.keys() else 0
                post["comments"] = post["comments"]["data"] if "comments" in post.keys() else []
            top_250_posts.extend(posts["data"])
            posts_url = posts["paging"]["next"] if "paging" in posts.keys() and "next" in posts["paging"].keys() else None
            page_no += 1
            
        else:
            print("posts url is none")
            break
    print("no of posts: " + str(len(top_250_posts)))
    json.dump(top_250_posts, open("facebook_" + page_id + "___" + datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') + ".json", "w", encoding="utf-8"))


# In[53]:



