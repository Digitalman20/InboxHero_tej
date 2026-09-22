import sys

from extras import batch_receipts, create_daily_digest, summarize_thread
from inbox_loader import load_inbox
from process_inbox import process_inbox

def run_all(emails):
    receipts = batch_receipts(emails)
    print(f"Created a batch report for {len(receipts)} receipts.")

    summary = summarize_thread("t-launch", emails)
    print("\nThread summary:")
    print(summary)

    decisions = process_inbox(emails)
    digest = create_daily_digest(decisions, emails)
    print("\nDaily digest:")
    print(digest)


if len(sys.argv) < 2:
    print("Use: python demo.py --cap X1")
    print("Or: python demo.py --all")
    sys.exit()

emails = load_inbox()

if sys.argv[1] == "--all":
    run_all(emails)

elif sys.argv[1] == "--cap":
    if len(sys.argv) < 3:
        print("Use: python demo.py --cap X1")
        sys.exit()

    capability = sys.argv[2]

    if capability == "X1":
        receipts = batch_receipts(emails)
        print(f"Created a batch report for {len(receipts)} receipts.")

    elif capability == "X2":
        if len(sys.argv) < 5 or sys.argv[3] != "--thread":
            print("Use: python demo.py --cap X2 --thread t-launch")
            sys.exit()

        summary = summarize_thread(sys.argv[4], emails)
        print(summary)

    elif capability == "X3":
        decisions = process_inbox(emails)
        digest = create_daily_digest(decisions, emails)
        print(digest)

    else:
        print("Unknown capability. Use X1, X2, or X3.")

else:
    print("Use: python demo.py --cap X1")
    print("Or: python demo.py --all")