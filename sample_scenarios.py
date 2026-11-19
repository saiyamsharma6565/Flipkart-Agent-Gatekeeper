"""
Preset Test Scenarios for all Seven Rules (R1 - R7).
These can be executed directly from the Streamlit UI or CLI for rapid grading and demonstration.
"""

TEST_SCENARIOS = [
    {
        "id": "R1",
        "title": "Scenario 1: Unknown / Unregistered Agent",
        "rule": "R1",
        "expected_decision": "BLOCK",
        "customer_name": "Rahul Sharma",
        "agent_name": "Shadow_Bot_Unknown",
        "action": "Browse Products",
        "amount": 0.0,
        "explanation": "Agent 'Shadow_Bot_Unknown' has never been registered by Rahul Sharma in the Gatekeeper system. The request must be immediately BLOCKED."
    },
    {
        "id": "R2",
        "title": "Scenario 2: Revoked Agent Attempting Cart Addition",
        "rule": "R2",
        "expected_decision": "BLOCK",
        "customer_name": "Rahul Sharma",
        "agent_name": "Rogue_AutoBuyer_Bot",
        "action": "Add to Cart",
        "amount": 1299.0,
        "explanation": "Agent 'Rogue_AutoBuyer_Bot' was previously registered but subsequently REVOKED with an exact timestamp. The Gatekeeper must immediately BLOCK any action from it."
    },
    {
        "id": "R3",
        "title": "Scenario 3: Registered Active Agent Browsing Products",
        "rule": "R3",
        "expected_decision": "ALLOW",
        "customer_name": "Rahul Sharma",
        "agent_name": "Flipkart_Shopper_Bot",
        "action": "Browse Products",
        "amount": 0.0,
        "explanation": "An active registered agent browsing products or comparing specifications creates zero monetary risk. The Gatekeeper permits this autonomously (ALLOW)."
    },
    {
        "id": "R4",
        "title": "Scenario 4: Registered Active Agent Adding Items to Cart",
        "rule": "R4",
        "expected_decision": "ALLOW",
        "customer_name": "Rahul Sharma",
        "agent_name": "Flipkart_Shopper_Bot",
        "action": "Add to Cart",
        "amount": 2499.0,
        "explanation": "Adding an item to the shopping cart stages purchase intent without deducting bank or wallet funds. The Gatekeeper permits this autonomously (ALLOW)."
    },
    {
        "id": "R5",
        "title": "Scenario 5: Low-Value Autonomous Purchase (<= ₹5,000)",
        "rule": "R5",
        "expected_decision": "ALLOW",
        "customer_name": "Rahul Sharma",
        "agent_name": "Flipkart_Shopper_Bot",
        "action": "Purchase",
        "amount": 3499.0,
        "explanation": "The purchase of ₹3,499 is within the ₹5,000 autonomous micro-transaction ceiling. The Gatekeeper approves the transaction directly (ALLOW)."
    },
    {
        "id": "R6",
        "title": "Scenario 6: High-Value Purchase (> ₹5,000)",
        "rule": "R6",
        "expected_decision": "ASK CUSTOMER",
        "customer_name": "Rahul Sharma",
        "agent_name": "Flipkart_Shopper_Bot",
        "action": "Purchase",
        "amount": 18999.0,
        "explanation": "The transaction amount of ₹18,999 exceeds the ₹5,000 autonomous threshold. The Gatekeeper pauses the transaction and demands customer 2FA/approval (ASK CUSTOMER)."
    },
    {
        "id": "R7",
        "title": "Scenario 7: Cancellation or Refund Request",
        "rule": "R7",
        "expected_decision": "ASK CUSTOMER",
        "customer_name": "Rahul Sharma",
        "agent_name": "Flipkart_Shopper_Bot",
        "action": "Cancel / Refund",
        "amount": 3499.0,
        "explanation": "Order cancellation or refund cannot be performed autonomously by an agent to prevent accidental or fraudulent order loss. Requires customer verification (ASK CUSTOMER)."
    }
]
