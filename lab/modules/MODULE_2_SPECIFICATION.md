# Module 2: Specification with `/speckit.specify` - AI Agents in Microsoft Foundry

**Estimated Duration**: 70–85 minutes  
**Prerequisites**: Complete Module 1, understand SDD principles  
**Deliverable**: Complete customer service agent specification (`specs/001-customer-service-agent/spec.md`) using `/speckit.specify` command

---

## 🎯 Learning Objectives

By the end of this module, you will:

1. **Understand intent specification:** How to translate vague user needs into executable, measurable specifications
2. **Write user stories for agents:** Applying traditional user story techniques to agentic systems
3. **Define acceptance criteria:** Clear, testable conditions that determine agent success
4. Practice the **spec-kit `/speckit.specify`** workflow with Foundry and Agent Framework focus
5. **Build specifications iteratively:** Refining requirements through clarification and feedback


---


## Section 1: From Vague Idea to Executable Specification

### The Challenge

Users rarely arrive with perfectly articulated needs:

```
User: "I need an agent to help with customer support"

⚠️ Problems:
- What kind of support? (billing, technical, returns?)
- What should the agent do? (answer FAQs, process refunds, escalate?)
- How do we measure success? (customer satisfaction, resolution time?)
- What constraints exist? (security, compliance, budget?)
```

### The Specification-Driven Solution

Our lab builds a **Customer Service AI Agent** - a conversational system that helps customers resolve issues autonomously.

**Real-World Context**:
- A medium-sized e-commerce company receives 500+ customer support inquiries daily
- Current support team spends 30% of time on routine questions: "Where's my order?" "How do I return an item?" "What's my refund status?"
- Goal: Automate these routine queries, freeing support team for complex issues
- Opportunity: Provide instant 24/7 support instead of business hours only

**Success Metrics** (business perspective):
- 70% of incoming customer inquiries resolved without human intervention
- First response time < 5 seconds (vs. 2–4 hour queue)
- Customer satisfaction ≥ 4.2/5.0 for automated interactions
- 15% reduction in support team workload

### Translating Real-World Needs into Specifications

**Real-World Need** → **Agent Intent** → **Tools Needed** → **Success Criteria**

#### From Idea to Executable Specification
Transform vague ideas into **executable specifications** through iterative refinement:

```
Initial Idea → Clarifying Questions → User Stories → Acceptance Criteria → Executable Spec
    ↓
"Help with customer support"
    ↓
Agent can handle order returns, check refund status, 
escalate complex issues to humans
    ↓
Story 1: "Customer initiates order return"
Story 2: "Customer checks refund status"
Story 3: "Agent escalates to human support"
    ↓
Acceptance: Return processed within 30 seconds, 
status accurate, escalation preserves context
    ↓
Spec template populated with measurable requirements,
tool contracts, success scenarios
```

---

## Section 2: Understanding User Intents

### Intent vs. Feature

| **Intent** | **Feature** |
|-----------|-----------|
| What the user needs (outcome-focused) | How we build it (implementation-focused) |
| "Book me a flight to Paris next month" | "Create a flight booking microservice with Stripe integration" |
| "Help me troubleshoot my internet connection" | "Build a diagnostic chatbot with ML inference" |

### Well-Formed Intent Attributes

A good intent for an agent has:

1. **Clarity:** No ambiguity about what the user wants
2. **Measurability:** Success can be verified objectively
3. **Scope:** Achievable within 60–90 minutes of development
4. **Constraints:** Security, compliance, or performance limits are explicit
5. **Context:** User role, environment, and assumptions are clear

### Intent Template

```markdown
# Intent: [Clear Name]

**User Role:** [Who is using the agent?]
**Scenario:** [When and why would this intent occur?]
**Goal:** [What does the user want to achieve?]
**Success Criteria:**
- Criterion 1 (measurable)
- Criterion 2 (measurable)
- Criterion 3 (measurable)

**Constraints:**
- Security: [Any requirements?]
- Compliance: [Regulatory concerns?]
- Performance: [Time/resource limits?]
```

### Example: Customer Support Agent Intent

<details>
<summary>Click to expand example</summary>

