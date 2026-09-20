import json


def load_inbox(path="inbox.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)