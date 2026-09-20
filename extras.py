import json
import os

from dashboard import find_commitments
from llm import call_ollama
from outbox import load_pending_actions
from thread import get_thread


def batch_receipts(emails):
    receipts = []

    for email in emails:
        if "receipt" in email["subject"].lower():
            receipts.append({"message_id": email["id"], "subject": email["subject"], "disposition": "archive", "reason": "Batch archived receipt."})

    os.makedirs("output", exist_ok=True)

    with open("output/receipt_batch.json", "w") as file:
        json.dump(receipts, file, indent=2)

    return receipts


def summarize_thread(thread_id, emails):
    selected_email = None

    for email in emails:
        if email["thread_id"] == thread_id:
            selected_email = email
            break

    if selected_email is None:
        return None

    thread = get_thread(selected_email, emails)

    prompt = f"""
        Summarize this email thread.

        State:
        1. The important information.
        2. The current open question or next step.

        Thread:
        {json.dumps(thread, indent=2)}
        """

    messages = [{"role": "system", "content": "You summarize email threads."}, {"role": "user", "content": prompt}]

    response = call_ollama(messages)
    summary = response["content"]

    os.makedirs("output", exist_ok=True)

    with open("output/thread_summary.txt", "w") as file:
        file.write(summary)

    return summary


def create_daily_digest(decisions, emails):
    pending_actions = load_pending_actions()
    commitments = find_commitments(emails)
    flagged = []

    for decision in decisions:
        if decision["disposition"] == "flag":
            flagged.append(decision)

    digest = "DAILY DIGEST\n\n"

    digest += "PENDING ACTIONS\n"
    for action in pending_actions:
        digest += f"- {action['message_id']}: Draft waiting for approval.\n"

    digest += "\nFLAGGED\n"
    for decision in flagged:
        digest += f"- {decision['message_id']}: {decision['reason']}\n"

    digest += "\nDATES AND DEADLINES\n"
    for commitment in commitments:
        sources = ", ".join(commitment["source_ids"])
        digest += f"- {commitment['date']}: {commitment['title']} ({sources})\n"

    os.makedirs("output", exist_ok=True)

    with open("output/daily_digest.txt", "w") as file:
        file.write(digest)

    return digest