```markdown
# Intent: Resolve Customer Order Issues

**User Role:** E-commerce customer with an order problem

**Scenario:** Customer has a question about their order 
(status, shipping, returns) and contacts support

**Goal:** Agent should resolve the issue or escalate to 
a human support specialist without requiring the customer 
to repeat information

**Success Criteria:**
- Agent retrieves correct order within 5 seconds
- Agent answers question OR escalates within 2 minutes
- Escalation to human preserves full conversation context
- Customer receives confirmation (resolution or ticket #)

**Constraints:**
- Security: Cannot expose PII (addresses, payment info)
- Compliance: GDPR-compliant data access only
- Performance: 99.5% uptime during business hours
```

</details>

---

## Section 3: User Stories for Agents

### What Is a User Story?

A user story captures **one small piece** of functionality from the user's perspective:

```
As a [user role]
I want to [action]
So that [benefit/outcome]
```

User stories work beautifully for agents because they:
- Force focus on user perspective (not implementation details)
- Are small enough to implement in one sprint
- Naturally translate to agent capabilities (intents + tools)

### User Stories vs. Agent Intents

**User Story:** One specific, actionable user need  
**Intent:** The broader goal that multiple user stories fulfill

**Example:**

```
INTENT: Resolve Customer Order Issues

USER STORY 1:
As a customer
I want to check the status of my order
So that I know when to expect delivery

USER STORY 2:
As a customer
I want to initiate a return without calling support
So that I can save time

USER STORY 3:
As a customer
I want to talk to a human if my issue is complex
So that I get personalized help

USER STORY 4:
As a support agent
I want the customer's issue history when they escalate
So that I don't make them repeat themselves
```

### User Story Template for Agents

```markdown
# User Story: [Descriptive Title]

**Story ID:** US-001

**As a** [user role]  
**I want to** [action the agent should enable]  
**So that** [user benefit]

## Acceptance Criteria

- [ ] Criterion 1: [Testable condition]
- [ ] Criterion 2: [Testable condition]
- [ ] Criterion 3: [Testable condition]

## Agent Behavior

**Happy Path:** [Describe successful scenario]
- Input: [What user provides]
- Agent Actions: [What agent does]
- Output: [What user receives]

**Unhappy Path:** [Describe failure/edge case]
- Input: [What user provides]
- Agent Error: [What goes wrong]
- Agent Recovery: [How agent handles it]

## Clarifying Questions

- [ ] [Question 1 - needs answering?]
- [ ] [Question 2 - needs answering?]
```


### Understanding Acceptance Criteria

**Acceptance Criteria** are the definition of done for each user story. They answer: "How do I know this story is complete?"

### Good Acceptance Criteria:

✅ **Testable**: Can be verified without implementation details  
✅ **Clear**: No ambiguity about what "done" means  
✅ **Complete**: Covers happy path AND edge cases  
✅ **Measurable**: Success is objectively verifiable  

### Bad Acceptance Criteria:

❌ "Agent works well" - Too vague  
❌ "Use FastAPI for the API" - Implementation detail, not behavior  
❌ "Return process is fast" - Not measurable (fast = <1s? <5s?)  
❌ "Agent handles most issues" - Vague quantification  


### Concrete Example

<details>
<summary>Click to expand example</summary>

```markdown
# User Story: Check Order Status

**Story ID:** US-001

**As a** customer with a pending order  
**I want to** ask the agent about my order status  
**So that** I know when my items will arrive

## Acceptance Criteria

- [ ] Agent retrieves the correct order (matches customer ID)
- [ ] Agent provides shipping status within 5 seconds
- [ ] Agent provides estimated delivery date if known
- [ ] If order not found, agent offers alternative help

## Agent Behavior

**Happy Path:**
- Input: "What's the status of my order?"
- Agent Actions:
  1. Identify customer (via session or question)
  2. Search order database for pending orders
  3. Retrieve tracking info from shipping API
  4. Format response with key details
- Output: "Your order #12345 shipped on Jan 2 and will arrive by Jan 7"

**Unhappy Path (order not found):**
- Input: "Where's my order?"
- Agent Error: Order database returns no results
- Agent Recovery: "I couldn't find an order. Can you provide your order number or email?"

## Clarifying Questions

- [NEEDS CLARIFICATION] What if the customer has multiple orders?
- [NEEDS CLARIFICATION] How should agent handle delayed/cancelled orders?
- [NEEDS CLARIFICATION] Can agent access orders from multiple sales channels?
```

</details>

---

## Section 4: Writing Specifications with Spec-Kit

### The Spec-Kit Specification Template

Spec-Kit provides a comprehensive template that guides specification writers. Key sections:

