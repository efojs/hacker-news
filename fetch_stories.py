import csv
import time
import bisect
import json
import requests

def read_ids(prefix):
    list = []
    with open("./data/" + prefix + '_stories_ids.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(int(row[0]))
    return list

def save_stories(stories):
    # with open('./data/test_fetched_stories.json', 'r') as f:
    with open('./data/json/fetched_stories.json', 'r') as f:
        dict = json.load(f)
    dict.update(stories)
    # with open('./data/test_fetched_stories.json', 'w+') as f:
    with open('./data/json/fetched_stories.json', 'w+') as f:
        json.dump(dict, f)

def save_ids(ids_to_save, prefix):
    ids_list = read_ids(prefix)
    old_len = len(ids_list)
    last_saved = ids_list[-1]

    # add news
    ids_list.extend(ids_to_save)

    # remove duplicates
    ids_list = list(set(ids_list))

    ids_list.sort()
    # with open('test.csv', 'w+') as file:
    with open("./data/" + prefix + '_stories_ids.csv', 'w') as file:
        writer = csv.writer(file)
        for id in ids_list:
            writer.writerow([id])

    added = len(ids_list)-old_len
    return {"added":added, "last_saved": last_saved }


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

def old_enough(story):
    if (time.time() - story["time"]) > 172800:
        return True
    else:
        return False


def make_to_fetch(fetched_ids):
    all_ids = read_ids("all")

    if len(fetched_ids) == 0:
        return all_ids
    else:
        return all_ids[all_ids.index(fetched_ids[-1])+1:]


def fetch_stories():
    print("start fetch:", time.ctime())

    fetched_ids = read_ids("fetched")
    print("Fetched IDs:\t", len(fetched_ids))

    to_fetch = make_to_fetch(fetched_ids)

    last_id = to_fetch[-1]
    print("To fetch:\t", len(to_fetch))

    stories = {}
    i = 0
    if len(to_fetch) < 20:
        i = len(to_fetch)

    count = 0
    for id in to_fetch:

        if is_fetched(fetched_ids, id) == False:
            story = fetch(id)
            if len(story) != 0 and not any(k in story for k in ["dead", "deleted"]):
                if old_enough(story):
                    stories[id] = story
                    if i == 20:
                        save_stories(stories)
                        save_ids(list(stories.keys()), "fetched")
                        print(":", end="", flush=True)
                        stories = {}
                        i = 0
                    print(".", end="", flush=True)
                    i += 1
                    count += 1
                    if count % 1000 == 0:
                        print(count, end="", flush=True)
                else:
                    print("")
                    break
            else:
                print(" ", end="")


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
