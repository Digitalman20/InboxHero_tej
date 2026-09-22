# CAPABILITIES.md —

**Student:** Tej Kandimalla, cert-aai-2026-06-0038
**Repository:** https://github.com/Digitalman20/InboxHero_tej/tree/main

Run everything through one entry point:

```
python demo.py --cap X1
python demo.py --cap X2 --thread t-launch
python demo.py --cap X3
python demo.py --all
python main.py          end to end run
python main.py --approve    
```

---

## The system, in one paragraph



InboxHero is a local email-agent prototype built with plain Python. It loads a mock inbox, checks for suspicious emails and runs simple rules first to sort, then uses a local Ollama model to classify any remaining emails. Emails that require any response (disposition = reply) get a grounded draft using the context from the thread. They are saved as pending actions and require approval (We have to run python main.py --approve to get to the approval loop). Preferences are stored in JSON so they continue to affect behavior after a restart. A Flask dashboard displays pending actions, flagged messages, and commitments.

## Design choices you were asked to state

- **Framework:** The pipeline itself is super simple, so no framework was used as it requires alot more planning before execution.
- **Retrieval:** The inbox has structured threads, so going through them is fairly simple. We basically use `thread_id` for retrivals.
- **Approval gate:** Reply drafts are saved to pending_actions.json. The user must run python main.py --approve and answer yes before an approved draft is written to outbox/.
- **Persistent memory:** memory.json stores user preferences and a history of changes.
- **Safety:** Suspicious instructions, phishing links, impersonation, and bank-detail changes are flagged. Safety refusals are recorded in trace.jsonl.

## Capabilities

| ID | Name | Tier | One-line claim |
|---|---|---:|---|
| R1 | Inbox classification | B | Every inbox message receives one disposition and reason. |
| R2 | Grounded reply drafts | B | Drafts use only the matching thread and cite source message IDs. |
| R3 | Approval-gated outbox | C | A draft enters `outbox/` only after explicit approval. |
| R4 | Persistent preferences | C | A saved preference survives restarts and changes later handling. |
| R5 | Safety refusal log | C | Suspicious emails are flagged, left in place, and logged. |
| R6 | Dashboard | C | Flask displays pending actions, flagged emails, and commitments. |
| X1 | Receipt batch report | B | Creates a report for receipt and shipping emails. |
| X2 | Thread summarizer | B | Summarizes a selected email thread. |
| X3 | Daily digest | B | Summarizes decisions, flagged messages, and commitments. |

## Evidence files
`decisions.json` stores the disposition and reason for every inbox message.
`pending_actions.json` stores reply drafts waiting for approval.
`outbox/` stores approved draft files.
`trace.jsonl` stores decision, refusal, and approval events.
`memory.json` stores persistent preferences.
`capabilities.json` is the machine-readable capability manifest.

## Final Report

### 1.What did you refuse to automate? Name one message your system deliberately does not handle on its own, and explain why you drew the line there.
```
I refuse to automate emails involving money, credentials, legal matters, suspicious instructions, or impersonation. For example, m021 requests updated bank details, so the system flags it for human review instead of replying. This is dealt with in the safety.py file

I do automate low-risk, repetitive messages with rules: receipts, shipping notifications, newsletters, and no-reply emails are archived automatically. I drew the line there because organizing obvious noise is low-risk, while a wrong decision involving security, money, or reputation could cause real harm.
```

### 2. Where does untrusted text enter your system? Describe the boundary between text your system reads and instructions it follows, as a property of your architecture rather than a line in a prompt. Name what an attacker would have to defeat to make your system act on their behalf.
```
The untrusted text comes from the emails themselves—the sender, subject, and body. The system reads it as only email content, not as commands it has to follow. An email cannot directly approve itself, call a Python function, or write something to the outbox.

Before the model handles an email, the safety checks look for suspicious instructions and flag them. Drafts are also based only on the messages in that email thread. A potential way the attacker might cheat the system is to have the system build a bad draft. Even if a bad email somehow affected a draft, it would still need to get past the safety checks and the owner would have to approve it before anything goes into outbox/. So, from my understanding, the only way they could defeat the system would be if the owner somehow approves the bad draft.
```

### 3. Who is accountable when it sends the wrong thing? If a message sent in the owner’s name is badly worded, factually wrong, or sent to the wrong person, who is answerable, and how does your system help trace back the failure?
```
As mentioned in the previous answer, if anything wrong is sent, it would be the owners fault as this is basically a human in the loop style pattern (atleast the draft part). The owner would be accountable as we added the approval mechanism to make sure the draft produced is accurate. The system aslo provides details regarding the recepients for the owner to verify.

The failures can be tracked through the output channel (outbox/), trace.jsonl or even the 'pending_action.json' as the system doesn't delete any pending actions (which might need a reconsideration). 
```

### 4. Name your own machinery. Point to the parts of your code that play the roles of a framework’s Agents, Tasks, Crew and router. Name one thing a framework would have given you that you built yourself, and say whether using one here would have helped or hurt, and why.
```
I used plain Python for the agent pipeline and Flask only for the dashboard. classify_email() and make_reply_draft() act like agents because they use the LLM. process_inbox() is the router because it chooses the safety, rule, or LLM path. main.py acts like the crew by connecting all tasks together.

A framework could have provided built-in task orchestration and tool calling, but I built the routing, logging, memory, and approval gate myself. For this project, a framework would have added extra setup without helping much because the workflow is small and mostly linear.
```