#### 1. **Feature Overview**
- Name and ID (auto-numbered)
- One-sentence description
- Business value

#### 2. **User Stories**
- Complete list of user stories (from Section 3)
- Each story includes acceptance criteria

#### 3. **Acceptance Scenarios**
- Real-world examples demonstrating agent behavior
- Inputs, expected outputs, success criteria

#### 4. **Non-Functional Requirements**
- Performance: Response times, throughput
- Security: Data protection, authentication
- Reliability: Uptime, error handling
- Compliance: Legal or regulatory constraints

#### 5. **Clarification Markers**
- [NEEDS CLARIFICATION] tags for ambiguous requirements
- Questions that must be answered before implementation

#### 6. **Implementation Constraints**
- Technology restrictions (e.g., "must use Foundry")
- Budget or resource limits
- Third-party service limitations

### Guidelines for Writing Effective Specification Prompts

When writing your `/speckit.specify` prompt for an AI Agent in Foundry:

1. **Start with User Needs**: "Users want to..."
2. **Describe Agent Intents**: What are the key things the agent must accomplish?
3. **Mention Tool Requirements**: What data/APIs does the agent need to access?
4. **Include Escalation Logic**: When should the agent hand off to humans?
5. **Define Success Metrics**: Quantifiable outcomes (resolution rate, response time, satisfaction)
6. **Focus on WHAT, not HOW**: Don't specify Python, FastAPI, or Foundry details (that's Module 3)
7. **Foundry Context**: Mention this will be deployed to Microsoft Foundry with Agent Framework

**Golden Rule**: A good specification reads like a user manual describing what an agent should do, not a technical architecture document.


### Using the Spec-Kit CLI

```bash
# Initialize a new feature specification
/speckit.specify "Customer Support Agent for E-commerce Platform"

# This automatically:
# 1. Creates a branch (e.g., "001-customer-support-agent")
# 2. Creates specs/001-customer-support-agent/spec.md
# 3. Populates with template structure
```

---

## Section 5: Iterative Refinement

### The Specification Feedback Loop

Specifications improve through iteration:

```
Draft Spec → Review → Clarifications → Updated Spec → Ready
              ↑                              |
              └──────────────────────────────┘
```

### Checklist for Specification Completeness

Before marking a specification as "ready for implementation," verify:

- [ ] **No remaining [NEEDS CLARIFICATION] markers**
  - If markers exist, add answers or remove speculative requirements

- [ ] **User stories are testable**
  - Each acceptance criterion can be verified objectively
  - No vague terms like "good," "fast," or "reliable"

- [ ] **Success scenarios are realistic**
  - Based on actual user workflows
  - Include both happy and unhappy paths

- [ ] **Non-functional requirements are measurable**
  - Performance targets have specific numbers (5 seconds, not "fast")
  - Compliance requirements reference specific standards

- [ ] **Implementation constraints are explicit**
  - Technology choices are justified
  - Budget and timeline are realistic

- [ ] **Risk identification**
  - External dependencies are called out
  - Mitigation strategies are proposed


---

### 🔧 Hands-On: Generate Specification with `/speckit.specify`

#### Step 1: Open VS Code in Your Project

```bash
cd /TechConnect-2026/LAB-1073
code .
```

#### Step 2: Open GitHub Copilot Chat in VS Code

1. **Open the Copilot Chat panel**:
   - Press `Cmd+Shift+I` (Mac) or `Ctrl+Shift+I` (Windows/Linux)
   - Or click the Copilot Chat icon in the left sidebar

2. **In the Copilot Chat window**, you'll see a chat interface where you can enter prompts

#### Step 3: Use the `/speckit.specify` Command

In the GitHub Copilot Chat interface, paste one of the prompts below and press Enter. Copilot will generate a complete specification file.

#### Example Prompts for Customer Service Agent

**Option 1: Customer Service Agent (Full Featured)**
```
/speckit.specify Build an AI agent for customer service using Microsoft Agent 
Framework that will be deployed to Foundry. The agent helps retail customers 
resolve common issues: (1) Look up order status and tracking information by 
customer account or order ID, (2) Check return/refund eligibility and initiate 
returns with automatic return labels, (3) Track refund status and provide timeline, 
(4) Escalate complex issues to human support with full conversation context. The 
agent should: (1) Understand natural language requests ("Where's my order?", "How 
do I return this?"), (2) Call backend tools to access customer and order data, 
(3) Maintain conversation context across multiple turns, (4) Proactively suggest 
solutions based on issue type. Agent should escalate if: customer explicitly 
requests human help, issue involves product quality/complaints, customer shows 
frustration, or agent cannot resolve after 2 tool calls. Success metrics: 70% of 
inquiries resolved without escalation, first response <5 seconds, customer 
satisfaction ≥4.2/5, support team workload reduced 40%.
```

