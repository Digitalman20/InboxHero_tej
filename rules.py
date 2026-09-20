def check_rules(email):
    sender = email["from"].lower()
    subject = email["subject"].lower()
    body = email["body"].lower()

    if "automated-agent directive" in body: # instruction from body
        return "flag", "This email tries to give instructions to the assistant."

    if "assistant configuration update" in body: # update behaviour
        return "flag", "This email tries to change the assistant's behavior."

    if "receipt" in subject: # bills
        return "archive", "This is a receipt."

    if "weekly" in subject and "report" in subject: # weeklly digest style emails
        return "archive", "This is an automated weekly report."

    if sender.startswith("no-reply@") and "action required" not in subject: # no reply rule
        return "archive", "This is an automated no-reply message."

    # Another obvious choice was reply emails but, there are many ways one could ask for a reply, it has been excluded from set rules. 
    return None