"""
Flipkart AI Agent Gatekeeper Prototype
Main Streamlit Application
Enrolment Number: PGD202570278
"""

import streamlit as st
import pandas as pd
from datetime import datetime

import database
import gatekeeper
from sample_scenarios import TEST_SCENARIOS
import seed_data

# ----------------- Page Configuration -----------------
st.set_page_config(
    page_title="Flipkart AI Agent Gatekeeper",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Database Initialization -----------------
database.init_db()
# Ensure demo data is available if first run
seed_data.seed_demo_data(force=False)

# ----------------- Custom Styling -----------------
st.markdown("""
<style>
    /* Main Flipkart Branding Colors */
    :root {
        --fk-blue: #2874F0;
        --fk-yellow: #FFE11B;
        --fk-dark: #1e293b;
    }
    
    .main-header {
        background: linear-gradient(135deg, #2874F0 0%, #1a56b7 100%);
        padding: 24px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(40, 116, 240, 0.25);
    }
    
    .enrolment-pill {
        display: inline-block;
        background-color: #FFE11B;
        color: #111827;
        font-weight: 800;
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 15px;
        letter-spacing: 0.5px;
        border: 2px solid #ffffff;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    
    .academic-pill {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin-left: 10px;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }

    .decision-card-allow {
        background: #ecfdf5;
        border-left: 8px solid #059669;
        border-radius: 10px;
        padding: 22px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.12);
    }
    
    .decision-card-ask {
        background: #fffbeb;
        border-left: 8px solid #d97706;
        border-radius: 10px;
        padding: 22px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(217, 119, 6, 0.12);
    }
    
    .decision-card-block {
        background: #fef2f2;
        border-left: 8px solid #dc2626;
        border-radius: 10px;
        padding: 22px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.12);
    }
    
    .metric-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 18px;
        text-align: center;
    }
    
    .metric-number {
        font-size: 26px;
        font-weight: 700;
        color: #1e293b;
    }
    
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.5px;
    }
    
    .rule-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 6px solid #2874F0;
        transition: transform 0.1s ease;
    }
    
    .badge-allow {
        background-color: #d1fae5;
        color: #065f46;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 6px;
        display: inline-block;
        font-size: 13px;
    }

    .badge-ask {
        background-color: #fef3c7;
        color: #92400e;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 6px;
        display: inline-block;
        font-size: 13px;
    }

    .badge-block {
        background-color: #fee2e2;
        color: #991b1b;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 6px;
        display: inline-block;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

def safe_rerun():
    """Trigger rerun safely across different Streamlit versions."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        safe_rerun()

# ----------------- Top Header Banner -----------------
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
            <div style="font-size: 30px; font-weight: 800; letter-spacing: -0.5px; display: flex; align-items: center; gap: 10px;">
                <span>🛒 Flipkart AI Agent Gatekeeper</span>
            </div>
            <div style="font-size: 15px; opacity: 0.95; margin-top: 6px;">
                Autonomous Shopping Governance & Policy Enforcement Engine
            </div>
        </div>
        <div>
            <div class="enrolment-pill">
                🎓 Enrolment No: PGD202570278
            </div>
            <div class="academic-pill">
                Academic Prototype
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- Top Metrics Summary -----------------
summary = database.get_audit_summary()

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{summary['total_agents']}</div>
        <div class="metric-label">Registered Agents ({summary['active_agents']} Active)</div>
    </div>
    """, unsafe_allow_html=True)

with col_m2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number">{summary['total_requests']}</div>
        <div class="metric-label">Total Gatekeeper Checks</div>
    </div>
    """, unsafe_allow_html=True)

with col_m3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number" style="color: #059669;">{summary['allowed']}</div>
        <div class="metric-label">Autonomous ALLOW</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number" style="color: #d97706;">{summary['ask_customer']}</div>
        <div class="metric-label">Step-Up ASK CUSTOMER</div>
    </div>
    """, unsafe_allow_html=True)

with col_m5:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-number" style="color: #dc2626;">{summary['blocked']}</div>
        <div class="metric-label">Enforced BLOCK</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- Sidebar Quick Actions -----------------
st.sidebar.image("https://static-assets-web.flixcart.com/batman-returns/batman-returns/p/images/fkheaderlogo_exploreplus-448295.svg", width=160)
st.sidebar.markdown("### 🛡️ Flipkart Gatekeeper")
st.sidebar.info(
    "**Student Enrolment:**\n\n"
    "**PGD202570278**\n\n"
    "*Autonomous Agent Governance Demonstration*"
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### ⚙️ Quick Database Controls")
if st.sidebar.button("🔄 Reload Demo Seed Data"):
    seed_data.seed_demo_data(force=True)
    st.sidebar.success("Database re-seeded with demo records!")
    safe_rerun()

if st.sidebar.button("🗑️ Clear Audit Trail"):
    database.clear_audit_logs()
    st.sidebar.warning("Audit logs cleared.")
    safe_rerun()

st.sidebar.markdown("---")
st.sidebar.caption("📌 Local Database: `gatekeeper.db` (SQLite)\n\nPersists all agents, revocation dates, and audit logs across application restarts.")

# ----------------- Main Navigation Tabs -----------------
tab_perm, tab_tests, tab_agents, tab_audit, tab_rules = st.tabs([
    "🛡️ Permission Check",
    "🧪 1-Click Rule Scenarios (R1 - R7)",
    "🤖 Agent Registration & Revocation",
    "📋 Audit Trail & Logs",
    "📖 Business Rulebook"
])


# ==============================================================================
# TAB 1: PERMISSION CHECK
# ==============================================================================
with tab_perm:
    st.subheader("🛡️ AI Agent Permission Check")
    st.markdown(
        "Evaluate an incoming action requested by an AI agent acting on behalf of a customer. "
        "The Gatekeeper evaluates business rules **R1 through R7** in real-time."
    )

    # Get active registered agents for easy dropdown autocompletion
    all_agents_list = database.list_agents()
    registered_customer_names = sorted(list(set([a["customer_name"] for a in all_agents_list])))
    registered_agent_names = sorted(list(set([a["agent_name"] for a in all_agents_list])))

    # Input Form
    with st.form("permission_check_form"):
        col1, col2 = st.columns(2)

        with col1:
            # Customer Name input
            cust_mode = st.radio(
                "Customer Selection Mode:",
                ["Pick from Registered Customers", "Enter Custom / New Customer"],
                horizontal=True
            )
            if cust_mode == "Pick from Registered Customers" and registered_customer_names:
                customer_name_input = st.selectbox("Customer Name:", registered_customer_names)
            else:
                customer_name_input = st.text_input("Customer Name:", value="Rahul Sharma", placeholder="e.g. Rahul Sharma")

            # Agent Name input
            agent_mode = st.radio(
                "Agent Selection Mode:",
                ["Pick from Registered Agents", "Enter Custom / Unknown Agent"],
                horizontal=True
            )
            if agent_mode == "Pick from Registered Agents" and registered_agent_names:
                agent_name_input = st.selectbox("Agent Name:", registered_agent_names)
            else:
                agent_name_input = st.text_input("Agent Name:", value="Flipkart_Shopper_Bot", placeholder="e.g. Flipkart_Shopper_Bot")

        with col2:
            action_input = st.selectbox(
                "Requested Action:",
                gatekeeper.SUPPORTED_ACTIONS,
                help="Select the shopping activity requested by the AI agent."
            )

            # Amount input with contextual default
            default_amount = 0.0
            if action_input == gatekeeper.ACTION_PURCHASE:
                default_amount = 3500.0
            elif action_input == gatekeeper.ACTION_CANCEL_REFUND:
                default_amount = 3500.0
            elif action_input == gatekeeper.ACTION_ADD_TO_CART:
                default_amount = 1299.0

            amount_input = st.number_input(
                "Transaction Amount (₹):",
                min_value=0.0,
                max_value=1000000.0,
                value=float(default_amount),
                step=100.0,
                format="%.2f",
                help="Monetary amount associated with the action. (Rules R5 & R6 apply a ₹5,000 threshold for purchases)."
            )

            st.caption("💡 *Note: Product browsing requires ₹0. Purchases up to ₹5,000 are auto-approved; purchases above ₹5,000 require customer confirmation.*")

        submitted = st.form_submit_button("⚡ Evaluate Permission with Gatekeeper")

    # Handle Form Submission
    if submitted:
        if not customer_name_input.strip() or not agent_name_input.strip():
            st.error("Customer Name and Agent Name cannot be blank.")
        else:
            result = gatekeeper.evaluate_permission(
                customer_name=customer_name_input,
                agent_name=agent_name_input,
                action=action_input,
                amount=amount_input,
                log_to_audit=True
            )

            # Display Decision Card
            decision = result["decision"]
            rule_num = result["rule_number"]
            reason = result["reason"]

            if decision == "ALLOW":
                card_class = "decision-card-allow"
                icon = "✅"
                color = "#059669"
            elif decision == "ASK CUSTOMER":
                card_class = "decision-card-ask"
                icon = "⚠️"
                color = "#d97706"
            else:  # BLOCK
                card_class = "decision-card-block"
                icon = "🛑"
                color = "#dc2626"

            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-size: 26px; font-weight: 800; color: {color};">
                        {icon} GATEKEEPER DECISION: {decision}
                    </div>
                    <div>
                        <span style="background: {color}; color: white; padding: 5px 14px; border-radius: 6px; font-weight: 700; font-size: 15px;">
                            Rule Applied: {rule_num}
                        </span>
                    </div>
                </div>
                <div style="font-size: 16px; color: #1e293b; margin-top: 10px; line-height: 1.5;">
                    <strong>Decision Reason:</strong> {reason}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Detailed Request Metadata Table
            res_col1, res_col2, res_col3, res_col4 = st.columns(4)
            with res_col1:
                st.write("**Customer:**", result["customer_name"])
                st.write("**Agent Name:**", result["agent_name"])
            with res_col2:
                st.write("**Agent Status in DB:**", result["agent_status"])
                st.write("**Action Requested:**", result["action"])
            with res_col3:
                st.write("**Transaction Amount:**", f"₹{result['amount']:,.2f}")
                st.write("**Evaluation Time:**", result["timestamp"])
            with res_col4:
                st.write("**Audit Log ID:**", f"#{result['log_id']}")
                st.write("**Persistence:**", "Saved to `gatekeeper.db`")


# ==============================================================================
# TAB 2: 1-CLICK TEST SCENARIOS (ALL 7 RULES)
# ==============================================================================
with tab_tests:
    st.subheader("🧪 1-Click Interactive Test Scenarios for Rules R1 to R7")
    st.markdown(
        "Use these pre-configured test scenarios to verify all seven business rules with a single click. "
        "Each scenario automatically executes against the local SQLite database and records the event into the audit trail."
    )

    # Batch Runner Button
    if st.button("🚀 Run All 7 Rules Sequentially & Generate Test Report"):
        test_results = []
        for scen in TEST_SCENARIOS:
            res = gatekeeper.evaluate_permission(
                customer_name=scen["customer_name"],
                agent_name=scen["agent_name"],
                action=scen["action"],
                amount=scen["amount"],
                log_to_audit=True
            )
            passed = (res["decision"] == scen["expected_decision"]) and (res["rule_number"] == scen["rule"])
            test_results.append({
                "Rule": scen["rule"],
                "Scenario": scen["title"],
                "Action": scen["action"],
                "Amount": f"₹{scen['amount']:,.2f}",
                "Expected Decision": scen["expected_decision"],
                "Actual Decision": res["decision"],
                "Actual Rule": res["rule_number"],
                "Test Status": "PASSED ✅" if passed else "FAILED ❌"
            })
        st.success("All 7 test scenarios executed successfully and logged to the audit trail!")
        df_results = pd.DataFrame(test_results)
        st.table(df_results)

    st.write("")
    st.markdown("---")
    st.markdown("#### Individual Rule Scenarios")

    # Render each scenario as an individual interactive card
    for idx, scen in enumerate(TEST_SCENARIOS):
        rule_id = scen["rule"]
        badge_style = "badge-allow" if scen["expected_decision"] == "ALLOW" else ("badge-ask" if scen["expected_decision"] == "ASK CUSTOMER" else "badge-block")
        
        with st.container():
            col_scen, col_act = st.columns([4, 1])
            with col_scen:
                st.markdown(f"""
                <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px 18px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; font-size: 16px; color: #1e293b;">
                            {scen['title']}
                        </span>
                        <span class="{badge_style}">
                            Expected: {scen['expected_decision']} ({rule_id})
                        </span>
                    </div>
                    <div style="color: #475569; font-size: 14px; margin-top: 6px;">
                        {scen['explanation']}
                    </div>
                    <div style="color: #64748b; font-size: 13px; margin-top: 6px;">
                        <strong>Customer:</strong> {scen['customer_name']} | 
                        <strong>Agent:</strong> {scen['agent_name']} | 
                        <strong>Action:</strong> {scen['action']} | 
                        <strong>Amount:</strong> ₹{scen['amount']:,.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_act:
                if st.button(f"▶️ Run {rule_id}", key=f"run_btn_{rule_id}"):
                    res = gatekeeper.evaluate_permission(
                        customer_name=scen["customer_name"],
                        agent_name=scen["agent_name"],
                        action=scen["action"],
                        amount=scen["amount"],
                        log_to_audit=True
                    )
                    st.session_state[f"result_{rule_id}"] = res

            # If scenario was run, show outcome right underneath
            if f"result_{rule_id}" in st.session_state:
                res = st.session_state[f"result_{rule_id}"]
                dec_color = "#059669" if res["decision"] == "ALLOW" else ("#d97706" if res["decision"] == "ASK CUSTOMER" else "#dc2626")
                st.markdown(f"""
                <div style="background: #f8fafc; border-left: 5px solid {dec_color}; padding: 10px 14px; margin-bottom: 12px; font-size: 14px;">
                    <strong>Evaluated Decision:</strong> <span style="color: {dec_color}; font-weight: 700;">{res['decision']}</span> 
                    (Triggered Rule: <strong>{res['rule_number']}</strong>) | 
                    <strong>Reason:</strong> {res['reason']}
                </div>
                """, unsafe_allow_html=True)


# ==============================================================================
# TAB 3: AGENT REGISTRATION & REVOCATION
# ==============================================================================
with tab_agents:
    st.subheader("🤖 AI Agent Lifecycle Management")
    st.markdown("Register new shopping agents for customers, or immediately revoke existing agents with exact timestamps.")

    col_reg, col_rev = st.columns(2)

    # Sub-form 1: Agent Registration
    with col_reg:
        st.markdown("#### ➕ 1. Register AI Agent")
        with st.form("agent_registration_form"):
            reg_customer = st.text_input("Customer Full Name:", placeholder="e.g. Rahul Sharma")
            reg_agent = st.text_input("AI Agent Name / Identifier:", placeholder="e.g. Flipkart_Shopper_Bot_02")
            reg_desc = st.text_input("Purpose / Description (Optional):", placeholder="e.g. Autonomous grocery replenishment agent")
            
            submit_reg = st.form_submit_button("Register AI Agent")
            if submit_reg:
                if not reg_customer.strip() or not reg_agent.strip():
                    st.error("Both Customer Name and Agent Name are required.")
                else:
                    outcome = database.register_agent(reg_agent, reg_customer, reg_desc)
                    if outcome["success"]:
                        st.success(outcome["message"])
                    else:
                        st.warning(outcome["message"])
                    safe_rerun()

    # Sub-form 2: Agent Revocation
    with col_rev:
        st.markdown("#### 🚫 2. Revoke AI Agent")
        active_agents = database.list_agents(filter_status="ACTIVE")
        
        if not active_agents:
            st.info("No active agents found in the system to revoke.")
        else:
            agent_options = {
                f"{a['agent_name']} (Customer: {a['customer_name']} | ID #{a['id']})": a['id'] 
                for a in active_agents
            }
            selected_agent_label = st.selectbox("Select Active Agent to Revoke:", list(agent_options.keys()))
            selected_agent_id = agent_options[selected_agent_label]

            # Display selected agent info
            chosen_agent = next((a for a in active_agents if a["id"] == selected_agent_id), None)
            if chosen_agent:
                st.caption(f"Registered on: `{chosen_agent['registered_at']}` | Customer: `{chosen_agent['customer_name']}`")

            if st.button("🚨 Revoke Agent Access Now"):
                rev_outcome = database.revoke_agent(selected_agent_id)
                if rev_outcome["success"]:
                    st.error(f"🛑 {rev_outcome['message']}")
                    st.info(f"Exact Revocation Timestamp Recorded: **{rev_outcome['revoked_at']}**")
                else:
                    st.warning(rev_outcome["message"])
                safe_rerun()

    st.write("")
    st.markdown("---")
    st.markdown("#### 📂 Agent Directory")

    status_filter = st.radio("Filter Agents by Status:", ["ALL", "ACTIVE", "REVOKED"], horizontal=True)
    agents_list = database.list_agents(filter_status=status_filter)

    if agents_list:
        df_agents = pd.DataFrame(agents_list)
        # Rename columns for presentation
        df_agents = df_agents.rename(columns={
            "id": "ID",
            "agent_name": "Agent Name",
            "customer_name": "Customer Name",
            "status": "Status",
            "registered_at": "Registered At",
            "revoked_at": "Revoked At",
            "description": "Description"
        })
        # Format None values
        df_agents["Revoked At"] = df_agents["Revoked At"].fillna("-")
        df_agents["Description"] = df_agents["Description"].fillna("-")
        st.dataframe(df_agents)
    else:
        st.info("No agents match the selected filter.")


# ==============================================================================
# TAB 4: AUDIT TRAIL & LOGS
# ==============================================================================
with tab_audit:
    st.subheader("📋 Gatekeeper Audit Log & Activity History")
    st.markdown(
        "Every permission check performed by the Gatekeeper is immutably recorded in the local SQLite database "
        "with its timestamp, customer, agent, requested action, amount, decision, and applied rule number."
    )

    # Filter Controls
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        f_decision = st.selectbox("Filter by Decision:", ["ALL", "ALLOW", "ASK CUSTOMER", "BLOCK"])
    with col_f2:
        f_rule = st.selectbox("Filter by Rule:", ["ALL", "R1", "R2", "R3", "R4", "R5", "R6", "R7"])
    with col_f3:
        f_search = st.text_input("Search Customer / Agent / Action:", placeholder="e.g. Rahul")

    logs = database.get_audit_logs(
        limit=500,
        filter_decision=f_decision,
        filter_rule=f_rule,
        search_query=f_search
    )

    if logs:
        df_logs = pd.DataFrame(logs)
        df_logs_display = df_logs.rename(columns={
            "id": "Log ID",
            "timestamp": "Timestamp",
            "customer_name": "Customer",
            "agent_name": "Agent Name",
            "action": "Action",
            "amount": "Amount (₹)",
            "decision": "Decision",
            "rule_number": "Rule",
            "reason": "Applied Reason"
        })
        
        # Format Amount
        df_logs_display["Amount (₹)"] = df_logs_display["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
        
        st.write(f"Showing **{len(df_logs_display)}** audit entries:")
        st.dataframe(df_logs_display)

        # Download CSV
        csv_data = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Audit Trail as CSV",
            data=csv_data,
            file_name=f"flipkart_gatekeeper_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No audit logs match your filter criteria.")


# ==============================================================================
# TAB 5: BUSINESS RULEBOOK
# ==============================================================================
with tab_rules:
    st.subheader("📖 Flipkart AI Agent Gatekeeper Rulebook")
    st.markdown(
        "The Gatekeeper operates as an authoritative boundary between autonomous shopping AI agents and Flipkart's "
        "transaction APIs. It strictly enforces the seven deterministic business rules defined below:"
    )

    for rule in gatekeeper.RULEBOOK:
        r_num = rule["rule_number"]
        r_dec = rule["decision"]
        r_badge = "badge-allow" if r_dec == "ALLOW" else ("badge-ask" if r_dec == "ASK CUSTOMER" else "badge-block")

        st.markdown(f"""
        <div class="rule-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-size: 18px; font-weight: 800; color: #2874F0;">
                    {r_num}: {rule['name']}
                </span>
                <span class="{r_badge}">
                    Decision: {r_dec}
                </span>
            </div>
            <div style="font-size: 15px; font-weight: 600; color: #1e293b; margin: 4px 0;">
                {rule['description']}
            </div>
            <div style="font-size: 13px; color: #475569; margin-top: 6px;">
                <strong>Trigger Condition:</strong> {rule['condition']} &bull; 
                <strong>Action Scope:</strong> {rule['action_scope']} &bull; 
                <strong>Threshold:</strong> {rule['threshold']}
            </div>
            <div style="font-size: 13px; color: #64748b; margin-top: 6px; font-style: italic;">
                🛡️ <strong>Flipkart Safety Rationale:</strong> {rule['rationale']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("---")
    st.markdown("#### 🏗️ System Architecture & Defense-in-Depth Model")
    st.markdown("""
```
 +------------------------+
 |    Customer Request    |
 +-----------+------------+
             |
             v
 +------------------------+
 |   Autonomous AI Agent  |  (Acts on customer's behalf)
 +-----------+------------+
             |
             v
 [ FLIPKART AI AGENT GATEKEEPER ]  <--- ENROLMENT NO: PGD202570278
      |
      +---> Check 1: Is Agent Registered in SQLite DB? ------ No ----> [ BLOCK (R1) ]
      |
      +---> Check 2: Has Agent been Revoked? ----------------- Yes ---> [ BLOCK (R2) ]
      |
      +---> Check 3: Is Action = 'Browse Products'? --------- Yes ---> [ ALLOW (R3) ]
      |
      +---> Check 4: Is Action = 'Add to Cart'? ------------- Yes ---> [ ALLOW (R4) ]
      |
      +---> Check 5: Is Action = 'Purchase' (Amount <= 5k)? - Yes ---> [ ALLOW (R5) ]
      |
      +---> Check 6: Is Action = 'Purchase' (Amount > 5k)? -- Yes ---> [ ASK CUSTOMER (R6) ]
      |
      +---> Check 7: Is Action = 'Cancel / Refund'? --------- Yes ---> [ ASK CUSTOMER (R7) ]
      |
      v
 [ Local SQLite Audit Log (gatekeeper.db) ] (Persistent timestamp, customer, agent, amount, decision, rule)
```
    """)

    st.markdown("---")
    st.warning("⚠️ **Academic Demonstration Disclaimer**: This project is built solely for educational and research demonstration under student enrolment number **PGD202570278**. It is not connected to real Flipkart production user accounts, bank APIs, or live merchant order channels.")

# ----------------- Footer -----------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 13px; padding-bottom: 20px;">
    Flipkart AI Agent Gatekeeper Prototype &bull; Student Enrolment No: <strong>PGD202570278</strong> &bull; Python & Streamlit & SQLite &bull; Academic Prototype
</div>
""", unsafe_allow_html=True)