**Option 2: Minimal MVP (Fast Iteration)**
```
/speckit.specify Build a minimal AI agent for customer service (MVP) using 
Microsoft Agent Framework for Foundry deployment. The agent handles the most 
common customer question: order status and tracking. Customers can ask in natural 
language "Where's my order?" or "Track order #12345" and the agent retrieves and 
displays order status with tracking number and estimated delivery. The agent can 
also handle: (1) Customer authentication to look up orders by email, (2) Escalate 
to human if order not found, (3) Provide shipping carrier tracking link. Success: 
80% of "where's my order" questions resolved in under 30 seconds without human 
help.
```

**Option 3: Advanced with Proactive AI**
```
/speckit.specify Build an advanced AI customer service agent (Microsoft Agent 
Framework, Foundry deployment) that goes beyond answering questions—it proactively 
helps customers. The agent can: (1) Look up orders and provide status proactively 
with tracking links and ETAs, (2) Detect when customers have potential issues 
(delivery delays, long waits for refunds) and suggest solutions before being asked, 
(3) Recommend relevant actions based on conversation context (offer return if 
customer mentions defect, offer review if order delivered), (4) Escalate to human 
for complaints or policy exceptions. The agent maintains context across turns—if 
customer asked about order #123, follow-up questions automatically reference that 
order. Escalation includes full conversation history. Success: Customer feels 
agent truly understands their situation; resolution rate 75%+.
```

**Option 4: High-Reliability Enterprise Version**
```
/speckit.specify Build a high-reliability AI customer service agent for enterprise 
use (Microsoft Agent Framework, Foundry). This agent MUST work correctly—failures 
cascade to customer frustration. The agent: (1) Authenticates customers securely, 
(2) Accesses customer data with strict data privacy (no PII in logs), (3) Handles 
edge cases gracefully (missing data, system errors, duplicate orders), (4) Provides 
clear next steps for all scenarios, (5) Always offers escalation as fallback. The 
agent must: Handle concurrent conversations (100+ simultaneously), maintain 
consistent response quality, log all interactions for compliance, never lose 
conversation context. Escalations to human support must include: full conversation 
history, all tool calls made, extracted customer intent, recommended next step. 
Success: 99.9% uptime, zero data privacy incidents, 80% first-contact resolution, 
customer satisfaction ≥4.5/5.
```

#### What These Prompts Include

Notice how each prompt:

✅ **Describes user needs** in natural language  
✅ **Lists agent intents** (what agent must accomplish)  
✅ **Specifies tools** agent needs to call (order lookup, refund status, etc.)  
✅ **Defines escalation logic** (when to hand off to human)  
✅ **Includes success metrics** (quantifiable outcomes)  
✅ **Mentions Foundry & Agent Framework** as context  
✅ **Avoids implementation details** (no "use Python", "use FastAPI", "use PostgreSQL")  

---

#### How to Run It

1. **Open Copilot Chat** in VS Code (Cmd+Shift+I on Mac, Ctrl+Shift+I on Windows/Linux)
2. **Copy the prompt** that best matches your project (Options 1-4 above)
3. **Paste into Copilot Chat** and press Enter (or modify to fit your scenario)
4. **Copilot will:**
   - Generate `specs/001-customer-service-agent/spec.md` with complete specification
   - Create user stories with priorities
   - Define acceptance criteria
   - List requirements and success metrics
   - Include glossary and edge cases
5. **Review the specification**: Understand all features before technical planning

---

#### What the Output Looks Like

After running `/speckit.specify`, you'll get a comprehensive specification similar to the one below:


### Completed Specification Example

<details>
<summary>Click to expand example</summary>

