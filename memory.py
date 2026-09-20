import json
import os
from datetime import datetime




def load_memory(file_name="memory.json"):
    if not os.path.exists(file_name):
        return {
            "facts": {},
            "history": [],
        }

    with open(file_name, "r") as file:
        return json.load(file)


def save_memory(memory, file_name="memory.json"):
    with open(file_name, "w") as file:
        json.dump(memory, file, indent=2)


def remember(key, value, source, file_name="memory.json"):
    memory = load_memory(file_name)
    now = datetime.now().isoformat()

    old_fact = memory["facts"].get(key)

    if old_fact is not None and old_fact["value"] != value:
        memory["history"].append({
            "key": key,
            "old_value": old_fact["value"],
            "new_value": value,
            "old_source": old_fact["source"],
            "new_source": source,
            "changed_at": now,
        })

    memory["facts"][key] = {
        "value": value,
        "source": source,
        "updated_at": now,
    }

    save_memory(memory, file_name)


def recall(key, file_name="memory.json"):
    memory = load_memory(file_name)

    return memory["facts"].get(key)


def search_memory(query, file_name="memory.json"):
    memory = load_memory(file_name)
    matches = []

    query = query.lower()

    for key, fact in memory["facts"].items():
        if query in key.lower() or query in str(fact["value"]).lower():
            matches.append({
                "key": key,
                "value": fact["value"],
                "source": fact["source"],
            })

    return matches