# part4.py
import json
import os


def save_pending_actions(pending_actions):
    with open("pending_actions.json", "w") as file:
        json.dump(pending_actions, file, indent=2)


def load_pending_actions():
    if not os.path.exists("pending_actions.json"):
        return []

    with open("pending_actions.json", "r") as file:
        return json.load(file)


def log_approval(message_id, proposed_action, user_answer, happened):
    event = {"message_id": message_id,
        "proposed_action": proposed_action,
        "user_answer": user_answer,
        "happened": happened}

    with open("trace.jsonl", "a") as file:
        file.write(json.dumps(event) + "\n")


def ask_for_approval(action):
    print("\nMessage:", action["message_id"])
    print("Proposed action: Send this draft")
    print("Reason: Sending an email cannot be undone.")
    print("\nDraft:")
    print(action["draft"])

    answer = input("\nApprove? (yes/no): ").lower()

    return answer == "yes"


def send_to_outbox(action):
    os.makedirs("outbox", exist_ok=True)

    path = f"outbox/{action['message_id']}.json"

    with open(path, "w") as file:
        json.dump(action, file, indent=2)

    return path


def approve_pending_actions():
    pending_actions = load_pending_actions()

    for action in pending_actions:
        approved = ask_for_approval(action)

        if approved:
            send_to_outbox(action)

            log_approval(action["message_id"],
                "send draft",
                "approved",
                "draft written to outbox",)
            

            print("Draft sent to outbox.")

        else:
            log_approval(action["message_id"],
                "send draft",
                "rejected",
                "nothing was sent",)
            

            print("Draft was not sent.")