```markdown
# Feature Specification: Customer Support AI Agent

**Feature Branch**: `001-customer-support-agent`  
**Created**: January 5, 2026
**Status**: Draft  
**Input**: User description: "Build an AI agent for customer service using Microsoft Agent Framework that will be deployed to Foundry. The agent helps retail customers resolve common issues: (1) Look up order status and tracking information by customer account or order ID, (2) Check return/refund eligibility and initiate returns with automatic return labels, (3) Track refund status and provide timeline, (4) Escalate complex issues to human support with full conversation context."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Order Status Inquiry Resolution (Priority: P1)

A retail customer wants to quickly find the current status of their order and tracking information. They may have misplaced their order confirmation or need to share tracking details with others. This is the most common customer service request and directly impacts customer satisfaction and reduces support workload.

**Why this priority**: Order inquiries represent the majority of customer service requests. Automating this resolution provides immediate value by reducing support team workload by 30-40% and satisfying customer expectations for self-service.

**Independent Test**: Can be fully tested by submitting an order ID or account number and verifying that the agent returns accurate order status, estimated delivery date, and tracking information without human intervention. Delivers immediate customer satisfaction.

**Acceptance Scenarios**:

1. **Given** a customer with an active order, **When** customer provides order ID, **Then** agent returns order status (processing/shipped/delivered), carrier, tracking number, and estimated delivery date
2. **Given** a customer who doesn't remember their order ID, **When** customer provides account email/phone, **Then** agent retrieves recent orders and customer selects the one they're inquiring about
3. **Given** an order with exception status, **When** customer queries order status, **Then** agent explains the delay/issue and provides next steps (e.g., "Your order is delayed due to carrier congestion. Estimated new delivery: Jan 12")
4. **Given** a customer asking about tracking, **When** customer provides order ID, **Then** agent provides carrier name, tracking number, and link to track real-time updates

---

### User Story 2 - Return and Refund Processing (Priority: P1)

A retail customer wants to understand if their purchase is returnable and needs to initiate a return without calling support. This includes determining refund eligibility, automatically generating return labels, and establishing clear return timeline expectations.

**Why this priority**: Returns and refunds are critical to customer satisfaction and brand loyalty. Enabling customers to self-serve return initiation reduces support calls while ensuring compliance with return policies. Second-most common inquiry type.

**Independent Test**: Can be fully tested by providing an order ID, receiving eligibility determination, generating a return label, and confirming return initiation without human support. Delivers measurable reduction in refund-related support tickets.

**Acceptance Scenarios**:

1. **Given** an order within the return window, **When** customer requests to initiate return, **Then** agent confirms eligibility, explains condition requirements, and offers automatic return label generation
2. **Given** an order outside return window, **When** customer requests return, **Then** agent explains why return is not eligible but offers alternative resolutions (discount, store credit, escalation)
3. **Given** a return initiated by customer, **When** agent generates return label, **Then** customer receives shipping label (email/SMS/in-app) with return address and instructions
4. **Given** a return with special conditions (oversized item, hazardous material), **When** customer initiates return, **Then** agent explains special handling requirements and adjusted refund timeline
5. **Given** a damaged/defective product return, **When** customer describes issue, **Then** agent asks clarifying questions and may offer instant refund or replacement as alternative

---

### ... Additional User Stories ...

---

### Edge Cases

- What happens when a customer provides an incorrect order ID multiple times? Agent should offer alternative lookup methods and escalate if customer cannot verify identity.
- How does system handle orders with multiple shipments? Agent should clarify which shipment customer is asking about and provide tracking for each.
- What happens when return label generation fails? Agent should explain the issue and provide alternative (email label, print from account portal, or escalate).
- ... additional edge cases ...

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Agent MUST accept natural language customer inquiries in text format and understand intent ("Where's my order?", "How do I return this?", "Is it refunded yet?")
- **FR-002**: Agent MUST retrieve order information (status, tracking, estimated delivery) from backend order management system using customer account ID or order ID
- **FR-003**: Agent MUST verify customer identity before sharing sensitive information (order details, personal information) using account email, phone, or order ID verification
- ... additional functional requirements ...

### Key Entities

- **Customer**: Individual making the inquiry with account ID, email, phone number, identity verification status, account creation date
- **Order**: Purchase record with order ID, customer ID, order date, items, prices, shipping address, delivery address, order status, tracking information
- **Return**: Return request record with return ID, order ID, return reason, return eligibility, return label, return shipping status, inspection date
- **Refund**: Financial transaction record with refund ID, return ID, refund amount, original payment method, processing status, estimated/actual credit date
- **Conversation**: Multi-turn dialog record with customer ID, message history, context (current order/return being discussed), escalation flag

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 70% of customer inquiries are resolved without escalation to human support
- **SC-002**: First response time is under 5 seconds for 95% of inquiries
- **SC-003**: Customer satisfaction rating is ≥4.2/5.0 for agent-resolved inquiries
- ... additional success criteria ...

## Assumptions

- Backend APIs for order management, customer data, and refund processing are available and documented
- Customer data (email, phone, order history) is current and accurate in backend system
- Return policies and refund timelines are configured in backend and accessible to agent
- ... additional assumptions ...

## Out of Scope

- Visual product returns or photo upload for damage verification (requires future capability)
- Customization of return policies per customer or account tier
- Inventory management or stock availability queries
- ... additional out-of-scope items ...

---

## Acceptance Scenarios

### Scenario 1: Happy Path - Standard Return

**Setup:** Customer with order in "delivered" status

**Actions:**
1. Customer asks: "I want to return my order"
2. Agent retrieves order and checks return eligibility
3. Agent confirms customer identity
4. Agent initiates return process
5. Agent sends return shipping label

**Expected Outcome:**
- Return created successfully
- Shipping label provided
- Customer receives confirmation

**Success Metrics:**
- ✓ Process completes within 2 minutes
- ✓ Return ID is unique and retrievable
- ✓ Shipping label is correct for origin location

---

### ... Additional Acceptance Scenarios ...

---

## Non-Functional Requirements

### Performance
- **Response Time:** Agent responds within 5 seconds (p95)
- **Throughput:** Handle 1000 concurrent conversations
- **Availability:** 99.5% uptime during business hours

### Security
- **Authentication:** Verify customer identity before sharing PII
- **Data Protection:** Encrypt order data in transit and at rest
- **PII Masking:** Never expose full credit card numbers, addresses
- **Audit Trail:** Log all customer interactions for compliance

### Reliability
- **Error Recovery:** Agent gracefully handles API failures
- **Escalation Path:** Clear escalation to human if agent fails
- **State Preservation:** Conversation context preserved during escalation
- **Monitoring:** Real-time alerts for abnormal behavior

### Compliance
- **GDPR:** Comply with data access and retention rules
- **PCI-DSS:** Never store or transmit payment card data
- **Accessibility:** Agents must work with screen readers and alt access methods

---

## Clarification Markers

- [NEEDS CLARIFICATION] How do we authenticate customers in the agent interface?
- [NEEDS CLARIFICATION] What's the SLA for human escalation?
- [NEEDS CLARIFICATION] Can the agent access inventory to check stock before suggesting returns?
- [NEEDS CLARIFICATION] Should refund amounts include shipping costs?

---

## Implementation Constraints

- Must use Microsoft Agent Framework (v1.0+)
- Must be deployable to Microsoft Foundry
- Cannot integrate with unapproved third-party payment processors
- Budget: $50k/month for cloud infrastructure
- Timeline: Deliver MVP within 3 sprints
```

