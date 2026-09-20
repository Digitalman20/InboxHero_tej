import sys

from extras import batch_receipts, create_daily_digest, summarize_thread
from inbox_loader import load_inbox
from process_inbox import process_inbox


if len(sys.argv) < 3 or sys.argv[1] != "--cap":
    print("Use: python demo.py --cap X1")
    sys.exit()

capability = sys.argv[2]
emails = load_inbox()

if capability == "X1":
    receipts = batch_receipts(emails)
    print(f"Archived {len(receipts)} receipts.")

elif capability == "X2":
    if len(sys.argv) < 5 or sys.argv[3] != "--thread":
        print("Use: python demo.py --cap X2 --thread t-launch")
        sys.exit()

    thread_id = sys.argv[4]
    summary = summarize_thread(thread_id, emails)
    print(summary)

elif capability == "X3":
    decisions = process_inbox(emails)
    digest = create_daily_digest(decisions, emails)
    print(digest)

else:
    print("Unknown capability.")