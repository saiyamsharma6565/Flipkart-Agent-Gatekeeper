"""
Database module for Flipkart AI Agent Gatekeeper Prototype.
Uses SQLite for persistent local storage across restarts.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_FILE = "gatekeeper.db"


def get_connection():
    """Establish and return a SQLite database connection with row factory."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables for agents and audit logs."""
    conn = get_connection()
    cursor = conn.cursor()

    # Table 1: Agents
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('ACTIVE', 'REVOKED')),
            registered_at TEXT NOT NULL,
            revoked_at TEXT,
            description TEXT,
            UNIQUE(agent_name, customer_name)
        )
    """)

    # Table 2: Audit Logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            action TEXT NOT NULL,
            amount REAL NOT NULL,
            decision TEXT NOT NULL CHECK(decision IN ('ALLOW', 'ASK CUSTOMER', 'BLOCK')),
            rule_number TEXT NOT NULL,
            reason TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- Agent Operations ----------------

def register_agent(agent_name: str, customer_name: str, description: str = "") -> Dict[str, Any]:
    """
    Register a new AI Agent for a customer.
    If already exists and REVOKED, re-activates the agent.
    """
    agent_name = agent_name.strip()
    customer_name = customer_name.strip()
    if not agent_name or not customer_name:
        return {"success": False, "message": "Agent name and Customer name cannot be empty."}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM agents WHERE LOWER(agent_name) = LOWER(?) AND LOWER(customer_name) = LOWER(?)",
        (agent_name, customer_name)
    )
    existing = cursor.fetchone()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if existing:
        if existing["status"] == "ACTIVE":
            conn.close()
            return {"success": False, "message": f"Agent '{agent_name}' is already ACTIVE for customer '{customer_name}'."}
        else:
            # Re-activate revoked agent
            cursor.execute("""
                UPDATE agents 
                SET status = 'ACTIVE', revoked_at = NULL, description = ?, registered_at = ?
                WHERE id = ?
            """, (description or existing["description"], now_str, existing["id"]))
            conn.commit()
            conn.close()
            return {"success": True, "message": f"Agent '{agent_name}' has been RE-ACTIVATED for customer '{customer_name}'."}

    cursor.execute("""
        INSERT INTO agents (agent_name, customer_name, status, registered_at, revoked_at, description)
        VALUES (?, ?, 'ACTIVE', ?, NULL, ?)
    """, (agent_name, customer_name, now_str, description))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Agent '{agent_name}' successfully registered for customer '{customer_name}'."}


def revoke_agent(agent_id: int) -> Dict[str, Any]:
    """Revoke an agent by ID and save exact date & time of revocation."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
    agent = cursor.fetchone()
    if not agent:
        conn.close()
        return {"success": False, "message": f"Agent with ID {agent_id} not found."}

    if agent["status"] == "REVOKED":
        conn.close()
        return {"success": False, "message": f"Agent '{agent['agent_name']}' is already REVOKED."}

    revoked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE agents SET status = 'REVOKED', revoked_at = ? WHERE id = ?", (revoked_at, agent_id))
    conn.commit()
    conn.close()
    return {
        "success": True, 
        "message": f"Agent '{agent['agent_name']}' for customer '{agent['customer_name']}' has been revoked at {revoked_at}.",
        "revoked_at": revoked_at
    }


def get_agent(agent_name: str, customer_name: str) -> Optional[Dict[str, Any]]:
    """Look up an agent by agent_name and customer_name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM agents WHERE LOWER(agent_name) = LOWER(?) AND LOWER(customer_name) = LOWER(?)",
        (agent_name.strip(), customer_name.strip())
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def list_agents(filter_status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return all registered agents, optionally filtered by status."""
    conn = get_connection()
    cursor = conn.cursor()
    if filter_status and filter_status != "ALL":
        cursor.execute("SELECT * FROM agents WHERE status = ? ORDER BY id DESC", (filter_status,))
    else:
        cursor.execute("SELECT * FROM agents ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------------- Audit Log Operations ----------------

def log_request(
    customer_name: str,
    agent_name: str,
    action: str,
    amount: float,
    decision: str,
    rule_number: str,
    reason: str,
    timestamp: Optional[str] = None
) -> int:
    """Save an evaluation request and its gatekeeper decision to audit logs."""
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_logs (timestamp, customer_name, agent_name, action, amount, decision, rule_number, reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, customer_name.strip(), agent_name.strip(), action, float(amount), decision, rule_number, reason))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return log_id


def get_audit_logs(
    limit: int = 500,
    filter_decision: Optional[str] = None,
    filter_rule: Optional[str] = None,
    search_query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Fetch audit logs with optional filters."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM audit_logs WHERE 1=1"
    params = []

    if filter_decision and filter_decision != "ALL":
        query += " AND decision = ?"
        params.append(filter_decision)

    if filter_rule and filter_rule != "ALL":
        query += " AND rule_number = ?"
        params.append(filter_rule)

    if search_query:
        query += " AND (LOWER(customer_name) LIKE ? OR LOWER(agent_name) LIKE ? OR LOWER(action) LIKE ?)"
        wildcard = f"%{search_query.lower()}%"
        params.extend([wildcard, wildcard, wildcard])

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_audit_summary() -> Dict[str, Any]:
    """Return aggregated metrics for dashboard summary cards."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM audit_logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM audit_logs WHERE decision = 'ALLOW'")
    allowed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM audit_logs WHERE decision = 'ASK CUSTOMER'")
    ask_customer = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM audit_logs WHERE decision = 'BLOCK'")
    blocked = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM agents")
    total_agents = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM agents WHERE status = 'ACTIVE'")
    active_agents = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM agents WHERE status = 'REVOKED'")
    revoked_agents = cursor.fetchone()[0]

    conn.close()

    return {
        "total_requests": total,
        "allowed": allowed,
        "ask_customer": ask_customer,
        "blocked": blocked,
        "total_agents": total_agents,
        "active_agents": active_agents,
        "revoked_agents": revoked_agents
    }


def clear_audit_logs():
    """Clear audit logs table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM audit_logs")
    conn.commit()
    conn.close()


def reset_database():
    """Drop and recreate tables."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS agents")
    cursor.execute("DROP TABLE IF EXISTS audit_logs")
    conn.commit()
    conn.close()
    init_db()
