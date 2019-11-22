# save_fetched_stories.py
import json
# import copy

def save_fetched_stories(items, file_name):
    # file_name = "fetched_stories.json"

    with open(file_name, "r") as f:
        old_stories = json.load(f)

    # DROP DUPLICATES
    # convert to JSONed dict (with string keys)
    items_s = json.dumps(items)
    items_j = json.loads(items_s)
    # leave only uniq items on update
    old_stories.update(items_j)
    # rewrite file
    with open(file_name, "w") as f:
        json.dump(old_stories, f)

def save_ids(ids, case):
    упроститть сохранение айдишников: fetched_ids or all

    начать сохранять истории не моложе 1-2 дней


# def resave_fetched_stories():
#     file_name = "fetched_stories.json"
#     with open(file_name, "r") as f:
#         old_stories = json.load(f)
#
#     print("was:", len(old_stories.keys()))
#
#     filtered = copy.deepcopy(old_stories)
#     i = 0
#     for key in old_stories:
#         if "score" not in old_stories[key]:
#             i += 1
#             del filtered[key]
#     print(i)
#     print("is:", len(filtered.keys()))
#
#     # rewrite file
#     with open(file_name, "w") as f:
#         json.dump(filtered, f)
#
# # resave_fetched_stories()
