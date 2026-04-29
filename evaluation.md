--Evaluation Cases--

--Purpose--

This file contains the 5 required test cases used to evaluate the phishing detection agent.

The goal is to test whether the system correctly classifies emails as:

- Safe
- Suspicious
- Phishing

The system is considered successful if it correctly classifies at least 4 out of 5 test cases.

 - Test Case 1 – Clear Phishing Email

# Email

URGENT: Your account has been compromised.

Click here immediately to reset your password:

http://bit.ly/reset123

Failure to act now may result in account suspension.

# Expected Result

Phishing

# Actual Result

Phishing

# Status

PASS


- Test Case 2 – Legitimate Internal Email

# Email

Reminder: Team meeting tomorrow at 3 PM in Conference Room B.

Please bring your weekly progress updates.

# Expected Result

Safe

# Actual Result

Safe

# Status

PASS


- Test Case 3 – Suspicious Verification Request

# Email

Please verify your account information immediately to avoid service interruption.

# Expected Result

Suspicious

# Actual Result

Suspicious

# Status

PASS


- Test Case 4 – Fake Invoice Scam

# Email

Invoice attached for your recent purchase.

Please review here:

http://tinyurl.com/invoice-pay

# Expected Result

Phishing

# Actual Result

Phishing

# Status

PASS


-  Test Case 5 – Company Newsletter

# Email

Welcome to this week’s employee newsletter.

Here are updates from HR and upcoming office events.

# Expected Result

Safe

# Actual Result

Safe

# Status

PASS


## Success Criteria

The system is considered successful if:

- It correctly classifies at least 4 out of 5 test cases
- The agent logs each major decision step
- Claude API analysis supports the final classification
- The system demonstrates multi-step reasoning and autonomous decision-making


## Known Agent Limitations

- False positives on legitimate urgent emails
- Advanced phishing attacks may bypass simple keyword detection
- Claude may occasionally make incorrect analysis decisions
- Link checker only detects shortened URLs like bit.ly and tinyurl
