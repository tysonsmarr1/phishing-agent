import re
import json
from datetime import datetime
import anthropic
from dotenv import load_dotenv
 
load_dotenv()
 
client = anthropic.Anthropic()

# Link Checker Tool
def check_links(email_text: str) -> dict:
    """
    Scans email text for URLs and flags suspicious ones.
    Returns a dict so it can be serialised as a tool result.
    """
    urls = re.findall(r'https?://\S+', email_text)
    results = []
    for url in urls:
        if any(shortener in url for shortener in ["bit.ly", "tinyurl", "t.co", "goo.gl"]):
            results.append({"url": url, "status": "suspicious"})
        elif re.search(r'\d{1,3}(\.\d{1,3}){3}', url):          # raw IP address
            results.append({"url": url, "status": "suspicious"})
        else:
            results.append({"url": url, "status": "unknown"})
 
    suspicious_count = sum(1 for r in results if r["status"] == "suspicious")
    return {
        "urls_found": len(results),
        "suspicious_count": suspicious_count,
        "details": results
    }

#Tool
TOOLS = [
    {
        "name": "check_links",
        "description": (
            "Scans an email for URLs and flags any that use known URL-shortening "
            "services (bit.ly, tinyurl, etc.) or raw IP addresses, which are common "
            "phishing indicators. Returns a count of suspicious links and their details."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "email_text": {
                    "type": "string",
                    "description": "The full text of the email to scan for links."
                }
            },
            "required": ["email_text"]
        }
    }
]
 
#Tool Call
def run_tool(tool_name: str, tool_input: dict) -> str:
    """Execute the requested tool and return its result as a JSON string."""
    if tool_name == "check_links":
        result = check_links(tool_input["email_text"])
        return json.dumps(result)
    return json.dumps({"error": f"Unknown tool: {tool_name}"})

# AGENT LOOP
def phishing_agent(email_text: str) -> dict:
    """
    Agentic loop:
      1. Send email + tools to Claude.
      2. If Claude calls a tool, execute it and feed the result back.
      3. Repeat until Claude returns a final text response.
      4. Parse a classification out of that response.
    """
    log = []
    log.append(f"[{datetime.now()}] Email received for analysis.")
 
    system_prompt = (
        "You are a cybersecurity assistant specialising in phishing detection. "
        "When given an email, you MUST call the check_links tool to inspect any URLs "
        "before forming your conclusion. "
        "After reviewing the tool results, classify the email as exactly one of: "
        "Safe, Suspicious, or Phishing. "
        "Explain your reasoning clearly, referencing the link-check results."
    )
 
    messages = [{"role": "user", "content": email_text}]
 
    # Agentic loop – continues until Claude stops calling tools
def phishing_agent(email_text: str) -> dict:
    """
    Agentic loop:
      1. Send email + tools to Claude.
      2. If Claude calls a tool, execute it and feed the result back.
      3. Repeat until Claude returns a final text response.
      4. Parse a classification out of that response.
    """
    log = []
    log.append(f"[{datetime.now()}] Email received for analysis.")
 
    system_prompt = (
        "You are a cybersecurity assistant specialising in phishing detection. "
        "When given an email, you MUST call the check_links tool to inspect any URLs "
        "before forming your conclusion. "
        "After reviewing the tool results, classify the email as exactly one of: "
        "Safe, Suspicious, or Phishing. "
        "Explain your reasoning clearly, referencing the link-check results."
    )
 
    messages = [{"role": "user", "content": email_text}]
 
    # Agentic loop – continues until Claude stops calling tools
    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            temperature=0,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )
 
        log.append(f"[{datetime.now()}] Claude stop_reason: {response.stop_reason}")
 
        # Collect any text blocks for the final answer
        text_blocks = [b.text for b in response.content if b.type == "text"]
 
        #Handle tool calls
        if response.stop_reason == "tool_use":
            # Append Claude's response (which contains the tool_use block)
            messages.append({"role": "assistant", "content": response.content})
 
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    log.append(f"[{datetime.now()}] Claude called tool: {block.name} | input: {block.input}")
                    result_str = run_tool(block.name, block.input)
                    log.append(f"[{datetime.now()}] Tool result: {result_str}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_str
                    })
 
            # Feed all tool results back in a single user turn
            messages.append({"role": "user", "content": tool_results})
            continue  # Let Claude continue reasoning
 
        #Final response
        final_text = "\n".join(text_blocks).strip()
        log.append(f"[{datetime.now()}] Claude final analysis:\n{final_text}")
 
        #classification from Claude's response
        lower = final_text.lower()
        if "phishing" in lower:
            decision = "Phishing"
        elif "suspicious" in lower:
            decision = "Suspicious"
        else:
            decision = "Safe"
 
        log.append(f"[{datetime.now()}] Final Decision: {decision}")
 
        return {
            "decision": decision,
            "analysis": final_text,
            "log": log
        }

# TEST RUN
if __name__ == "__main__":
    test_emails = [
        {
            "name": "Phishing Example",
            "content": (
                "URGENT: Your account has been compromised.\n\n"
                "Click here immediately:\n"
                "http://bit.ly/reset123"
            )
        },
        {
            "name": "Safe Example",
            "content": (
                "Reminder: Team meeting tomorrow at 3 PM.\n\n"
                "Please bring your weekly updates."
            )
        },
        {
            "name": "Suspicious Example",
            "content": (
                "Please verify your account immediately\n"
                "to avoid service interruption."
            )
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