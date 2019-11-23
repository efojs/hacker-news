import csv
import time
import bisect
import json
import requests

def read_ids(prefix):
    list = []
    with open(prefix + '_stories_ids.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(int(row[0]))
    return list


def save_story(story):
    with open('./data/fetched_stories.json', 'r') as f:
        dict = json.load(f)
    dict.update(story)
    with open('./data/fetched_stories.json', 'w+') as f:
        json.dump(dict, f)

def save_id(id):
    fetched_ids = read_ids("fetched")
    fetched_ids.append(id)
    fetched_ids.sort()
    with open('fetched_stories_ids.csv', 'w+') as file:
    # with open('fetched_stories_ids.csv', 'w') as file:
        writer = csv.writer(file)
        for id in fetched_ids:
            writer.writerow([id])





def is_fetched(fetched_ids, id):
    index = bisect.bisect_left(fetched_ids, id)
    if index < len(fetched_ids):
        if id == fetched_ids[index]:
            return True
    return False




def get_story(id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(id) + '.json?print=pretty'
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def fetch(id):
    try:
        story = get_story(id)
    except requests.RequestException as e:
        print("\nfailed request:", id)
        print("error:", e)
    else:
        if story != None and story["type"] == "story":
            # print(id, end=",")
            return story
    return {}



def fetch_stories():
    # to load file once during main huge fetch
    # after move old_ids to is_fetched()
    old_ids = read_ids("fetched")
    print("old_ids:", len(old_ids))

    for id in read_ids("all"):
        if is_fetched(old_ids, id) != True:
            story = fetch(id)
            save_story({id: story})
            save_id(id)
            print(".", end="")


fetch_stories()

# a = []
# for id in all_ids:
#     index = bisect.bisect_left(fetched_ids, id)
#     if index < len(fetched_ids):
#         if id == fetched_ids[index]:
#             a.append(id)
