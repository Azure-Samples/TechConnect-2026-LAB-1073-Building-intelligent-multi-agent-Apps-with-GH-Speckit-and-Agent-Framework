# Module 1: Lab Foundations, Spec-Kit Basics & Agentic AI Fundamentals

**Estimated Duration**: 10 minutes  
**Prerequisites**: Python 3.11+, Git, terminal experience  
**Deliverable**: Initialized spec-kit project with lab constitution

---

## 🎯 Learning Objectives

By the end of this module, you will:

1. **Understand core agentic AI concepts:** agents, tools, orchestration, and state management
2. Understand the core principles of **Spec-Driven Development (SDD)** and why it's essential for agentic AI applications
3. Learn how to **design AI multi-agent** systems using the Microsoft Agent Framework and Foundry platform 
4. Successfully initialize a **spec-kit** project using the CLI
5. Navigate the **spec-kit workflow**: Constitution → Specification → Plan → Tasks → Implementation

---


## 📚 Section 1: Agentic AI Fundamentals

### 1.1 What is an Agent?

An **AI Agent** is an autonomous software component that:
- **Receives goals or intents** from users or systems
- **Decides which actions to take** using internal reasoning
- **Executes actions** through a set of available tools
- **Adapts behavior** based on outcomes and feedback

#### Key Difference: Agents vs. Traditional Code

| Aspect | Traditional Code | Agent |
|--------|-----------------|-------|
| **Control Flow** | Predefined (if-then-else) | Dynamic (reasoning-based) |
| **Decision Making** | Hardcoded logic | LLM-powered reasoning |
| **Tool Selection** | Developer chooses | Agent chooses based on intent |
| **Adaptability** | Requires code changes | Adapts through reasoning |

#### Example: Customer Support Agent

```
User: "I want to return my order from last week."

Agent's Decision Process:
1. Recognize intent: "Order return request"
2. Select tools: Fetch order history, check return policy, initiate return
3. Execute: "I found your order #12345. It's eligible for return. I've initiated the process."
```

#### Key Concepts

##### 1. Agents
A wrapper around an LLM (Language Model) that can:
- Receive instructions (system prompts)
- Access a set of tools
- Make autonomous decisions
- Maintain conversation history and state
- Execute multi-step reasoning

**In Microsoft Agent Framework**, agents are built using:
- **Chat Clients**: LLM access (OpenAI, Azure OpenAI, GitHub Models)
- **Agent Orchestrators**: Manage agent lifecycle, tool calling, state
- **Threads**: Persistent conversation context across multiple turns

##### 2. Tools

Capabilities (Functions/APIs) the agent can invoke to achieve intents. Each tool has:
- **Name:** Descriptive identifier (e.g., `create_task`, `search_knowledge_base`)
- **Description:** Human-readable purpose, what the tool does (helps agent decide when to use it)
- **Parameters:** Input schema (what data the tool needs)
- **Returns:** Output structure and format

**Example Tool for Customer Service Agent:**
```
Name: lookup_customer_account
Description: "Retrieve customer account details including name, email, order history, and support tickets"
Parameters: {customer_id: string, include_orders: boolean}
Returns: {customer_id, name, email, status, recent_orders[], open_tickets[]}
```

##### 3. Orchestration
The logic that governs:
- **Tool selection:** Which tools to invoke based on intent
- **Sequencing:** Order of tool calls (e.g., fetch calendar → check policy → create event)
- **Error handling:** What to do if a tool fails
- **Termination:** When the agent has completed the task

**For our customer service app**, we'll use **sequential orchestration**:
1. User sends message → Customer Service Agent
2. Agent analyzes intent
3. Agent selects and calls appropriate tools
4. Agent synthesizes results
5. Agent responds to customer


##### 4. State Management
Persistent context that the agent maintains:
- **Conversation History**: Previous messages and agent decisions
- **Tool Results**: Outputs from function calls
- **User Context**: Customer info, session data
- **Agent Memory**: Learned patterns from conversation


##### 5. Agent Lifecycle (One Turn)

