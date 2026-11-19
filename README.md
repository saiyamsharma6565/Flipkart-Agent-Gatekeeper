# Flipkart AI Agent Gatekeeper Prototype

**Academic Demonstration Project**  
**Student Enrolment Number:** `PGD202570278`

---

## 📌 Executive Summary

The **Flipkart AI Agent Gatekeeper** is a governance and security prototype built in Python and Streamlit to monitor and control autonomous AI agents acting on behalf of customers.

As autonomous AI agents participate in e-commerce workflows (browsing products, staging shopping carts, checking out, and requesting refunds), the Gatekeeper acts as an authoritative boundary protecting customer accounts and financial boundaries. Every agent request is evaluated deterministically against seven business rules (**R1 – R7**), producing an instantaneous decision:
- `ALLOW` (Green)
- `ASK CUSTOMER` (Amber / Step-Up Verification)
- `BLOCK` (Red / Enforced Denial)

All registered agents, revocation events (with exact timestamps), and request logs are stored locally in a persistent SQLite database (`gatekeeper.db`), ensuring data remains intact across application restarts.

---

## 🚀 How to Run the Application

### 1. Prerequisites
- Python 3.9+ installed
- Packages: `streamlit` and `pandas`

Install requirements:
```powershell
pip install -r requirements.txt
```

### 2. Launch the Streamlit Web Application
Run the following command from the project root directory:
```powershell
streamlit run app.py
```
Streamlit will automatically open the web dashboard in your browser (default: `http://localhost:8501`).

### 3. Run Command-Line Demo (Zero Browser Required)
You can also run the full test suite directly from PowerShell or terminal:
```powershell
python run_demo_cli.py
```

### 4. Run Automated Unit Tests
To verify all rules, boundaries, and database operations:
```powershell
python test_gatekeeper.py
```

---

## 🛡️ Business Rules Reference (R1 – R7)

| Rule | Name | Condition | Action Scope | Threshold | Gatekeeper Decision | Flipkart Rationale |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **R1** | Unregistered Agent Gate | Unknown / Unregistered agent | Any Action | N/A | **`BLOCK`** | Prohibits unknown bots or malicious scripts from acting on customer accounts. |
| **R2** | Revoked Agent Gate | Agent status is `REVOKED` | Any Action | N/A | **`BLOCK`** | Enforces immediate revocation across all sessions for compromised or deactivated bots. |
| **R3** | Autonomous Browsing | Active Registered Agent | Browse Products | ₹0 (Zero Risk) | **`ALLOW`** | Read-only product discovery and price comparison are low-risk autonomous operations. |
| **R4** | Cart Staging | Active Registered Agent | Add to Cart | Zero funds committed | **`ALLOW`** | Adding items stages purchase intent without deducting bank or wallet balances. |
| **R5** | Low-Value Autonomous Purchase | Active Registered Agent | Purchase | $\le$ ₹5,000.00 | **`ALLOW`** | Frictionless autonomous shopping for routine purchases within the pre-approved budget. |
| **R6** | High-Value Purchase Step-Up | Active Registered Agent | Purchase | $>$ ₹5,000.00 | **`ASK CUSTOMER`** | Mitigates financial liability; demands explicit customer confirmation (OTP/Biometric). |
| **R7** | Cancellation & Refund Protection | Active Registered Agent | Cancel / Refund | Account Action | **`ASK CUSTOMER`** | Prevents irreversible loss of promotional discounts or unintended order cancellations. |

---

## 🧪 7 Pre-Configured Test Scenarios

The prototype includes interactive 1-click test scenarios in the UI (`tab 2`) and CLI:

| # | Scenario Title | Customer Name | Agent Name | Action | Amount (₹) | Expected Rule | Expected Decision |
| :-: | :--- | :--- | :--- | :--- | :---: | :-: | :-: |
| **1** | Unknown / Unregistered Agent | Rahul Sharma | Shadow_Bot_Unknown | Browse Products | ₹0.00 | **R1** | `BLOCK` |
| **2** | Revoked Agent Attempting Action | Rahul Sharma | Rogue_AutoBuyer_Bot | Add to Cart | ₹1,299.00 | **R2** | `BLOCK` |
| **3** | Active Agent Browsing Products | Rahul Sharma | Flipkart_Shopper_Bot | Browse Products | ₹0.00 | **R3** | `ALLOW` |
| **4** | Active Agent Adding to Cart | Rahul Sharma | Flipkart_Shopper_Bot | Add to Cart | ₹2,499.00 | **R4** | `ALLOW` |
| **5** | Low-Value Purchase ($\le$ ₹5,000) | Rahul Sharma | Flipkart_Shopper_Bot | Purchase | ₹3,499.00 | **R5** | `ALLOW` |
| **6** | High-Value Purchase ($>$ ₹5,000) | Rahul Sharma | Flipkart_Shopper_Bot | Purchase | ₹18,999.00 | **R6** | `ASK CUSTOMER` |
| **7** | Cancellation / Refund Request | Rahul Sharma | Flipkart_Shopper_Bot | Cancel / Refund | ₹3,499.00 | **R7** | `ASK CUSTOMER` |

---

## 📂 Project Architecture & File Structure

```
Flipkart_Agent_Gatekeeper/
├── app.py                 # Streamlit web dashboard with tabs, styling, and charts
├── gatekeeper.py          # Deterministic rule evaluation engine (Rules R1 - R7)
├── database.py            # SQLite database manager (agents, revocation, audit trail)
├── sample_scenarios.py    # Specification of all 7 test scenarios
├── seed_data.py           # Pre-populates sample active & revoked agents and past logs
├── test_gatekeeper.py     # Comprehensive automated unit test suite
├── run_demo_cli.py        # Standalone terminal demonstration script
├── gatekeeper.db          # Persistent SQLite local database
├── requirements.txt       # Python dependencies (streamlit, pandas)
└── README.md              # Project documentation and user guide
```

### Database Schema (Local Persistence)
1. **`agents`**:
   - `id`: Integer Primary Key
   - `agent_name`: Text (e.g., `Flipkart_Shopper_Bot`)
   - `customer_name`: Text (e.g., `Rahul Sharma`)
   - `status`: Text (`ACTIVE` or `REVOKED`)
   - `registered_at`: Text Timestamp (`YYYY-MM-DD HH:MM:SS`)
   - `revoked_at`: Text Timestamp (`YYYY-MM-DD HH:MM:SS`, or `NULL`)
   - `description`: Text

2. **`audit_logs`**:
   - `id`: Integer Primary Key
   - `timestamp`: Text Timestamp (`YYYY-MM-DD HH:MM:SS`)
   - `customer_name`: Text
   - `agent_name`: Text
   - `action`: Text (`Browse Products`, `Add to Cart`, `Purchase`, `Cancel / Refund`)
   - `amount`: Real (Transaction amount in ₹)
   - `decision`: Text (`ALLOW`, `ASK CUSTOMER`, `BLOCK`)
   - `rule_number`: Text (`R1` to `R7`)
   - `reason`: Text (Detailed explanatory text)

---

## 🎓 Academic Demonstration Disclaimer
This project is an academic simulation developed for demonstration under student enrolment number **PGD202570278**. It is strictly a security and policy enforcement prototype and does not connect to real Flipkart accounts, bank payment gateways, or live order management systems.