</details>

---

### Tips for Better Specification Prompts

✅ **DO:**
- Focus on user value and agent intent
- Use concrete examples ("Customer asks...", "Agent should...")
- Define success metrics (quantifiable: %, time, scores)
- Mention escalation scenarios
- Write as if the agent already exists
- Include who the users are (retail customers, support team)
- Mention Foundry and Agent Framework deployment context
- Specify edge cases agent should handle

❌ **AVOID:**
- Specifying implementation (Python, FastAPI, PostgreSQL)
- Architectural decisions ("use microservices", "cache results")
- Tool implementation details ("use REST API", "SQL queries")
- Assuming integrations without user need
- Vague features ("make it smart", "handle errors well")
- Focusing on technical elegance over user problems

---

### Advanced Prompt Variations for Different Scenarios
<details>
<summary>Click to expand</summary>

**Variation 1: Multi-Turn Conversational Agent**
```
/speckit.specify Build an AI customer service agent (Microsoft Agent Framework, 
Foundry) that excels at multi-turn conversations where context is critical. 
Customers should feel they're having a natural conversation, not repeating 
information. The agent: (1) Remembers what customer said in message 1 when 
they ask a follow-up in message 5, (2) Updates understanding as conversation 
evolves, (3) Proactively asks clarifying questions only when needed, (4) 
Provides follow-up suggestions based on conversation direction. Example: 
Customer: "I have a problem with my order" → Agent: "I'm here to help! What 
order are you referring to?" → Customer: "The blue shoes from last week" → 
Agent remembers "blue shoes order" for all subsequent messages. Success: 
Customers report "agent understood me" in 90%+ of interactions.
```

