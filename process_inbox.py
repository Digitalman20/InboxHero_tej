from rules import check_rules
from classifier import classify_email
from safety import check_for_attack, log_refusal, log_decision


def process_inbox(emails, classifier=classify_email):
    decisions = []

    for email in emails:
        attack = check_for_attack(email)

        if attack is not None:
            decisions.append({"message_id": email["id"], "disposition": "flag", "reason": attack, "handled_by": "safety"})
            log_decision(decisions[-1])
            log_refusal(email, attack)
            continue

        rule_result = check_rules(email)

        if rule_result is not None:
            disposition, reason = rule_result
            handled_by = "rule"
        else:
            disposition, reason = classifier(email)
            handled_by = "llm"

        decisions.append({"message_id": email["id"], "disposition": disposition, "reason": reason, "handled_by": handled_by})
        log_decision(decisions[-1])

    return decisions