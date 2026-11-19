"""
Initial database seeder for Flipkart AI Agent Gatekeeper Prototype.
Pre-populates demonstration agents and initial audit records.
"""

from datetime import datetime, timedelta
import database
import gatekeeper

def seed_demo_data(force: bool = False):
    """Seed sample agents and audit logs if tables are empty or force=True."""
    database.init_db()
    
    existing_agents = database.list_agents()
    if existing_agents and not force:
        return {"seeded": False, "message": "Database already contains agents. Skipping seed."}

    if force:
        database.reset_database()

    # 1. Register sample agents
    # Active agent 1
    database.register_agent(
        agent_name="Flipkart_Shopper_Bot",
        customer_name="Rahul Sharma",
        description="Autonomous shopping assistant for electronics and household essentials."
    )
    
    # Active agent 2
    database.register_agent(
        agent_name="Grocery_Assistant_Agent",
        customer_name="Priya Patel",
        description="Daily grocery restock agent for Flipkart Minutes / Supermart."
    )

    # Revoked agent (First registered, then revoked with exact timestamp)
    database.register_agent(
        agent_name="Rogue_AutoBuyer_Bot",
        customer_name="Rahul Sharma",
        description="Decommissioned aggressive bidding bot."
    )
    # Find its ID and revoke it
    revoked_agent = database.get_agent("Rogue_AutoBuyer_Bot", "Rahul Sharma")
    if revoked_agent:
        database.revoke_agent(revoked_agent["id"])

    # 2. Add some initial audit log entries representing past activity
    t_now = datetime.now()
    sample_logs = [
        ("Rahul Sharma", "Flipkart_Shopper_Bot", "Browse Products", 0.0, "ALLOW", "R3",
         "Agent 'Flipkart_Shopper_Bot' is registered and active. Autonomous product browsing has zero monetary liability and is permitted.",
         (t_now - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")),

        ("Rahul Sharma", "Flipkart_Shopper_Bot", "Add to Cart", 1499.0, "ALLOW", "R4",
         "Agent 'Flipkart_Shopper_Bot' is registered and active. Adding products to cart stages items without committing funds and is permitted.",
         (t_now - timedelta(hours=2, minutes=30)).strftime("%Y-%m-%d %H:%M:%S")),

        ("Rahul Sharma", "Flipkart_Shopper_Bot", "Purchase", 1499.0, "ALLOW", "R5",
         "Agent 'Flipkart_Shopper_Bot' is registered and active. Purchase amount of ₹1,499.00 is within the autonomous micro-transaction limit (<= ₹5,000.00).",
         (t_now - timedelta(hours=2, minutes=15)).strftime("%Y-%m-%d %H:%M:%S")),

        ("Rahul Sharma", "Rogue_AutoBuyer_Bot", "Purchase", 25000.0, "BLOCK", "R2",
         "Agent 'Rogue_AutoBuyer_Bot' was REVOKED. All operations by revoked agents are immediately blocked.",
         (t_now - timedelta(hours=1, minutes=45)).strftime("%Y-%m-%d %H:%M:%S")),

        ("Rahul Sharma", "Flipkart_Shopper_Bot", "Purchase", 45000.0, "ASK CUSTOMER", "R6",
         "Agent 'Flipkart_Shopper_Bot' is registered and active. Purchase amount of ₹45,000.00 exceeds the autonomous limit of ₹5,000.00. Explicit customer step-up verification (OTP/Biometric) is required.",
         (t_now - timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S")),

        ("Amit Kumar", "Unauthorized_Scraper", "Browse Products", 0.0, "BLOCK", "R1",
         "Agent 'Unauthorized_Scraper' is not registered for customer 'Amit Kumar'. Gatekeeper prohibits transactions from unknown or unverified AI agents.",
         (t_now - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")),
    ]

    for cust, agent, act, amt, dec, rule, rsn, ts in sample_logs:
        database.log_request(cust, agent, act, amt, dec, rule, rsn, timestamp=ts)

    return {"seeded": True, "message": "Demo data successfully seeded."}

if __name__ == "__main__":
    result = seed_demo_data(force=True)
    print(result)