**Variation 2: Complaint Handling & De-Escalation**
```
/speckit.specify Build an AI agent skilled at handling upset customers 
(Microsoft Agent Framework, Foundry). Angry customers are more common in 
support than happy ones. The agent should: (1) Detect frustration/anger 
indicators in text (all caps, multiple exclamation marks, insulting language), 
(2) Respond with empathy ("I understand this is frustrating"), (3) Take 
immediate action to resolve (offer refund, expedite shipping, escalate), (4) 
Never respond defensively or match customer tone. The agent should escalate 
immediately if: Customer is extremely angry, issue requires judgment call, 
customer explicitly requests human. Success: 80% of angry customers are 
satisfied after agent interaction; escalation rate <15% for complaints.
```

**Variation 3: Omnichannel Integration**
```
/speckit.specify Build an AI customer service agent (Microsoft Agent Framework, 
Foundry) that operates across multiple channels: chat, email, SMS. When customer 
switches from chat to email, the agent has full context. The agent: (1) Accesses 
conversation history across all channels, (2) Remembers customer context 
regardless of channel, (3) Offers seamless handoff to human on any channel, (4) 
Provides consistent responses across channels. Success: Customers can start on 
chat, continue on email, finish on SMS without repeating themselves.
```
</details>

---

## 🎓 Module 2 Quiz

Answer these 5 questions to validate your learning.

### Question 1: User Story Independence with Agents

**Scenario**: You're specifying a customer service agent. You've written:
- User Story 1: "Agent can look up customer order status"
- User Story 2: "Agent can escalate to human support"

Your team asks: "Can we implement User Story 2 before User Story 1?"

**Question**: Is User Story 2 independent (can it be implemented standalone)? Why or why not?

**Options**:
- A) Yes, they are completely independent
- B) No, Story 2 depends on Story 1
- C) Partially independent—escalation works but without order context

- B) No, User Story 2 depends on User Story 1
- C) No, User Story 2 requires both User Story 1 and 3

---

### Question 2: Acceptance Criteria Quality

**Scenario**: A team member proposes this acceptance criterion:

"Given a customer has an order, When they ask about it, Then the agent responds quickly"

**Question**: What's wrong with this criterion? Rewrite it to be better.

**Hint**: Check the "Good Acceptance Criteria" section above.

---

### Question 3: Specification vs. Technical Plan

**Scenario**: You're reviewing a specification and you see:

"The agent will use a FastAPI endpoint at `/api/orders` to retrieve customer orders via REST calls"

**Question**: Is this appropriate for a specification? Why or why not? Where should this content go instead?

---

### Question 4: User Story Priority Justification

**Scenario**: In our customer service spec, we prioritized "Order Status Inquiry" as P1 (MVP-critical).

**Question**: What evidence from the specification justifies this P1 priority?

---

### Question 5: Edge Cases

**Scenario**: In our specification, we listed edge cases like "What happens when customer order doesn't exist?"

**Question**: Why is it important to identify edge cases in the specification phase (before technical plan or implementation)?

---

## ✅ Module 2 Quiz: Worked Solutions

### Solution 1: User Story Independence

**Correct Answer**: A) Yes, they are completely independent

**Reasoning**:
- User Story 2 (escalation) can be fully implemented and tested independently
- You can create a support ticket escalation system without order status lookup
- The stories might be used together in practice, but that's orchestration (how they work together), not dependency
- In Spec-Driven Development, independent stories enable parallel development—teams can work on Story 1 and Story 2 simultaneously

**Key Insight**: Independence is crucial for Spec-Kit. The `/speckit.tasks` command uses story independence to identify parallelizable work, speeding up development.

---

### Solution 2: Acceptance Criteria Quality

**Original**: "When they ask about it, Then the agent responds quickly"

**Issues**:
- "Responds quickly" is unmeasurable (fast = <1s? <5s? <1m?)
- No verification method specified
- Vague about what a successful response looks like

**Better Version**:
"When they ask about order #12345, Then the agent responds within 5 seconds with: (1) order status, (2) tracking number, (3) estimated delivery date"

**Why Better**:
- ✅ Measurable: "within 5 seconds" is objective
- ✅ Testable: Can verify by calling agent with order ID
- ✅ Complete: Specifies exactly what data should be returned
- ✅ Clear: No ambiguity about success

