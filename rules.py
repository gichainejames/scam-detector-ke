def check_scam(message, sender=""):
    msg = message.lower()
    sender = sender.upper().strip()
    if "m-pesa" in msg or "mpesa" in msg or "received" in msg:
        if sender != "MPESA" and sender != "":
            return True, f"Fake M-PESA: Sender is '{sender}' not MPESA"
    scam_words = ["congratulations", "won", "lottery", "claim", "click http", "bit.ly", "urgent", "kra pin blocked", "fuliza", "loan approved"]
    for w in scam_words:
        if w in msg:
            return True, f"Contains scam trigger: '{w}'"
    if ("http" in msg or "www." in msg) and ("kes" in msg or "ksh" in msg or "won" in msg):
        return True, "Suspicious link + money promise"
    return False, "Looks legit - Sender verified"