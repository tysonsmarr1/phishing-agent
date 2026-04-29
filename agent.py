import re
from datetime import datetime
import anthropic
from dotenv import load_dotenv

load_dotenv()


client = anthropic.Anthropic()

# Link Checker
def check_links(email_text):
    urls = re.findall(r'https?://\S+', email_text)

    results = []

    for url in urls:
        if "bit.ly" in url or "tinyurl" in url:
            results.append((url, "suspicious"))
        else:
            results.append((url, "unknown"))

    return results

#Claude Email Analyzer
def analyze_email_claude(email_text):
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"""
You are a cybersecurity assistant.

Analyze this email for phishing indicators.
Explain if it appears safe, suspicious, or if it appears to be phishing.


Email:
{email_text}
"""
            }
        ]
    )

    return message.content[0].text

# AGENT LOOP
def phishing_agent(email_text):
    log = []

    log.append(f"[{datetime.now()}] Email received")

    # Step 1: Claude analysis
    llm_analysis = analyze_email_claude(email_text)
    log.append(f"Claude Analysis: {llm_analysis}")

    # Step 2: Link checking
    link_results = check_links(email_text)
    log.append(f"Link Analysis: {link_results}")

    # Step 3: Decision Logic
    if "urgent" in email_text.lower() or any(
        result[1] == "suspicious" for result in link_results
    ):
        decision = "Phishing"

    elif "verify your account" in email_text.lower():
        decision = "Suspicious"

    else:
        decision = "Safe"

    log.append(f"Final Decision: {decision}")

    return {
        "decision": decision,
        "analysis": llm_analysis,
        "links": link_results,
        "log": log
    }

# TEST RUN
if __name__ == "__main__":
    test_emails = [
        {
            "name": "Phishing Example",
            "content": """
URGENT: Your account has been compromised.

Click here immediately:
http://bit.ly/reset123
"""
        },

        {
            "name": "Safe Example",
            "content": """
Reminder: Team meeting tomorrow at 3 PM.

Please bring your weekly updates.
"""
        },

        {
            "name": "Suspicious Example",
            "content": """
Please verify your account immediately
to avoid service interruption.
"""
        }
    ]

    for email in test_emails:
        print("\n==============================")
        print("TEST CASE:", email["name"])
        print("==============================")

        result = phishing_agent(email["content"])

        for line in result["log"]:
            print(line)

        print("\nFINAL DECISION:", result["decision"])