---

### Solution 3: Specification vs. Technical Plan

**Is it appropriate for specification?**: NO

**Why**:
- Specifying HOW to implement violates SDD principles
- Saying "use FastAPI endpoint at `/api/orders`" is a technical decision, not a requirement
- Specification should say WHAT: "System can retrieve customer orders"
- Technical plan should say HOW: "Use FastAPI endpoint at `/api/orders` with REST calls"

**Better Specification Language**:
"The system can retrieve customer order data including status, items, and tracking information"

**Where it goes**: In the Technical Plan (`specs/001-customer-service-agent/plan.md`), which comes in Module 3.

**Key Insight**: This is a critical SDD distinction. Mixing specification and implementation causes specs to become outdated when technology choices change.

---

### Solution 4: User Story Priority Justification

**Evidence from specification**:
- Introduction states: "40% of all inquiries" are order status questions
- Success criteria state: "Handling this alone cuts support workload by 30%"
- Specification notes: "Essential for MVP"
- MVP definition relies on this story

**Why P1**:
1. **Highest Volume**: 40% of incoming queries
2. **Highest Impact**: Solving this provides 30% support reduction
3. **Business Critical**: Must be in MVP to achieve business goals
4. **Independent Value**: Delivers value even without other stories

**Non-P1 stories** (like Proactive Suggestions/P2):
- Lower volume (covered by P1 interactions)
- Nice-to-have, not essential
- Can be added post-MVP

---

### Solution 5: Why Edge Cases Matter in Specification

**Why identify edge cases in specification phase**:

1. **Prevents Surprises**: Discovering edge cases during code makes fixes expensive; in specs, they're free to address
2. **Informs Tool Design**: Edge cases affect what tools and data we need (e.g., "handle >90 days old orders" → need return policy tool)
3. **Enables Complete Testing**: Acceptance scenarios should cover edge cases; if edge cases aren't in spec, tests won't cover them
4. **Impacts Architecture**: Some edge cases require architectural decisions (e.g., "payment system down" → need fallback behavior in agent)
5. **Cost Efficiency**: Addressing edge cases in specs costs 1-2 hours; discovering them in code or production costs 10-100x more

**Example**:
- Edge case in spec: "What happens if order is >90 days old?"
- This edge case → informs return policy tool design
- Return policy tool → informs agent's refund offering logic
- Agent logic → informs testing scenarios
- By identifying upfront, we ensure complete implementation

---

## 📝 Next Steps

**Before moving to Module 3:**

1. ✅ **Complete the Hands-on Exercise**:
   
2. ✅ **Verify specification and review user stories**:
   
3. ✅ **Complete Module 2 quiz** and verify your understanding

4. ✅ **Get ready for Module 3:**    
   In Module 3, you'll create a technical implementation plan based on your specification using the `/speckit.plan` command.
   - Create a technical plan choosing Microsoft Agent Framework, Python, FastAPI, Vite
   - Define tool contracts and data models
   - Create API endpoint specifications
   
---

## 📚 Module 2 Resources

- **Microsoft Agent Framework**: https://learn.microsoft.com/en-us/agent-framework/
- **Microsoft Foundry Documentation**: https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry?view=foundry
- **Spec-Kit GitHub**: https://github.com/github/spec-kit
- **Spec-Driven Development Guide**: https://github.com/github/spec-kit/blob/main/spec-driven.md
- **Your Generated Specification**: `specs/001-customer-service-agent/spec.md`

---

## ✅ Module 2 Deliverables Checklist

Before moving to Module 3, verify you have completed:

- [ ] ✅ Reviewed real-world customer service scenario
- [ ] ✅ Generated specification using `/speckit.specify` command
- [ ] ✅ Reviewed and understood your specification
- [ ] ✅ Verified specification includes user stories, requirements, success criteria
- [ ] ✅ Completed Module 2 quiz

**All items checked?** → **Ready for Module 3: Technical Planning with `/speckit.plan`**

---

**Module 2 Status**: ✅ COMPLETE

**Next Step**: Module 3 will guide you through creating a technical implementation plan using `/speckit.plan`, including tool contracts, data models, and API specifications!

||||
|-|-|-|
| [Module 1: Foundations](./MODULE_1_FOUNDATIONS.md) ←  | 📍 Module 2: Specification |  → [Module 3: Planning](./MODULE_3_PLANNING.md) |