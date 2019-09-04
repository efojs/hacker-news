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
from apscheduler.schedulers.blocking import BlockingScheduler

filename = "newstories.csv"

def get_news():
    r = requests.get("https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty")
    return r.json()

def save_news_to_file():
    series = pd.DataFrame(news)
    series.to_csv(filename, header=None, index=None)

def grab_and_add_news():
    # load news
    news = get_news()

    # convert news to DataFrame
    news = pd.DataFrame(news)

    # load old file
    old_data = pd.read_csv(filename, header=None)
    old_len = len(old_data)

    # merge with news
    new_data = old_data.append(news)

    # leave only unique
    new_data = new_data.drop_duplicates(keep='first')
    print(datetime.datetime.now())
    print("added: " + str(len(new_data)-old_len))

    # sort
    new_data = new_data.sort_values(by=0, ascending=True)

    # save file
    new_data.to_csv(filename, header=None, index=None)

# grab_and_add_news()
scheduler = BlockingScheduler()
scheduler.add_job(grab_and_add_news, 'interval', hours=5)
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
