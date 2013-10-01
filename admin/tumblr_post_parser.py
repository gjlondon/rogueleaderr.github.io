from collections import defaultdict
import json
import os
import datetime

import requests

def get_posts():
    headers = {'content-type': 'application/json'}
    url = "http://rogueleaderr.com/api/read/json?num=100"
    r = requests.get(url, headers=headers)

    split_text = r.text.split("=", 1)
    clean_text = split_text[1].strip(";\n")
    post_json = json.loads(clean_text)

    posts = []
    for item in post_json['posts']:
        post = generate_post(item)
        if post:
            posts.append(post)
    return posts


def copy_posts(posts):
    for item in posts:
        slug, post = item
        slug += ".md"
        folder = "../content/posts/tumblr"
        try:
            with open(os.path.join(folder, slug)):
                print(slug, "already exists.")
                continue
        except IOError:
            f = open(os.path.join(folder, slug), "w")
            f.write(post.encode("utf8"))


def generate_post(tumblr_post):
    try:
        date = datetime.datetime.utcfromtimestamp(tumblr_post["unix-timestamp"])
        tumblr_post["date"] = date.strftime('%Y-%m-%d %H:%M')
    except KeyError:
        pass
    except:
        import pdb ; pdb.set_trace()
    for key in ("regular-body", "slug", "date", "tags"):
        if key not in tumblr_post:
            tumblr_post[key] = ""
    tumblr_post["folder_slug"] = "tumblr/" + tumblr_post["slug"]
    tumblr_post["str-tags"] = []
    for tag in tumblr_post["tags"]:
        # otherwise pelican shows tags as u'tag'
        try:
            tumblr_post["str-tags"].append(str(tag))
        except UnicodeDecodeError as e:
            print e
            pass
    try:
        post =  u"""Title: {regular-title}
Slug: {folder_slug}
Date: {date}
Tags: {str-tags}

{regular-body}
""".format(**tumblr_post)
        return (tumblr_post["slug"], post)
    except KeyError:
        # media posts without a regular title won't render without custom code, so skip them
        print("skipping {} because it's media".format(tumblr_post["slug"]))
        return


def run():
    posts = get_posts()
    copy_posts(posts)


if __name__ == "__main__":
    run()