```
User Input
    ↓
Agent reads input & conversation history
    ↓
Agent reasons: "What tool(s) do I need?"
    ↓
Agent calls selected tool(s) with parameters
    ↓
Tool executes, returns results
    ↓
Agent reads tool results
    ↓
Agent decides: "Do I need more info?"
    Yes → Loop back (call another tool)
    No → Generate response to user
    ↓
Agent returns response to user
    ↓
Response added to conversation history
```


### 1.2 Microsoft Agent Framework Overview

#### What is the Microsoft Agent Framework?

The **[Microsoft Agent Framework](https://github.com/microsoft/agent-framework)** is a comprehensive SDK for building, orchestrating, and deploying AI agents. It provides:

- **Flexible Agent Building**: Create agents with different backends (Azure OpenAI, Microsoft Foundry, OpenAI)
- **Multi-Agent Orchestration**: Build complex workflows combining multiple agents
- **Function Calling**: Extend agents with external tools and APIs
- **Conversation Persistence**: Maintain context across interactions using threads
- **Human-in-the-Loop**: Require approval for sensitive operations
- **Cross-Platform Support**: Available for .NET and Python

#### Agent Framework Architecture

```
┌──────────────────────────────────────────────────┐
│      Microsoft Agent Framework                   │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────────────────────────────────────┐     │
│  │  Agent Types                            │     │
│  │  • ChatAgent (Core)                     │     │
│  │  • Azure OpenAI ChatCompletion          │     │
│  │  • Microsoft Foundry Agents             │     │
│  │  • Custom Agents                        │     │
│  └─────────────────────────────────────────┘     │
│                                                  │
│  ┌─────────────────────────────────────────┐     │
│  │  Workflow Orchestration                 │     │
│  │  • Sequential (one after another)       │     │
│  │  • Concurrent (parallel processing)     │     │
│  │  • Handoff (specialized routing)        │     │
│  │  • Magentic (advanced group chat)       │     │
│  └─────────────────────────────────────────┘     │
│                                                  │
│  ┌─────────────────────────────────────────┐     │
│  │  Core Features                          │     │
│  │  • Function Tools (external integration)│     │
│  │  • Multi-turn Conversations (threads)   │     │
│  │  • Structured Output (JSON schema)      │     │
│  │  • Tool Approval (human gates)          │     │
│  │  • Memory & Persistence                 │     │
│  └─────────────────────────────────────────┘     │
│                                                  │
└──────────────────────────────────────────────────┘
```

#### Key Concepts

##### **Agents**
Self-contained decision-making units that can:
- Understand natural language
- Call tools to take action
- Make decisions based on context
- Maintain conversation state

##### **Workflows**
Orchestration patterns that coordinate multiple agents:
- **Sequential**: Tasks execute one after another with shared context
- **Concurrent**: Multiple agents work in parallel, then results are combined
- **Handoff**: Dynamic routing between agents based on requirements
- **Magentic**: Advanced multi-agent group discussion with a manager

##### **Tools (Function Calling)**
External capabilities agents can invoke:
```python
@ai_function(name="get_order_status")
def get_order_status(order_id: str) -> str:
    """Get the current status of an order"""
    return fetch_order_from_database(order_id)
```

##### **Threads**
Persistent conversation contexts that:
- Maintain message history
- Preserve context across interactions
- Enable multi-turn conversations
- Support resuming paused interactions

---

### 1.3 Microsoft Foundry for AI Agents

#### What is Microsoft Foundry?

**Microsoft Foundry** (formerly Azure AI Foundry) is Microsoft's comprehensive AI platform that provides:

1. **Unified AI Models Catalog**
   - Access to cutting-edge models: Phi, GPT-4o, Llama, Mistral, etc.
   - Deploy models on Azure infrastructure
   - Pay-per-token pricing

2. **Agent Services**
   - Service-managed agent persistence
   - Conversation thread management
   - Built-in safety and compliance
   - Scalable infrastructure

3. **Development Environment**
   - AI playground for testing
   - Prompt optimization tools
   - Evaluation frameworks
   - Monitoring and observability

#### Why Use Foundry for Agentic AI Systems?

| Requirement | Foundry Benefit |
|-------------|-----------------|
| **Scalability** | Handles millions of concurrent conversations |
| **Reliability** | 99.9% SLA with automatic failover |
| **Security** | Enterprise-grade encryption and compliance |
| **Cost Efficiency** | Pay only for tokens used, no idle charges |
| **Model Choice** | Select from multiple high-performing models |
| **Integration** | Seamless integration with Azure ecosystem |


Foundry Agents provide features necessary for building robust agentic AI systems, including:

```
Microsoft Foundry Agent
├── Conversation Management
│   ├── Service-managed threads
│   ├── Automatic state persistence
│   └── Long-context support
├── Safety & Compliance
│   ├── Content filtering
│   ├── Audit logging
│   └── Data residency compliance
└── Integration Points
    ├── Function calling for tools
    ├── Knowledge base integration
    └── Custom skill deployment
```


---

<!-- Section 2 -->

## 📚 Section 2: What is Spec-Driven Development?

### 2.1 The Traditional vs. Spec-Driven Approach

**Traditional Development (Waterfall/Agile Hybrid)**:
- Specification → Design → Code → Test → Deploy
- Specs are created, then set aside; code becomes source of truth
- Gap between intent and implementation grows over time
- Changes require manual propagation through docs and code

**Spec-Driven Development (SDD)**:
- Constitution → Specification → Technical Plan → Task List → Code Generation
- **Specifications ARE the source of truth**; code is the generated output
- AI (like Claude, GitHub Copilot) understands specs and generates implementation automatically
- Changes to specs automatically regenerate affected plans and code
- Specs and code stay perfectly aligned

### 2.2 Why SDD Matters for Agentic AI

Agentic AI applications are uniquely suited to SDD because:

1. **Intent-Driven Architecture**: Agents execute actions based on explicit intents. SDD forces you to define intents clearly before building tool orchestration.
2. **Tool Composition**: Agentic systems require well-defined tool contracts. SDD generates these contracts from specifications.
3. **Testability**: Agents need extensive testing. SDD generates test scenarios from acceptance criteria.
4. **Reproducibility:** The same specification should generate the same agent behavior
5. **Maintenance:** Updating agent behavior means evolving specifications, not debugging code

### 2.3 The Spec-Driven Workflow

1. **Specification** (This module's focus: Constitution)
   - Define principles, constraints, and governance
   - Answer: *What are our non-negotiable rules?*

2. **Intent Specification** (Module 2)
   - Define specific user intents and acceptance criteria
   - Answer: *What do users need the agent to do?*

3. **Technical Plan** (Module 3)
   - Translate intents into agent architecture
   - Answer: *How will we build the agent to satisfy these intents?*

4. **Implementation** (Module 4)
   - Write code that satisfies the technical plan
   - Answer: *How do we code this design?*

5. **Deployment & Validation** (Module 5)
   - Deploy to Foundry, monitor, iterate
   - Answer: *Does the agent work in production?*

---

## 📚 Section 3: Introduction to Spec-Kit

### 3.1 What is Spec-Kit?

**Spec-Kit** is an open-source framework (GitHub: [github.com/github/spec-kit](https://github.com/github/spec-kit)) that automates the SDD workflow:

- **CLI Tool** (`specify` command): Initializes projects, creates feature branches
- **Templates**: Guide specification, planning, task creation
- **Slash Commands** (in AI agents): Semi-automate SDD steps
  - `/speckit.constitution` - Create project principles
  - `/speckit.specify` - Create feature specifications
  - `/speckit.plan` - Generate technical implementation plans
  - `/speckit.tasks` - Break down into executable tasks
  - `/speckit.implement` - Execute tasks and build

### 3.2 Spec-Kit File Structure

```
project-root/
├── .specify/                  # Spec-Kit configuration
│   ├── memory/
│   │   └── constitution.md    # Project governance & principles
│   ├── templates/             # Template files for specs, plans, tasks
│   └── scripts/               # Automation scripts
├── specs/                     # Feature specifications (versioned)
│   ├── 001-feature-name/
│   │   ├── spec.md           # Feature specification
│   │   ├── plan.md           # Technical implementation plan
│   │   ├── tasks.md          # Task list
│   │   ├── data-model.md     # Data structures
│   │   ├── contracts/        # API contracts, tool definitions
│   │   └── research.md       # Research notes
│   └── 002-another-feature/
└── [source code directories]
```
---

## 🔧 Hands-On: Setting Up Your Lab Environment

### Step 1: Verify Prerequisites

```bash
# Check Python version (must be 3.11+)
python3 --version

# Check Git is installed
git --version

# Check if uv package manager is installed (we'll install if needed)
uv --version
```

**Expected Output Examples:**
```
Python 3.11.7
git version 2.46.0
uv 0.4.29
```

If `uv` is not installed:
```bash
# Install uv (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Install Spec-Kit

Spec-Kit is the framework for specification-driven development. Install it using UV:

```bash
# Install Spec-Kit via uv
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Verify installation
specify --version
```

**Expected Output:**
```
Spec-Kit CLI version 1.x.x
```

### Step 3: Initialize the Lab Project

We already initialized the project with `specify init .` in the setup. Let's verify it's ready:

```bash
git clone https://www.github.com/AZURE-SAMPLES/TechConnect-2026-Lab-1073.git ./TechConnect-2026-LAB-1073

cd ./TechConnect-2026-LAB-1073

# List the spec-kit structure
ls -la .specify/

# Check constitution exists
cat .specify/memory/constitution.md | head -20
```

**Expected Output**: You should see the constitution file.

### Step 4: Review the Lab Constitution

**View the constitution**:
```bash
cat .specify/memory/constitution.md
```

**Key takeaways from the constitution**:  
TODO: update from the lab constitution

| Principle | Meaning for This Lab |
|-----------|---------------------|
| **I. Spec-Driven Development Foundation** | Specs are executable blueprints; code is generated output |
| **II. Intent-First Architecture** | Every agent capability tied to clear user intent |
| **III. Foundry-Native Deployment** | All artifacts must work in Microsoft Foundry |
| **IV. Clear, Simple Learning Path** | Each module is 60–90 min; builds on prior output |
| **V. Quiz-Driven Validation** | Knowledge validated through practical quizzes |

### Step 4: Understand Your Project Structure

**Review the project structure**:

Expected Structure (after initialization):
```
LAB-1073/
├── .specify/                 # Spec-Kit infrastructure
│   ├── memory/
│   │   └── constitution.md   # Lab governance (what you just reviewed)
│   ├── templates/            # Specification & planning templates
│   └── scripts/              # Automation scripts
├── docs/
│   └── modules/              # Lab module files (including this file!)
├── .github/
│   └── prompts/              # AI agent prompts for slash commands
└── .git/                      # Version control

```

### Step 5: Create Your First Spec-Kit Branch

We'll create a branch for our customer service agent application:

```bash
cd ./TechConnect-2026-LAB-1073

# Create and check out a feature branch
git checkout -b customer-service-agent

# Verify branch created
git branch -a
```

**Expected Output**:
```
* customer-service-agent
  main
```

### Step 6: Initialize the Specs Directory

```bash
# Create the specs directory structure for our feature
mkdir -p specs/customer-service-agent

# Verify
ls -la specs/
```

---

## 🎓 Module 1 Quiz

Answer the following 5 questions to validate your understanding. Complete worked solutions are provided below.

### Question 1: Specification as Source of Truth

**Scenario**: Your team has built a customer service agent. Three months later, you realize the agent should also handle refund requests. A traditional development team would:
- A) Update the code to add refund handling
- B) Create a design document, then update code and tests
- C) Update the specification, then regenerate code and tests automatically

**Question**: In Spec-Driven Development, which approach is correct? Why?

### Question 2: Agent Tools and Intent

**Scenario**: You're designing a customer service agent. The customer wants the agent to "help customers with their orders."

Which of the following is the BEST way to decompose this intent into tools using the Agent Framework?

- A) One tool: `customer_service()` that does everything
- B) Multiple tools:
  - `lookup_order_status(order_id)` - Get order tracking info
  - `initiate_return(order_id, reason)` - Start return process
  - `check_refund_status(order_id)` - Check refund progress
- C) Tools that directly mirror database tables: `get_orders()`, `get_customers()`, `get_transactions()`

**Question**: Which approach is correct for an agentic system? Why?

### Question 3: Spec-Kit Workflow Sequence

**Scenario**: You're starting a new feature in a spec-kit project.

Which of the following sequences is CORRECT?

- A) Constitution → Specification → Technical Plan → Task List → Code
- B) Specification → Task List → Constitution → Technical Plan → Code
- C) Task List → Code → Specification → Technical Plan → Constitution

**Question**: What is the correct order? Why does order matter?

### Question 4: Microsoft Foundry Deployment Principle

**Scenario**: Your team has built a Python agent using the Microsoft Agent Framework. One developer suggests using a custom async library to make the agent faster. However, this library is not supported by Microsoft Foundry's agent runtime.

According to the lab constitution's Principle III (Foundry-Native Deployment), what should you do?

- A) Use the custom library; performance is more important
- B) Don't use the custom library; all artifacts must be Foundry-compatible
- C) Use it in development, then replace it before deployment

**Question**: What does the constitution require?

### Question 5: Agentic AI Orchestration

**Scenario**: You have a customer service agent with these tools:
- `lookup_customer()` - Get customer details
- `search_orders()` - Find customer orders
- `create_support_ticket()` - Open a support case
- `send_email()` - Send email to customer

A customer asks: "I can't find my order from last week. Can you help?"

The agent executes the following steps:
1. Call `lookup_customer()` with customer ID
2. Call `search_orders()` with customer ID
3. Call `create_support_ticket()` with order details
4. Call `send_email()` with ticket confirmation

**Question**: Is this orchestration correct? If not, what's missing?

---

## ✅ Module 1 Quiz: Worked Solutions

### Solution 1: Specification as Source of Truth

**Correct Answer**: C) Update the specification, then regenerate code and tests automatically

**Reasoning**:
- In Spec-Driven Development, specifications ARE the source of truth
- Code is the generated output of specifications
- When requirements change, you update the specification
- The technical plan and code are regenerated from the updated spec
- This ensures spec and code stay perfectly aligned
- Eliminates the gap between intent and implementation that grows over time in traditional development

**Key Insight**: This is the central power of SDD—changes are fast and eliminate manual propagation errors.

---

### Solution 2: Agent Tools and Intent

**Correct Answer**: B) Multiple tools with specific purposes

**Reasoning**:
- A) A single `customer_service()` tool is too vague; agent can't reason about what it does or when to use it
- B) CORRECT—Each tool has a specific purpose, description, and parameters. Agent can reason: "Customer asked about order status? Use `lookup_order_status()`. Wants to return? Use `initiate_return()`."
- C) Database tools are too low-level; agent doesn't need to know about database structure

**Why this matters**:
- Clear, specific tools help agents make better decisions
- Tool descriptions enable agent reasoning ("When should I call this?")
- Encapsulation means agent doesn't need database knowledge
- This aligns with Principle II: Intent-First Architecture—define intents first (help customers), then select tools

**Key Insight**: Tool design is crucial; it directly affects agent reasoning quality.

---

### Solution 3: Spec-Kit Workflow Sequence

**Correct Answer**: A) Constitution → Specification → Technical Plan → Task List → Code

**Reasoning**:
1. **Constitution** first: Establish governance and principles that guide all future work
2. **Specification** next: Define WHAT to build (user needs, acceptance criteria) before HOW
3. **Technical Plan** next: Decide HOW to build it (tech stack, architecture)
4. **Task List** next: Break plan into executable tasks
5. **Code** last: Generate/write code to implement tasks

**Why order matters**:
- Constitution provides guardrails for all decisions
- Specifications ensure you're building the right thing
- Plans ensure you're building it right (technically sound)
- Tasks ensure you build it systematically
- Code is the final expression of all the above

**Skipping steps causes problems**:
- No constitution → inconsistent quality, over-engineering, abandoned principles
- No specification → building wrong thing, rework
- No plan → technical debt, architectural issues
- No tasks → chaotic implementation, missed dependencies

**Key Insight**: The order embodies the principle "intent before implementation."

---

### Solution 4: Foundry-Native Deployment

**Correct Answer**: B) Don't use the custom library; all artifacts must be Foundry-compatible

**Reasoning**:
- Principle III: "All developed artifacts MUST be deployable to Microsoft Foundry"
- This is NON-NEGOTIABLE in the lab constitution
- Using an unsupported library violates this principle
- A faster agent that can't be deployed is worthless
- Foundry compatibility is a hard constraint, not a preference

**What to do instead**:
- Use libraries supported by Foundry's agent runtime
- If performance is critical, optimize within Foundry's constraints
- Explore other Foundry-approved approaches for performance gains

**Key Insight**: Principles from the constitution are immutable constraints; they drive all technical decisions.

---

### Solution 5: Agentic AI Orchestration

**Correct Answer**: No, this is NOT correct orchestration. The agent is missing a reasoning step.

**Issues**:
1. Agent looked up customer (step 1) ✓ Correct
2. Agent searched orders (step 2) ✓ Correct
3. Agent created support ticket (step 3) ✗ PROBLEM: Agent should first check if the order exists or if the customer is confused
4. Agent sent confirmation email (step 4) ✓ Would be correct if step 3 is valid

**Better orchestration**:
1. Call `lookup_customer()` with customer ID
2. Call `search_orders()` with customer ID and filter for last week
3. **REASONING STEP**: Agent reads order details
   - If order found: Continue
   - If order not found: Ask customer for clarification instead of escalating
4. Only if customer still needs help: Call `create_support_ticket()`
5. Call `send_email()` with confirmation

**Key Insight**: Agent orchestration requires decision points where the agent reasons about tool results, not just blindly executing a sequence. This is where agent intelligence emerges—making decisions based on context and tool results.

---

## 📝 Next Steps

**Before moving to Module 2:**

1. ✅ Verify your spec-kit project is initialized:
   ```bash
   ls -la .specify/memory/constitution.md
   ```

2. ✅ Confirm you're on the correct branch:
   ```bash
   git branch
   # Should show: * customer-service-agent
   ```

3. ✅ Complete Module 1 quiz and verify your understanding

4. ✅ Understand the customer service scenario we'll build in Module 2:
   - **User**: Support customer with order/refund questions
   - **Agent**: Handles common inquiries autonomously, escalates when needed
   - **Tools**: Order lookup, return initiation, ticket creation
   - **Frontend**: Vite + React chat interface
   - **Backend**: Python FastAPI agents
   - **Deployment**: Microsoft Foundry

---

## 📚 Spec-Kit Commands Reference

This section provides a quick reference for Spec-Kit slash commands you'll use throughout the lab. For complete documentation, see the [Spec-Kit GitHub Repository](https://github.com/github/spec-kit).

### Core Commands Summary

| Command | Purpose | When to Use | Output |
|---------|---------|-----------|--------|
| `/speckit.constitution` | Define project principles and governance | At project start; defines values guiding all decisions | `.specify/memory/constitution.md` |
| `/speckit.specify` | Define requirements and user stories | After constitution; describes WHAT to build (not HOW) | `specs/001-feature/spec.md` |
| `/speckit.plan` | Create technical implementation plan | After specification clarified; describes HOW to build it | `specs/001-feature/plan.md` |
| `/speckit.tasks` | Break plan into executable tasks | After plan approved; lists all implementation work | `specs/001-feature/tasks.md` |
| `/speckit.implement` | Execute all tasks and build feature | After tasks reviewed; generates/writes the code | Working implementation in `backend/`, `frontend/`, etc. |

### Optional Validation Commands

| Command | Purpose | When to Use |
|---------|---------|-----------|
| `/speckit.clarify` | Clarify underspecified areas | Before `/speckit.plan`; ask Claude to highlight ambiguities |
| `/speckit.analyze` | Check consistency across artifacts | After `/speckit.tasks`; ensure spec/plan/tasks align |
| `/speckit.checklist` | Generate custom quality checklists | Before `/speckit.implement`; validate completeness |

### Getting Started with Each Command

#### Using `/speckit.constitution`

**Basic Command Structure:**
```
/speckit.constitution [Your project description and core values]
```

**What to include in your prompt:**
- Project type and domain
- Core values (3-5 most important)
- Quality standards
- Deployment/platform constraints
- Team culture preferences

**Example:**
```
/speckit.constitution Create a constitution for a retail customer service AI agent. 
Core values: reliability, simplicity, transparency. Quality standards: all tools have 
clear contracts, comprehensive testing, code reviews required. Platform: Microsoft 
Foundry deployment. Team: collaborative spec-first development.
```

**Output Files Created:**
- `.specify/memory/constitution.md` - Your project's governing principles

---

#### Using `/speckit.specify`

**Basic Command Structure:**
```
/speckit.specify [Describe what users need and how they'll use it]
```

**What to include in your prompt:**
- Who your users are
- What problem they're solving
- Desired outcomes (not technology)
- User stories or key scenarios
- Acceptance criteria
- Edge cases or constraints

**Example:**
```
/speckit.specify Build an AI customer service agent that helps customers resolve 
order and refund issues. Users are retail customers who want fast answers without 
phone queues. The agent should look up order history, check return eligibility, 
and provide clear next steps. Success metrics: 80% of issues resolved in under 
2 minutes without escalation.
```

**Output Files Created:**
- `specs/001-customer-service-agent/spec.md` - Your feature specification

---

### Comparing Command Outputs

**Constitution** focuses on **Principles & Governance:**
```
Core Principle I: Specification is Source of Truth
Core Principle II: Intent-First Architecture
Core Principle III: Microsoft Foundry Compatibility
...
```

**Specification** focuses on **User Needs & Features:**
```
User Stories:
- As a customer, I want to look up my order so that...
- As a customer, I want to initiate a return so that...

Acceptance Criteria:
1. Orders retrieved within 2 seconds
2. Return eligibility checked against policy
...
```

**Plan** focuses on **Technical Decisions:**
```
Technology Stack:
- Backend: Python with FastAPI
- Database: PostgreSQL
- Agent Framework: Microsoft Agent Framework
- Frontend: React with Vite

Architecture:
- Customer Service Agent (orchestrator)
- Tool: lookup_order_status()
- Tool: check_return_eligibility()
...
```

**Tasks** focuses on **Implementation Steps:**
```
Phase 1: Foundation (Days 1-2)
- Task 1.1: Set up FastAPI backend project
- Task 1.2: Create database schema
- Task 1.3: Implement database connection

Phase 2: Agent Tools (Days 3-4)
- Task 2.1: Build lookup_order_status() tool
- Task 2.2: Build check_return_eligibility() tool
...
```

### Testing Multiple Variations

Spec-Kit is flexible—you can test multiple approaches using different prompts. Here's a testing workflow:

#### Test 1: Create Constitution, Review, Iterate

```
# First attempt
/speckit.constitution Create a simple constitution for a customer service chatbot...

# (Review the output)

# If unsatisfied, try again with a different approach:
/speckit.constitution Create a constitution emphasizing security and compliance 
for financial transaction handling...
```

#### Test 2: Create Multiple Specifications

You can generate multiple specifications in different branches:

```bash
# In your project, create test branches
git checkout -b spec-test-1
# (Generate /speckit.specify for approach 1)

git checkout -b spec-test-2
# (Generate /speckit.specify for approach 2)

# Compare the two specs and pick the best
git checkout -b spec-test-3
# (Generate /speckit.specify for a hybrid approach)
```

#### Test 3: Use `/speckit.clarify` Before Planning

```
# After specification is draft, clarify ambiguities:
/speckit.clarify Please review the current specification and identify any 
underspecified areas. Highlight where more detail is needed before we can create 
a technical plan.

# Claude will ask questions like:
# - How many concurrent users?
# - What's the acceptable response latency?
# - Should the agent maintain conversation history across sessions?
```

---

## 🆘 Troubleshooting

### Spec-Kit Command Issues

#### Issue: Slash commands not available in Claude Code

**Symptoms**: Typing `/speckit.constitution` doesn't trigger autocomplete or command

**Solution**:
1. Verify you're in the project root directory:
   ```bash
   pwd
   # Should output: /Users/nadeemis/Projects/LAB-1073
   ```

2. Verify `.specify/` folder exists:
   ```bash
   ls -la .specify/
   # Should show: memory/, templates/, scripts/
   ```

3. Close and reopen Claude Code:
   ```bash
   # Close VS Code completely
   # Reopen the project
   code .
   ```

4. Make sure you're using a supported AI agent (Claude, Copilot, Cursor, etc.):
   - Check [Spec-Kit supported agents](https://github.com/github/spec-kit#-supported-ai-agents)
   - Ensure your agent is properly configured in VS Code

#### Issue: `/speckit.constitution` runs but output is too generic

**Symptoms**: Generated constitution lacks specificity for your project

**Solution**: Your prompt was too vague. Revise with more detail:

**Before (too generic):**
```
/speckit.constitution Create a constitution for an AI project
```

**After (specific):**
```
/speckit.constitution Create a constitution for a healthcare provider AI that 
handles patient appointment scheduling. Core values: data privacy (HIPAA 
compliance), reliability (uptime critical), user-friendliness (non-technical 
staff). Quality standards: all patient data encrypted, audit trails for all 
access, testing required before any production deployment.
```

#### Issue: `/speckit.specify` doesn't capture my feature completely

**Symptoms**: Generated spec misses important features or edge cases

**Solution**: Use `/speckit.clarify` to fill gaps:

```
/speckit.clarify Please review our specification and identify:
1. What user scenarios are not covered?
2. What edge cases should we handle?
3. What acceptance criteria are missing or unclear?
4. What integrations with other systems are needed?
```

#### Issue: Spec-Kit generated files in wrong location

**Symptoms**: Constitution created in wrong folder; specification created outside `specs/`

**Solution**: Manually organize files:

```bash
# If files are in wrong place, move them
mkdir -p specs/001-customer-service-agent
mv constitution.md .specify/memory/constitution.md
mv spec.md specs/001-customer-service-agent/spec.md

# Verify structure
ls -R specs/
ls -R .specify/
```



### General Setup Issues

#### Issue: `specify init` command not found

**Solution**:
```bash
# Install Specify CLI (one-time setup)
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Verify installation
specify --version

# Should output something like: specify-cli 0.0.90
```

#### Issue: Python version is 3.10 or lower

**Symptoms**: `specify` commands fail with Python version error

**Solution**: Spec-Kit requires Python 3.11+. Install Python 3.11:
```bash
# Using Homebrew (macOS)
brew install python@3.11

# Verify
python3.11 --version

# Set as default (optional, adjust to your setup)
alias python3=/usr/local/bin/python3.11
```

#### Issue: Git branch creation failed

**Solution**:
```bash
# Ensure you're in the project directory
cd /Users/nadeemis/Projects/LAB-1073

# Check git status
git status

# Create branch manually if needed
git checkout -b 001-customer-service-agent

# Verify branch
git branch
```

---

## 📚 Additional Resources

- **Spec-Kit GitHub Repository**: https://github.com/github/spec-kit
- **Spec-Driven Development Methodology**: https://github.com/github/spec-kit/blob/main/spec-driven.md
- **Spec-Kit CLI Reference**: https://github.com/github/spec-kit#-specify-cli-reference
- **Supported AI Agents**: https://github.com/github/spec-kit#-supported-ai-agents
- **Microsoft Agent Framework Overview**: https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
- **Microsoft Foundry Documentation**: https://learn.microsoft.com/en-us/foundry/
- **Your Generated Artifacts**:
  - Constitution: `.specify/memory/constitution.md`
  - Specification: `specs/001-customer-service-agent/spec.md`
  - Technical Plan: `specs/001-customer-service-agent/plan.md` (Module 3)
  - Task List: `specs/001-customer-service-agent/tasks.md` (Module 3)

---

## ✅ Module 1 Deliverables Checklist

Before moving to Module 2, verify you have completed:

- [ ] ✅ Understood Spec-Driven Development principles
- [ ] ✅ Understood agentic AI fundamentals (agents, tools, orchestration)
- [ ] ✅ Set up Spec-Kit project structure
- [ ] ✅ Generated project constitution using `/speckit.constitution`
- [ ] ✅ Reviewed and understood your constitution
- [ ] ✅ Created git branch: `001-customer-service-agent`
- [ ] ✅ Completed Module 1 quiz
- [ ] ✅ Ratified constitution

**All items checked?** → **Ready for Module 2: Specification with `/speckit.specify`**

---

**Module 1 Status**: ✅ COMPLETE

**Next Step**: Module 2 will guide you through creating a detailed specification for your customer service agent using `/speckit.specify` with Microsoft Foundry and Agent Framework focus!

||||
|-|-|-|
| [Introduction](./INTRODUCTION.md) ←  | 📍 Module 1: Foundations |  → [Module 2: Specification](./MODULE_2_SPECIFICATION.md) |