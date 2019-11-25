import csv
import json

def read_ids(prefix):
    list = []
    with open(prefix + '_stories_ids.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            list.append(int(row[0]))
    return len(list)


def fetched():
    with open('./data/fetched_stories.json', 'r') as f:
        dict = json.load(f)
    return len(dict)


all_ids = read_ids("all")
fetched = fetched()

print("All IDs:\t", all_ids)
print("Fetched:\t", fetched)
print("To fetch:\t", all_ids-fetched)
