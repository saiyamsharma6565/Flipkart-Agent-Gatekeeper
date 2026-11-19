"""
Gatekeeper Engine for Flipkart AI Autonomous Shopping Policy Enforcement.
Evaluates agent permissions based on business rules R1 through R7.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import database

# Complete Specification of the Seven Business Rules
RULEBOOK = [
    {
        "rule_number": "R1",
        "name": "Unregistered Agent Gate",
        "condition": "Agent is unknown or not registered for customer",
        "action_scope": "Any Action",
        "threshold": "N/A",
        "decision": "BLOCK",
        "description": "Unknown or unregistered agent = BLOCK.",
        "rationale": "Prevents unauthorized third-party scripts or rogue AI entities from interacting with Flipkart customer profiles."
    },
    {
        "rule_number": "R2",
        "name": "Revoked Agent Gate",
        "condition": "Agent status is REVOKED",
        "action_scope": "Any Action",
        "threshold": "N/A",
        "decision": "BLOCK",
        "description": "Revoked agent = BLOCK.",
        "rationale": "Ensures customer revocation takes effect immediately across all sessions, preventing compromised agents from executing further commands."
    },
    {
        "rule_number": "R3",
        "name": "Autonomous Product Browsing",
        "condition": "Agent is registered & active; Action = Browse Products",
        "action_scope": "Browse Products",
        "threshold": "Zero monetary risk (₹0)",
        "decision": "ALLOW",
        "description": "Registered agent browsing products = ALLOW.",
        "rationale": "Product browsing and price comparison are low-risk, read-only actions essential for AI shopping assistants."
    },
    {
        "rule_number": "R4",
        "name": "Autonomous Cart Staging",
        "condition": "Agent is registered & active; Action = Add to Cart",
        "action_scope": "Add to Cart",
        "threshold": "Zero committed funds",
        "decision": "ALLOW",
        "description": "Registered agent adding products to cart = ALLOW.",
        "rationale": "Adding items to cart stages an intent without committing funds or debiting customer accounts."
    },
    {
        "rule_number": "R5",
        "name": "Autonomous Low-Value Purchase",
        "condition": "Agent is registered & active; Action = Purchase; Amount <= ₹5,000",
        "action_scope": "Purchase",
        "threshold": "<= ₹5,000.00",
        "decision": "ALLOW",
        "description": "Registered agent making a purchase of ₹5,000 or less = ALLOW.",
        "rationale": "Enables seamless frictionless autonomous shopping for routine, low-risk purchases under the safety threshold."
    },
    {
        "rule_number": "R6",
        "name": "High-Value Purchase Step-Up Verification",
        "condition": "Agent is registered & active; Action = Purchase; Amount > ₹5,000",
        "action_scope": "Purchase",
        "threshold": "> ₹5,000.00",
        "decision": "ASK CUSTOMER",
        "description": "Registered agent making a purchase above ₹5,000 = ASK CUSTOMER.",
        "rationale": "High-value transactions pose financial risk; requires explicit customer confirmation (OTP / biometric approval)."
    },
    {
        "rule_number": "R7",
        "name": "Cancellation & Refund Protection",
        "condition": "Agent is registered & active; Action = Cancel / Refund",
        "action_scope": "Cancel / Refund",
        "threshold": "Irreversible account/order action",
        "decision": "ASK CUSTOMER",
        "description": "Registered agent requesting cancellation or refund = ASK CUSTOMER.",
        "rationale": "Cancellations and refund requests can forfeit promotional discounts or disrupt deliveries; customer confirmation is mandatory."
    }
]

# Action categories
ACTION_BROWSE = "Browse Products"
ACTION_ADD_TO_CART = "Add to Cart"
ACTION_PURCHASE = "Purchase"
ACTION_CANCEL_REFUND = "Cancel / Refund"

SUPPORTED_ACTIONS = [
    ACTION_BROWSE,
    ACTION_ADD_TO_CART,
    ACTION_PURCHASE,
    ACTION_CANCEL_REFUND
]


def evaluate_permission(
    customer_name: str,
    agent_name: str,
    action: str,
    amount: float = 0.0,
    log_to_audit: bool = True
) -> Dict[str, Any]:
    """
    Evaluates whether the requested action is permitted for the given agent and customer.
    
    Returns a dictionary with:
      - decision: 'ALLOW' | 'ASK CUSTOMER' | 'BLOCK'
      - rule_number: 'R1' .. 'R7'
      - reason: Detailed explanatory string
      - timestamp: Evaluation timestamp string
      - customer_name: Normalized customer name
      - agent_name: Normalized agent name
      - action: Normalized action name
      - amount: Normalized float amount
      - agent_status: 'ACTIVE' | 'REVOKED' | 'UNREGISTERED'
      - log_id: Audit log ID if recorded
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    customer_name = customer_name.strip()
    agent_name = agent_name.strip()
    amount = float(amount) if amount is not None else 0.0

    # Retrieve agent record from local database
    agent_record = database.get_agent(agent_name, customer_name)

    # ---------------- Rule 1: Unknown or unregistered agent = BLOCK ----------------
    if not agent_record:
        decision = "BLOCK"
        rule_number = "R1"
        reason = (
            f"Agent '{agent_name}' is not registered for customer '{customer_name}'. "
            "Gatekeeper prohibits transactions from unknown or unverified AI agents."
        )
        agent_status = "UNREGISTERED"

    # ---------------- Rule 2: Revoked agent = BLOCK ----------------
    elif agent_record["status"] == "REVOKED":
        decision = "BLOCK"
        rule_number = "R2"
        revocation_time = agent_record.get("revoked_at") or "an earlier timestamp"
        reason = (
            f"Agent '{agent_name}' was REVOKED on {revocation_time}. "
            "All operations by revoked agents are immediately blocked."
        )
        agent_status = "REVOKED"

    # Agent is registered and ACTIVE
    else:
        agent_status = "ACTIVE"

        # ---------------- Rule 3: Registered agent browsing products = ALLOW ----------------
        if action == ACTION_BROWSE:
            decision = "ALLOW"
            rule_number = "R3"
            reason = (
                f"Agent '{agent_name}' is registered and active. "
                "Autonomous product browsing has zero monetary liability and is permitted."
            )

        # ---------------- Rule 4: Registered agent adding products to cart = ALLOW ----------------
        elif action == ACTION_ADD_TO_CART:
            decision = "ALLOW"
            rule_number = "R4"
            reason = (
                f"Agent '{agent_name}' is registered and active. "
                "Adding products to cart stages items without committing funds and is permitted."
            )

        # ---------------- Rules 5 & 6: Purchase actions ----------------
        elif action == ACTION_PURCHASE:
            # Rule 5: Purchase <= ₹5,000 = ALLOW
            if amount <= 5000.0:
                decision = "ALLOW"
                rule_number = "R5"
                reason = (
                    f"Agent '{agent_name}' is registered and active. "
                    f"Purchase amount of ₹{amount:,.2f} is within the autonomous micro-transaction limit (<= ₹5,000.00)."
                )
            # Rule 6: Purchase > ₹5,000 = ASK CUSTOMER
            else:
                decision = "ASK CUSTOMER"
                rule_number = "R6"
                reason = (
                    f"Agent '{agent_name}' is registered and active. "
                    f"Purchase amount of ₹{amount:,.2f} exceeds the autonomous limit of ₹5,000.00. "
                    "Explicit customer step-up verification (OTP/Biometric) is required."
                )

        # ---------------- Rule 7: Cancellation or refund = ASK CUSTOMER ----------------
        elif action == ACTION_CANCEL_REFUND:
            decision = "ASK CUSTOMER"
            rule_number = "R7"
            reason = (
                f"Agent '{agent_name}' requested order cancellation or refund. "
                "This action is irreversible and requires explicit customer approval."
            )

        # Fallback for unrecognized action
        else:
            decision = "BLOCK"
            rule_number = "R1"
            reason = f"Unrecognized action '{action}' requested. Gatekeeper blocked the operation by default."

    # Save to Audit Log
    log_id = None
    if log_to_audit:
        log_id = database.log_request(
            customer_name=customer_name,
            agent_name=agent_name,
            action=action,
            amount=amount,
            decision=decision,
            rule_number=rule_number,
            reason=reason,
            timestamp=timestamp
        )

    return {
        "decision": decision,
        "rule_number": rule_number,
        "reason": reason,
        "timestamp": timestamp,
        "customer_name": customer_name,
        "agent_name": agent_name,
        "action": action,
        "amount": amount,
        "agent_status": agent_status,
        "log_id": log_id
    }
