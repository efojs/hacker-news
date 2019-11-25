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


def save_stories(stories):
    # with open('./data/test_fetched_stories.json', 'r') as f:
    with open('./data/fetched_stories.json', 'r') as f:
        dict = json.load(f)
    dict.update(stories)
    # with open('./data/test_fetched_stories.json', 'w+') as f:
    with open('./data/fetched_stories.json', 'w+') as f:
        json.dump(dict, f)

def save_ids(ids):
    fetched_ids = read_ids("fetched")
    fetched_ids.extend(ids)
    fetched_ids.sort()
    # with open('test.csv', 'w+') as file:
    with open('fetched_stories_ids.csv', 'w') as file:
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
    print("start fetch:", time.ctime())
    # to load file once during main huge fetch
    # after move fetched_ids to is_fetched()
    fetched_ids = read_ids("fetched")
    print("Fetched IDs:\t", len(fetched_ids))

    all_ids = read_ids("all")
    last_id = all_ids[-1:]
    print("All IDs:\t", len(all_ids))
    print("To fetch:\t", len(all_ids)-len(fetched_ids))

    stories = {}
    i = 0
    count = 0
    for id in all_ids:
        if is_fetched(fetched_ids, id) != True:
            story = fetch(id)
            if len(story) != 0:
                stories[id] = story
                if i == 10 or id == last_id:
                    save_stories(stories)
                    save_ids(list(stories.keys()))
                    print(":", end="", flush=True)
                    stories = {}
                    i = 0
                print(".", end="", flush=True)
                i += 1
                count += 1
                if count % 1000 == 0:
                    print(count, end="", flush=True)
            else:
                print("(", id, ")", end="")


if __name__ == '__main__':
    # run via: $ python app.py
    fetch_stories()


# fastest way to check if a value is in a list:
# a = []
# for id in all_ids:
#     index = bisect.bisect_left(fetched_ids, id)
#     if index < len(fetched_ids):
#         if id == fetched_ids[index]:
#             a.append(id)
