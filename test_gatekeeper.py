"""
Unit tests for Flipkart AI Agent Gatekeeper Prototype.
Tests all rules R1 through R7, registration, revocation, and audit logging.
"""

import unittest
import database
import gatekeeper
from sample_scenarios import TEST_SCENARIOS

class TestFlipkartGatekeeper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import seed_data
        seed_data.seed_demo_data(force=True)
        # Register test active agent
        database.register_agent("Test_Active_Agent", "Test Customer", "Standard test active bot")
        # Register test revoked agent
        database.register_agent("Test_Revoked_Agent", "Test Customer", "Revoked test bot")
        revoked_rec = database.get_agent("Test_Revoked_Agent", "Test Customer")
        database.revoke_agent(revoked_rec["id"])

    def test_r1_unregistered_agent(self):
        """R1: Unknown or unregistered agent = BLOCK."""
        result = gatekeeper.evaluate_permission("Test Customer", "Non_Existent_Agent", "Browse Products", 0.0)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["rule_number"], "R1")
        self.assertIn("not registered", result["reason"])

    def test_r2_revoked_agent(self):
        """R2: Revoked agent = BLOCK."""
        result = gatekeeper.evaluate_permission("Test Customer", "Test_Revoked_Agent", "Browse Products", 0.0)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["rule_number"], "R2")
        self.assertIn("REVOKED", result["reason"])

    def test_r3_browsing_products(self):
        """R3: Registered agent browsing products = ALLOW."""
        result = gatekeeper.evaluate_permission("Test Customer", "Test_Active_Agent", "Browse Products", 0.0)
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["rule_number"], "R3")

    def test_r4_adding_to_cart(self):
        """R4: Registered agent adding products to cart = ALLOW."""
        result = gatekeeper.evaluate_permission("Test Customer", "Test_Active_Agent", "Add to Cart", 1200.0)
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["rule_number"], "R4")

    def test_r5_purchase_under_or_equal_5000(self):
        """R5: Registered agent making a purchase of ₹5,000 or less = ALLOW."""
        # Boundary: exactly 5000
        result_edge = gatekeeper.evaluate_permission("Test Customer", "Test_Active_Agent", "Purchase", 5000.0)
        self.assertEqual(result_edge["decision"], "ALLOW")
        self.assertEqual(result_edge["rule_number"], "R5")

        # Typical low-value: 2999
        result_low = gatekeeper.evaluate_permission("Test Customer", "Test_Active_Agent", "Purchase", 2999.0)
        self.assertEqual(result_low["decision"], "ALLOW")
        self.assertEqual(result_low["rule_number"], "R5")

    def test_r6_purchase_above_5000(self):
        """R6: Registered agent making a purchase above ₹5,000 = ASK CUSTOMER."""
        # Boundary: 5000.01
        result_edge = gatekeeper.evaluate_permission("Test Customer", "Test_Active_Agent", "Purchase", 5000.01)
        self.assertEqual(result_edge["decision"], "ASK CUSTOMER")
        self.assertEqual(result_edge["rule_number"], "R6")

        # Typical high-value: 25000
        result_high = gatekeeper.evaluate_permission("Test Customer", "Test_Active_Agent", "Purchase", 25000.0)
        self.assertEqual(result_high["decision"], "ASK CUSTOMER")
        self.assertEqual(result_high["rule_number"], "R6")

    def test_r7_cancellation_refund(self):
        """R7: Registered agent requesting cancellation or refund = ASK CUSTOMER."""
        result = gatekeeper.evaluate_permission("Test Customer", "Test_Active_Agent", "Cancel / Refund", 2500.0)
        self.assertEqual(result["decision"], "ASK CUSTOMER")
        self.assertEqual(result["rule_number"], "R7")

    def test_preset_scenarios(self):
        """Test all 7 preset test scenarios."""
        for scenario in TEST_SCENARIOS:
            res = gatekeeper.evaluate_permission(
                customer_name=scenario["customer_name"],
                agent_name=scenario["agent_name"],
                action=scenario["action"],
                amount=scenario["amount"],
                log_to_audit=False
            )
            self.assertEqual(res["decision"], scenario["expected_decision"], f"Failed on {scenario['id']}")
            self.assertEqual(res["rule_number"], scenario["rule"], f"Failed on {scenario['id']}")

    def test_revocation_records_timestamp(self):
        """Verify agent revocation accurately records timestamp."""
        database.register_agent("Temp_Bot", "Customer X")
        agent = database.get_agent("Temp_Bot", "Customer X")
        self.assertEqual(agent["status"], "ACTIVE")
        self.assertIsNone(agent["revoked_at"])

        res = database.revoke_agent(agent["id"])
        self.assertTrue(res["success"])
        self.assertIn("revoked_at", res)

        updated_agent = database.get_agent("Temp_Bot", "Customer X")
        self.assertEqual(updated_agent["status"], "REVOKED")
        self.assertIsNotNone(updated_agent["revoked_at"])

if __name__ == "__main__":
    unittest.main()
