# PROMPTS.md
## Flipkart Agent Gatekeeper

**Student Name:** Saiyam Sharma  
**Enrolment Number:** PGD202570278  
**Company:** Flipkart  
**Development Tool:** Google Antigravity

### 1. Main Project Development Prompt

I want to build a simple AI Agent Gatekeeper prototype for Flipkart using Python and Streamlit. The application should check whether an AI agent is authorised to perform shopping activities on behalf of a customer.

The application should accept customer name, agent name, requested action and transaction amount. It should return one of three decisions: ALLOW, ASK CUSTOMER or BLOCK. Each decision should display a clear reason and the applicable business rule number.

The application should include agent registration, agent revocation, permission checking, an audit log and a rulebook. It should store agent details and request records in a local database. Display my enrolment number PGD202570278 on the main dashboard.

### 2. Business Rules Prompt

Implement the following seven business rules:

- R1: Unknown or unregistered agents must be BLOCKED.
- R2: Revoked agents must be BLOCKED.
- R3: Registered agents can browse products – ALLOW.
- R4: Registered agents can add products to the cart – ALLOW.
- R5: Purchases up to ₹5,000 – ALLOW.
- R6: Purchases above ₹5,000 – ASK CUSTOMER.
- R7: Cancellation and refund requests – ASK CUSTOMER.

Make sure every decision displays its reason and rule number.

### 3. Agent Registration and Revocation Prompt

Create a registration feature where customers can register an AI agent. Store the customer name, agent name, registration status and registration date/time.

Also create a revocation feature. When an agent is revoked, update its status and save the revocation date/time. A revoked agent must not be allowed to perform any further actions.

### 4. Audit Log Prompt

Create an audit log that automatically records every permission-checking request. Store the date/time, customer name, agent name, requested action, transaction amount, decision, reason and applicable rule number.

Display the records in a readable table.

### 5. Debugging and Error-Fixing Prompt

The application encountered a RecursionError during execution. Check the code for recursive rerun calls, particularly the safe_rerun() function. Replace the incorrect recursive behaviour with the appropriate Streamlit rerun method. Check the remaining code for similar issues and fix them without removing existing features, business rules or database records.

### 6. Testing Prompt

Test the application using different scenarios, including:

1. Registered agent browsing products.
2. Registered agent adding products to the cart.
3. Purchase of ₹4,500.
4. Purchase of ₹7,000.
5. Refund request.
6. Unknown agent attempting an action.
7. Revoked agent attempting an action.

Verify that the application produces the correct decision, reason and rule number for each scenario.

### 7. My Personal Contribution

I personally reviewed the business rules, checked the application outputs, registered an agent, performed permission-checking tests and verified the audit log. I also checked whether the system displayed the correct decisions for different shopping activities.

**Note:** This file documents the prompts used or reconstructed from the project development process. Adjust the wording if it differs from the exact prompts entered into Google Antigravity. The project is an academic prototype and is not connected to Flipkart's actual systems.
