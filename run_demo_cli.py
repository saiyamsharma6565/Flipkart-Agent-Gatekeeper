"""
Command-Line Demonstration of Flipkart AI Agent Gatekeeper Prototype.
Enrolment Number: PGD202570278
Tests and demonstrates all 7 rules (R1 to R7) in terminal.
"""

import database
import gatekeeper
from sample_scenarios import TEST_SCENARIOS
import seed_data

def main():
    print("=" * 80)
    print("  FLIPKART AI AGENT GATEKEEPER PROTOTYPE - CLI DEMO")
    print("  Student Enrolment Number: PGD202570278")
    print("  Academic Prototype Demonstration")
    print("=" * 80)

    # Initialize and re-seed
    seed_data.seed_demo_data(force=True)
    print("\n[OK] Local SQLite Database Initialized & Demo Data Loaded (`gatekeeper.db`).")

    print("\n" + "-" * 80)
    print("  EVALUATING ALL 7 BUSINESS RULES (R1 - R7)")
    print("-" * 80)

    passed_count = 0
    for scen in TEST_SCENARIOS:
        rule_id = scen["rule"]
        print(f"\n[Test Case {rule_id}] {scen['title']}")
        print(f"  * Customer: {scen['customer_name']}")
        print(f"  * Agent: {scen['agent_name']}")
        print(f"  * Action: {scen['action']}")
        print(f"  * Amount: Rs. {scen['amount']:,.2f}")
        print(f"  * Expected Decision: {scen['expected_decision']} ({rule_id})")

        result = gatekeeper.evaluate_permission(
            customer_name=scen["customer_name"],
            agent_name=scen["agent_name"],
            action=scen["action"],
            amount=scen["amount"],
            log_to_audit=True
        )

        match = (result["decision"] == scen["expected_decision"]) and (result["rule_number"] == scen["rule"])
        status = "PASSED [OK]" if match else "FAILED [X]"
        if match:
            passed_count += 1

        print(f"  -> Actual Decision: {result['decision']}")
        print(f"  -> Rule Number: {result['rule_number']}")
        print(f"  -> Gatekeeper Reason: {result['reason']}")
        print(f"  -> Audit Log ID: #{result['log_id']}")
        print(f"  -> Outcome Status: {status}")

    print("\n" + "=" * 80)
    print(f"  SUMMARY: {passed_count}/{len(TEST_SCENARIOS)} Rules Passed Successfully.")
    print("=" * 80)

if __name__ == "__main__":
    main()
