import requests
import random





def get_random_wiki_topic():
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": "Category:Psychology",
        "cmlimit": 100,
        "cmtype": "page"
    } 

    headers = {
        "User-Agent": "bot (https://github.com/dhavalpoonia)"
    }

    r = requests.get(URL, params=params, headers=headers)
    data = r.json()
    pages = data["query"]["categorymembers"]

    topic = random.choice(pages)

    topic_name = topic['title']
    print(f"Topic Name: {topic_name}")
    return topic_name



def get_wiki_topic_summary(topic):
    topic 
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": topic,
        # "exchars": 5000,
        "exsentences": 20,
        "explaintext": True,

        "exsectionformat": "plain"
    } 

    headers = {
        "User-Agent": "bot (https://github.com/dhavalpoonia)"
    }

    r = requests.get(URL, params=params, headers=headers)
    data = r.json()
    pages = data['query']['pages']

    pages_id = list(pages.keys())[0]

    extract = pages[pages_id]['extract']
    print(pages)
    print(extract)

    paras = _refine_extract(extract)
    # print(paras)
    return paras

def _refine_extract(extract):
    paras = extract.split('\n') 
    # print(paras)
    return paras


topic = 'Frequency illusion' 

get_wiki_topic_summary(topic)


