import json
import sys
#imports to process the emails
from inbox_loader import load_inbox
from process_inbox import process_inbox

#thread
from thread import make_reply_draft
# outbox
from outbox import save_pending_actions, approve_pending_actions
#memory
from memory import remember, recall

from dashboard import create_dashboard



#  helpers
def save_decisions(decisions):
    with open("decisions.json", "w") as file:
        json.dump(decisions, file, indent=2)

def get_email(inbox, message_id):
    for email in inbox:
        if email["id"] == message_id:
            return email

    return None


def main():

    with open("trace.jsonl", "w") as file:
        file.write("")

    #__________________________Inbox processing+remember/recall prefeferences_____________
    emails = load_inbox()

    for email in emails:
        body = email["body"].lower()

        if email["from"] == "sam@paperjet.io":
            if "do not take meetings before 11:00am" in body:
                remember(
                    "meeting_before_11",
                    False,
                    email["id"],
                )

    decisions = process_inbox(emails)

    meeting_preference = recall("meeting_before_11")

    if meeting_preference is not None:
        if meeting_preference["value"] is False:

            for decision in decisions:
                email = get_email(emails, decision["message_id"])
                body = email["body"].lower()

                if "9:00am" in body or "10:00am" in body:
                    decision["disposition"] = "escalate"
                    decision["reason"] = (
                        "This meeting request conflicts with the saved "
                        "no-morning-meetings preference."
                    )

    save_decisions(decisions)

    rule_handled = 0

    for decision in decisions:
        if decision["handled_by"] == "rule":
            rule_handled += 1

    print(f"Processed: {len(decisions)}")
    print(f"Rule handled: {rule_handled}")
    print(f"LLM handled: {len(decisions) - rule_handled}")

    flagged = []

    for decision in decisions:
        if decision["disposition"] == "flag":
            flagged.append(decision)

    print(f"Flagged: {len(flagged)}")

    for decision in flagged:
        print(f"{decision['message_id']}: {decision['reason']}")
    #_________________________draft and approval __________________________


    pending_actions = []
    reply_count = 0
    for decision in decisions:
        if decision["disposition"] == "reply":
            reply_count += 1
            email = get_email(emails, decision["message_id"])

            if email is not None:
                draft = make_reply_draft(email, emails)
                print("Draft for", email["id"], ":", draft)

                if draft is not None:
                    pending_actions.append(draft)
    print("Reply decisions:", reply_count)
    print("Pending actions:", len(pending_actions))
    save_pending_actions(pending_actions)

    #_____________________

    create_dashboard(pending_actions, decisions, emails)


if __name__ == "__main__":
    if "--approve" in sys.argv:
        approve_pending_actions()
    else:
        main()