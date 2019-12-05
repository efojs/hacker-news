# Grabs list of new HackerNews stories
# every 5 hours
# and adds to file
# https://github.com/HackerNews/API

import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler

import fetch_stories as fetch

filename = "all_stories_ids.csv"

def get_news():
    r = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty")
    return r.json()

def grab_and_add_news():
    # load news
    news = get_news()
    first_new = news[0]
    print("first_new:", first_new)

    # save news to file
    results = fetch.save_ids(news, "all")

    # in case there was a downtime we missed some IDs and get all 500 new
    # to get them check each between last saved and first new
    if results["added"] >= 500 and results["last_saved"] != first_new:  # != first_new — what for?
        fetch_miising_ids(range(results["last_saved"], first_new))

    # fetch stories
    fetch.fetch_stories()

def fetch_miising_ids(range):
    ids = []
    # failed_requests = []
    print("Fetching lost IDs")
    print(range)
    print("IDs to go:", len(range)-1)
    print("Start fetch:", time.ctime(time.time()))
    passed = 0
    range_len = len(range)
    for i in range:
        print("*"*int((passed/range_len)*10) + "_"*int(((range_len-passed)/range_len)*10) + " | " + str(passed), end="\r")
        passed += 1
        if i not in ids:
            item = fetch.fetch(i)
            if len(item) != 0:
                ids.append(i)
    print("\nEnd fetch:", time.ctime(time.time()))
    results = fetch.save_ids(ids, "all")
    print("added fetched ids:", results["added"])


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
