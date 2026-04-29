# Milestone 4 - 
# Phishing Detection Agent

Authors: Dylan Stafford, and Tyson Smarr

## What the system does: 
    - This is a phishing detection agent that analyzes emails and decides if they are safe, suspicous, or phishing. The system uses Claude API to analyze the email content and a Python link checker to find suspicious links like bit.ly or tinyurl. Then, it makes a final decision and logs each step of the process. This shows agentic behavior because the system follows a goal-directed loop, uses tools, and makes decisions automatically.

## How to run: 
    In the terminal, run - "python agent.py" (no quotes.)

## Files Included: 
    - agent.py
    - README.md
    - evaluation.md
    - requirements.txt
    - .gitignore

## Limitations: 
    -Simple rule based final decisions
    -Limited link checking
    -No real email integration yet
    -Claude may occasionally make mistakes

## Taken to a professional level:
    -Add Gmail API integration
    -Automatic incoming Email scans.
    -Detect phishing in real time
    -Warn users
    -Send for human review.

