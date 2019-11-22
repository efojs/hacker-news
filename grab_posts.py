# Grabs list of new HackerNews stories
# every 5 hours
# and adds to file
# https://github.com/HackerNews/API

import json
import csv
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler

filename = "all_stories_ids.csv"

def get_news():
    r = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty")
    return r.json()

def grab_and_add_news():
    # load news
    news = get_news()

    # convert news to DataFrame
    news = pd.DataFrame(news)
    first_new = news[:1].iloc[0][0]
    print("first_new:", first_new)

    results = add_news(news)

    # in case there was a downtime we missed some IDs and get all 500 new
    # to get them check each between last saved and first new
    if results["added"] >= 500 and results["last_saved"] != first_new:
        fetch_miising_ids(range(results["last_saved"], first_new))

def add_news(to_add):
    # load old file
    old_data = pd.read_csv(filename, header=None)
    old_len = len(old_data)
    last_saved = old_data[-1:].iloc[0][0]

    # merge with news
    new_data = old_data.append(to_add)

    # leave only unique
    new_data = new_data.drop_duplicates(keep='first')

    # count how much IDs added
    added = len(new_data)-old_len

    # sort
    new_data = new_data.sort_values(by=0, ascending=True)

    # save file
    new_data.to_csv(filename, header=None, index=None)

    # print what's added
    print("added: " + str(added) + "\ttotal: " + str(len(new_data)) + "\t" + datetime.datetime.now().ctime())

    return {"added":added, "last_saved": last_saved }

def get_item(id):
    url = 'https://hacker-news.firebaseio.com/v0/item/' + str(id) + '.json?print=pretty'
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def fetch_miising_ids(range):
    items = {}
    failed_requests = []
    print("Fetching lost IDs")
    print(range)
    print("IDs to go:", len(range)-1)
    print("Start fetch:", time.ctime(time.time()))
    passed = 0
    range_len = len(range)
    for i in range:
        print("*"*int((passed/range_len)*10) + "_"*int(((range_len-passed)/range_len)*10) + " | " + str(passed), end="\r")
        passed += 1
        time.sleep(0.1)
        try:
            item = get_item(i)
        except requests.RequestException as e:
            failed_requests.append(i)
        else:
            if item != None and item["type"] == "story" and "score" in item:
                if i not in items:
                    items[i] = item
    print("\nEnd fetch:", time.ctime(time.time()))
    print("Failed_requests:", end="")
    print(failed_requests)
    save_fetched_items(items)

def save_fetched_items(items):
    # save fetched stories
    # to avoid duplicates
    with open("fetched_stories.json", "r") as f:
        old_stories = json.load(f)

    # to drop duplicates convert to JSONed dict (with string keys)
    items_s = json.dumps(items)
    items_j = json.loads(items_s)
    # leaves only uniq keys
    old_stories.update(items_j)
    # rewrite file
    with open("fetched_stories.json", "w") as f:
        json.dump(old_stories, f)

    # save fetched IDs
    # load saved fetched IDs
    old_fetched_ids = pd.read_csv("fetched_stroies_ids.csv", header=None)
    # merge
    new_fetched_ids = old_fetched_ids.append(pd.DataFrame(items.keys()))
    # clean
    new_fetched_ids = new_fetched_ids.drop_duplicates(keep='first')
    # sort
    new_fetched_ids = new_fetched_ids.sort_values(by=0, ascending=True)
    # save
    new_fetched_ids.to_csv("fetched_stroies_ids.csv", header=None, index=None)
    # show
    print("added fetched ids:", len(new_fetched_ids)-len(old_fetched_ids))



grab_and_add_news()
scheduler = BlockingScheduler()
scheduler.add_job(grab_and_add_news, 'interval', hours=2)
scheduler.start()




# 20832555
# ...
# 20859471
# 20872564


# ----------

# to load manuay collected data
# def load_manual():
#     with open("newstories.txt", "r") as f:
#         list_of_string_numbers = f.read().split(', ')
#         list_of_ints = list(map(int, list_of_string_numbers))
#         print(len(list_of_ints))
#         set_of_numbers = set(list_of_ints)
#         print(len(set_of_numbers))
#
#         series = pd.DataFrame(set_of_numbers)
#         series = series.sort_values(by=0, ascending=True)
#         series.to_csv(filename, header=None, index=None)
#
#         pass
