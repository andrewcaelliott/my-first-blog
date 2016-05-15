from pytumblr import TumblrRestClient
import json
from bs4 import BeautifulSoup
from random import choice

client = TumblrRestClient('9g1lRa75IJ7HLbnyqMCaXsSsnvyz8uUsa7ZLzyGCipFciA23PM')

def tumblrSelection(category):
    storyposts = posts(tag=category)
    #storyposts = [{'body': '<p><a href="https://en.wikipedia.org/wiki/Universe">https://en.wikipedia.org/wiki/Universe</a></p><p>No, literally.</p><p>As Douglas Adams said, the universe is big. Really big</p>', 'short_url': 'https://tmblr.co/ZJc03i22P_y9r', 'tags': ['passion'], 'title': 'Astronomical Numbers', 'plain': 'https://en.wikipedia.org/wiki/UniverseNo, literally.As Douglas Adams said, the universe is big. Really big', 'date': '2016-02-26 10:38:48 GMT', 'img_url': None, 'link_url': '<a href="https://en.wikipedia.org/wiki/Universe">https://en.wikipedia.org/wiki/Universe</a>', 'post_url': 'http://itabn.tumblr.com/post/140022366837/astronomical-numbers'}, {'body': '<p><a href="https://en.wikipedia.org/wiki/Number">https://en.wikipedia.org/wiki/Number</a></p><p>It starts with counting: 1, 2, 3 are what the maths guys call the Natural Numbers. From there it gets more and more UN-natural, all the way to imaginary and beyond, to some very weird structures that still get called numbers.</p>', 'short_url': 'https://tmblr.co/ZJc03i22P_oKs', 'tags': ['passion'], 'title': 'You Call That a Number?', 'plain': 'https://en.wikipedia.org/wiki/NumberIt starts with counting: 1, 2, 3 are what the maths guys call the Natural Numbers. From there it gets more and more UN-natural, all the way to imaginary and beyond, to some very weird structures that still get called numbers.', 'date': '2016-02-26 10:37:01 GMT', 'img_url': None, 'link_url': '<a href="https://en.wikipedia.org/wiki/Number">https://en.wikipedia.org/wiki/Number</a>', 'post_url': 'http://itabn.tumblr.com/post/140022326582/you-call-that-a-number'}]
    stories={}
    if storyposts:
        featureStory = storyposts[0]
    else:
        featureStory = None
    #todo handle zero stories
    feature_candidates = []
    for post in storyposts:
        if post["featured"]:
            feature_candidates.append(post)

    featureStory = choice(feature_candidates)
    stories["featured"]=featureStory
    if featureStory:
        storyposts.remove(featureStory)
    stories["other"]=storyposts
    return stories

def posts(**kwargs):
    postlist = client.posts('itabn.tumblr.com', filter='html', **kwargs)
    result = []
    for post in postlist["posts"]:
        result.append(post_summary(post))
    return result

def grab_link(body):
    if body.find("<a")>=0:
        link = body[body.find("<a"):body.find("</a>")+4]
    else:
        link = None
    if link:
        href_start = link.find("href=")
        link_url = link[href_start+6:href_start+6+link[href_start+6:].find('"')]
        #link_url = link[href_start+6:]
        body = body.replace(link, '')
        link_url= link_url.replace("http://www.isthatabignumber.com","/.")
    else:
        link_url = None
    return link_url, body        

def post_summary(post):
    body = post["body"]
    link_urls = []
    while body.find("<a")>=0:
        link_url, body = grab_link(body)
        link_urls.append(link_url)
    img_start = body.find('<img src=')
    if img_start>=0:
        img_url = body[img_start+10:img_start+10+body[img_start+10:].find('"')]
    else:
        img_url = None
    soup = BeautifulSoup(body, "html.parser")
    #plain_body = soup.get_text()
    plain_body = []
    for string in soup.stripped_strings:
        plain_body+=[string]

    if len(link_urls)==0:
        link_urls.append(post["post_url"])

    return {
#{"title":storyName, "synopsis":synopsis,"link":sourceLink}
        "title":post["title"],
        "synopsis":plain_body,
        "links":link_urls,
        "featured": "featured" in post["tags"],

#        "post_url":post["post_url"],
#        "short_url":post["short_url"],
#        "date":post["date"],
#        "tags":post["tags"],
#        "body":post["body"],
#        "link_url":link_url,
        "img_url":img_url,
    }


