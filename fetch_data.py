import csv
import time
import bisect
import json

# fetched_ids = []
# with open('fetched_stories_ids.csv') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         fetched_ids.append(int(row[0]))
#
# all_ids = []
# with open('all_stories_ids.csv') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         all_ids.append(int(row[0]))
#
# a = []
# for id in all_ids:
#     index = bisect.bisect_left(fetched_ids, id)
#     if index < len(fetched_ids):
#         if id == fetched_ids[index]:
#             a.append(id)

test = {"20840711237": {"by": "R3G1R", "dead": "true"}}

def save_story(story):
    with open('./data/fetched_stories.json', 'r') as f:
        dict = json.load(f)
    # dict.update(story)
    # with open('./data/fetched_stories.json', 'w') as f:
    #     json.dump(dict, f)
    # # save story key


save_story(test)
