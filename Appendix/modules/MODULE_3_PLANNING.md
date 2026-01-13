# Module 3: Planning with Spec-Kit & Agent Framework
## From Specification to Multi-Agent Workflows

**Estimated Duration:** 20 minutes  
**Prerequisites:** Complete Modules 1 & 2, have specification from `/speckit.specify`  
**Deliverables:**
- Complete technical implementation plan (`specs/NNN-customer-service-agent/plan.md`)
- Executable task list (`specs/NNN-customer-service-agent/tasks.md`)
- Multi-agent architecture documentation
- Agent and workflow definitions

---

## 🎯 Learning Objectives

By the end of this module, you will:

1. Understand the **Microsoft Agent Framework** and how agents and workflows are built
2. Learn **Foundry Agents** concepts and deployment patterns
3. Understand the `/speckit.plan` and `/speckit.tasks` commands
4. Create a **multi-agent customer service system** implementation plan with orchestrated workflows
5. Generate a complete **implementation plan** and **executable task list**
6. Prepare for execution and learn how agent-framework integrates with **Microsoft Foundry**

---

## 📚 Section 1: Understanding Agent Framework Agents & Workflows

### 1.1 What is an Agent?

In the Microsoft Agent Framework, an **agent** is an autonomous AI entity that:

- **Understands intent** from user input through an LLM (GPT-4o, Azure OpenAI, etc.)
- **Makes decisions** about which tools to invoke and in what order
- **Executes tools** to retrieve data or trigger actions
- **Maintains context** across multiple conversation turns
- **Iterates** until the user's goal is achieved or escalation is needed

**Agent Components:**

```
┌─────────────────────────────────────────────────┐
│ User Input: "I want to return my order"         │
└────────────────────┬────────────────────────────┘
                     │
     ┌───────────────▼───────────────┐
     │  LLM Reasoning Engine         │
     │  (ex. Azure OpenAI / GPT-5)   │
     │  - Parse intent               │
     │  - Decide tools needed        │
     └───────────────┬───────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────┐      ┌───▼─────┐      ┌──▼───────┐
│Tool 1  │      │Tool 2   │      │Tool 3    │
│Lookup  │      │Check    │      │Initiate  │
│Customer│      │Return   │      │Return    │
│        │      │Policy   │      │          │
└────────┘      └─────────┘      └──────────┘
    │                │                │
    └────────────────┼────────────────┘
                     │
        ┌────────────▼─────────────┐
        │ Agent Response           │
        │ "Return initiated for... │
        └──────────────────────────┘
```

### 1.2 Agent Types in Microsoft Agent Framework

The Microsoft Agent Framework supports multiple agent types, each backed by different inference services:

| Agent Type | Service | Service Chat History storage supported | Custom Chat History storage supported |
|---|---|---|---|
| **Azure AI Agent** | Azure AI Agents Service | ✓ Yes | ✗ No |
| **Azure OpenAI Chat Completion** | Azure OpenAI | ✗ No | ✓ Yes |
| **Azure OpenAI Responses** | Azure OpenAI Responses Service | ✓ Yes | ✓ Yes |
| **OpenAI Chat Completion** | OpenAI | ✗ No | ✓ Yes |
| **OpenAI Responses** | OpenAI Responses Service | ✓ Yes | ✓ Yes |
| **OpenAI Assistants** | OpenAI Assistants API | ✓ Yes | ✗ No |
| **Custom ChatClient** | Any ChatClient implementation | Varies | Varies |

**For production customer service agents, recommend Azure AI Agent or Azure OpenAI Responses** (both support function tools and multi-turn conversations).

#### Creating a Basic Agent with Function Tools

All agents are created using `ChatAgent` with a chat client and instructions:

```python
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential

# Step 1: Create the agent with instructions
async with (
    DefaultAzureCredential() as credential,
    ChatAgent(
        chat_client=AzureAIAgentClient(async_credential=credential),
        instructions="You are a helpful assistant"
    ) as agent
):
    # Step 2: Run the agent
    response = await agent.run("Hello!")
    print(response.text)
```

#### Function Tools: Giving Agents Capabilities

Agents can use **function tools** for enhanced capabilities. Define tools as Python functions with type annotations and descriptions:

```python
from typing import Annotated
from pydantic import Field
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import DefaultAzureCredential

# Define tools as functions with clear parameter descriptions
def search_orders(
    customer_id: Annotated[str, Field(description="Customer UUID")]
) -> dict:
    """Search for customer orders"""
    return {
        "order_id": "ORD-123456",
        "status": "delivered",
        "purchase_date": "2025-12-15"
    }

def initiate_return(
    order_id: Annotated[str, Field(description="Order ID to return")],
    reason: Annotated[str, Field(description="Reason for return")]
) -> dict:
    """Initiate a return for an order"""
    return {
        "return_id": "RET-789",
        "status": "pending_approval",
        "estimated_completion": "7 business days"
    }

# Create agent with tools
async with (
    DefaultAzureCredential() as credential,
    AzureAIAgentClient(async_credential=credential).create_agent(
        instructions="You are an order specialist. Help customers find and return orders.",
        tools=[search_orders, initiate_return]  # Pass functions directly
    ) as agent
):
    # Agent now calls tools autonomously
    response = await agent.run("I want to return my order from December")
    print(response.text)
```

**Tool Definition Best Practices:**
- Use `Annotated` with `Field(description="...")` for all parameters
- Provide clear, concise docstrings
- Return well-structured data (dict or Pydantic model)
- Handle errors gracefully with meaningful return values
- Keep tool scope focused (one responsibility per tool)

#### Streaming Responses for Real-Time User Feedback

Agents support two response modes:

**Regular Response** - Wait for complete result:
```python
response = await agent.run("What's the weather in Seattle?")
print(response.text)
```

**Streaming Response** - Get results as they are generated (better UX):
```python
async for chunk in agent.run_stream("What's the weather in Portland?"):
    if chunk.text:
        print(chunk.text, end="", flush=True)  # Print incrementally
```

**When to use streaming:**
- Chat interfaces (users see response building in real-time)
- Long-running operations (provide progress feedback)
- Multi-tool workflows (show intermediate steps as tools execute)

**Agents that support streaming:** Azure OpenAI Chat Completion, Azure OpenAI Responses, OpenAI Chat Completion, OpenAI Responses

### 1.3 Agent Framework: Orchestrating Workflows

A **workflow** orchestrates multiple agents, tools, and control flow to handle complex scenarios. Workflows support several patterns:

#### Pattern 1: Sequential Workflow

Agents execute one after another. Each agent's output informs the next.

```
Customer Request
      ↓
[Triage Agent] → Classify & gather info
      ↓
[Specialist Agent] → Take action
      ↓
[Confirmation Agent] → Summarize & close
      ↓
Response
```

**Use case:** Multi-step processes with clear ordering (intake → analysis → resolution → confirmation)

#### Pattern 2: Handoff Workflow

A triage agent routes to the most appropriate specialist, who handles the issue.

```
Customer Request
      ↓
[Triage Agent] → Determine specialist needed
      ├─→ [Billing Agent] → Resolve billing issue
      ├─→ [Orders Agent] → Handle order problem
      └─→ [Technical Agent] → Fix technical issue
      ↓
Response
```

**Use case:** Multi-specialist environments where the right expert depends on problem type

#### Pattern 3: Concurrent Workflow

Multiple agents work in parallel on different aspects of a problem.

```
Customer Request
    ├─→ [Billing Agent] ──┐
    ├─→ [Orders Agent] ───┼─→ [Aggregator] → Response
    └─→ [Support Agent] ──┘
```

**Use case:** Gather information from multiple sources simultaneously

#### Pattern 4: Magentic Workflow

Multiple agents discuss and collaborate to solve complex problems.

```
Customer Problem
      ↓
[Manager Agent] → Plan approach
      ↓
[Agents] ↔ [Manager] → Collaborate & discuss
      ↓
Solution
```

**Use case:** Complex, multi-faceted issues requiring agent-to-agent discussion

### 1.4 Building a Multi-Agent Workflow

```python
from agent_framework import HandoffBuilder, ChatAgent
from agent_framework.azure import AzureAIAgentClient

async def create_customer_service_workflow():
    """Create handoff workflow for customer service"""
    
    # Define three specialist agents
    triage_agent = ChatAgent(
        name="TriageAgent",
        instructions="""Classify the customer issue:
        - Billing: Payments, invoices, refunds
        - Orders: Tracking, modifications, returns
        - Technical: System errors, bugs
        
        Provide context for the specialist.""",
        chat_client=chat_client
    )
    
    billing_agent = ChatAgent(
        name="BillingAgent",
        instructions="Handle payment and refund issues.",
        tools=[get_invoice, process_refund],
        chat_client=chat_client
    )
    
    orders_agent = ChatAgent(
        name="OrdersAgent",
        instructions="Handle order tracking and returns.",
        tools=[search_orders, initiate_return],
        chat_client=chat_client
    )
    
    # Build the workflow
    workflow = (
        HandoffBuilder(name="customer_service")
        .add_handoff_agent(
            triage_agent,
            [billing_agent, orders_agent]  # Triage can route to these
        )
        .add_handoff_agent(
            billing_agent,
            [triage_agent]  # Can escalate back to triage
        )
        .add_handoff_agent(
            orders_agent,
            [triage_agent]  # Can escalate back to triage
        )
        .build()
    )
    
    return workflow
```

---

## 📚 Section 2: Foundry Agents & Deployment

### 2.1 What is Microsoft Foundry?

**Microsoft Foundry** is an enterprise AI platform that provides:

- **Managed Agent Runtime:** Deploy agents without managing infrastructure
- **Model Selection:** Access to GPT-4o, GPT-4, and other LLMs
- **Tool Integration:** Connect to Azure services, APIs, databases
- **Orchestration:** Built-in workflow management and routing
- **Observability:** Full tracing of agent decisions and tool calls
- **Security:** Enterprise authentication, content filtering, compliance
- **Scaling:** Automatic scaling based on demand

### 2.2 Foundry Agent Architecture

Foundry provides a **"factory" approach** to agent development:

```
┌─────────────────────────────────────────────────┐
│           Foundry Control Plane                  │
│  (Config, Monitoring, Auth, Logging, Scaling)   │
└──────────────┬──────────────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼──────────────┐  ┌──▼──────────────┐
│  Agent Instance  │  │  Agent Instance  │
│  (Replica 1)     │  │  (Replica 2)     │
└───┬──────────────┘  └──┬──────────────┘
    │                    │
┌───▴────────────────────▴────┐
│  Shared Infrastructure       │
│  - LLM (GPT-4o)              │
│  - Tool Execution            │
│  - State Store (Cosmos DB)   │
│  - Message History           │
└──────────────────────────────┘
```

### 2.3 Foundry Agent Components

**1. Models:** The LLM powering reasoning
- GPT-4o (recommended)
- GPT-4
- Llama (via Azure)

**2. Instructions:** Define agent behavior, role, constraints
- System prompts guide decisions
- Tool usage patterns
- Escalation logic

**3. Tools:** What the agent can do
- Function calls to external services
- Database queries
- API integrations
- File operations

**4. Orchestration:** How agents interact
- Workflow patterns
- State management
- Message routing

**5. Observability:** Monitoring and debugging
- Full conversation history
- Tool execution traces
- Performance metrics
- Error tracking

**6. Trust & Safety:** Enterprise security
- Microsoft Entra authentication
- RBAC (Role-Based Access Control)
- Content filtering
- Encrypted state storage

### 2.4 Creating and Deploying Agents with Agent Framework

#### Creating Agents with AzureAIClient

The **Microsoft Agent Framework** provides `AzureAIClient` to create agents that run on **Microsoft Foundry**. This is the modern approach using the `azure-ai-projects` SDK:

**Basic Agent Creation Pattern:**

```python
import asyncio
from typing import Annotated
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field

# Define tools as functions
def search_orders(
    customer_id: Annotated[str, Field(description="Customer UUID")]
) -> dict:
    """Search for customer orders"""
    return {
        "order_id": "ORD-123456",
        "status": "delivered",
        "purchase_date": "2025-12-15"
    }

def initiate_return(
    order_id: Annotated[str, Field(description="Order ID to return")],
    reason: Annotated[str, Field(description="Reason for return")]
) -> dict:
    """Initiate a return for an order"""
    return {
        "return_id": "RET-789",
        "status": "pending_approval",
        "estimated_completion": "7 business days"
    }

async def main():
    # Authenticate with Azure (requires `az login`)
    async with AzureCliCredential() as credential:
        # Create agent with AzureAIClient
        async with (
            AzureAIClient(credential=credential).create_agent(
                name="customer-support-agent",
                instructions="You are an order specialist. Help customers find and return orders.",
                tools=[search_orders, initiate_return]  # Pass functions directly
            ) as agent
        ):
            # Run agent - it autonomously calls tools based on user intent
            response = await agent.run("I want to return my order from December")
            print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Thread Management for Conversation Persistence

Agents in Foundry maintain conversation context using **threads**. There are three patterns:

**Pattern 1: Automatic Thread Creation (Stateless)**

Each `agent.run()` creates a new thread - no context preserved across calls:

```python
# First query - creates thread automatically
result1 = await agent.run("What's the weather in Seattle?")

# Second query - creates a NEW thread (doesn't remember Seattle)
result2 = await agent.run("What was the last city I asked about?")
```

**Pattern 2: In-Memory Thread Persistence**

Reuse a thread across multiple turns with `store=False`:

```python
# Create a thread to reuse
thread = agent.get_new_thread()

# First query
result1 = await agent.run("What's the weather in Tokyo?", thread=thread, store=False)

# Second query - same thread, remembers Tokyo
result2 = await agent.run("How about that city?", thread=thread, store=False)
```

**Pattern 3: Service-Managed Thread Persistence (Recommended for Production)**

Let Foundry manage thread storage for true conversation persistence:

```python
# First conversation - thread stored on service
thread = agent.get_new_thread()
result1 = await agent.run("First question", thread=thread)
thread_id = thread.id  # Save this ID

# Later, reconnect to the same conversation
thread = agent.get_new_thread(service_thread_id=thread_id)
result2 = await agent.run("Second question", thread=thread)
# Agent remembers the context from "First question"
```

**Full Example with Thread Persistence:**

```python
async def example_with_thread_persistence():
    async with AzureCliCredential() as credential:
        async with (
            AzureAIClient(credential=credential).create_agent(
                name="OrderSupportAgent",
                instructions="Help customers with orders and returns.",
                tools=[search_orders, initiate_return]
            ) as agent
        ):
            # Start a new conversation with a persistent thread
            thread = agent.get_new_thread()
            
            # User looks up an order
            result1 = await agent.run(
                "Find my order from December",
                thread=thread  # Thread persists on service
            )
            print(f"Agent: {result1.text}")
            
            # Later, same conversation continues
            result2 = await agent.run(
                "I want to return that order",
                thread=thread  # Same thread, agent remembers the order
            )
            print(f"Agent: {result2.text}")
```

#### Reusing Agent Versions in Production

To avoid creating new agent versions on each run, use `use_latest_version=True`:

```python
async with (
    AzureAIClient(
        credential=credential,
        use_latest_version=True  # Reuse latest version instead of creating new
    ).create_agent(
        name="customer-support-agent",
        instructions="Help customers with orders...",
        tools=[search_orders, initiate_return]
    ) as agent
):
    response = await agent.run("I want to return my order")
```

#### Integration with Hosted MCP Tools

Agents can use **Hosted Model Context Protocol (MCP)** tools from Foundry:

```python
from agent_framework import HostedMCPTool

async with (
    AzureAIClient(credential=credential).create_agent(
        name="docs-agent",
        instructions="Help with Microsoft documentation questions.",
        tools=HostedMCPTool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
            approval_mode="never_require"  # Or "always_require" for approvals
        )
    ) as agent
):
    response = await agent.run("How do I create an Azure storage account?")
```

#### Foundry Deployment Architecture

When agents are created with `AzureAIClient`, they are automatically deployed to **Microsoft Foundry**:

```
┌─────────────────────────────────────────────────┐
│      Microsoft Foundry Control Plane             │
│  (Hosting, Scaling, Monitoring, Auth, Logging)  │
└──────────────┬──────────────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼──────────────┐  ┌──▼──────────────┐
│  Agent Instance  │  │  Agent Instance  │
│  (Replica 1)     │  │  (Replica 2)     │
│                  │  │                  │
│ search_orders    │  │ search_orders    │
│ initiate_return  │  │ initiate_return  │
└───┬──────────────┘  └──┬──────────────┘
    │                    │
┌───▴────────────────────▴────┐
│  Foundry Infrastructure      │
│  - LLM (Azure OpenAI)        │
│  - Thread Store              │
│  - Tool Execution            │
│  - Message History (Cosmos)  │
│  - Auto-scaling              │
└──────────────────────────────┘
```

**Key Benefits:**
- **Managed runtime**: No infrastructure to manage
- **Auto-scaling**: Handles variable load automatically
- **Persistent storage**: Conversations stored in Cosmos DB
- **Observability**: Full tracing via Application Insights
- **Security**: Built-in authentication and content filtering
- **Enterprise-ready**: RBAC, audit logs, compliance support

---

## 📚 Section 3: Planning with Spec-Kit: Plan & Tasks

### 3.1 Overview: From Specification to Executable Tasks

**Specification-Driven Development (SDD)** has been covered in previous modules. This section focuses on the **planning and tasking phase** of Spec-Kit, where specifications become actionable implementation work.

The workflow is straightforward:

```
Step 1: Specification (covered in Module 2)
  Feature Description → /speckit.specify → spec.md
  
Step 2: Planning ← YOU ARE HERE
  spec.md → /speckit.plan → plan.md + contracts/ + data-model.md + research.md
  (Agent architecture, tool contracts, workflow patterns)
  
Step 3: Tasks
  plan.md → /speckit.tasks → tasks.md
  (Executable work items, dependencies, parallelization)
  
Step 4: Implementation
  tasks.md → Development Team → Working System
  
Step 5: Deployment
  Working System → Foundry → Production
```

### 3.2 The `/speckit.plan` Command

**Purpose:** Transform a feature specification into a comprehensive, technically detailed implementation plan.

**Inputs:**
- `specs/NNN-feature-name/spec.md` - The feature specification from `/speckit.specify`

**What it does:**

1. **Specification Analysis** - Reads and understands feature requirements, user stories, and acceptance criteria
2. **Constitutional Compliance** - Ensures alignment with project architecture principles and constraints
3. **Technical Translation** - Converts business requirements into technical architecture and implementation details
4. **Detailed Documentation** - Generates supporting documents for data models, API contracts, and scenarios
5. **Quickstart Validation** - Produces validation scenarios capturing critical user workflows

**Outputs:**
- `plan.md` - Complete technical architecture, phases, and implementation approach
- `data-model.md` - Entity definitions (Customer, Order, Return, Conversation, etc.)
- `contracts/tools.md` - Tool function signatures, parameters, returns, error handling
- `contracts/endpoints.md` - API endpoint definitions and request/response formats
- `research.md` - Technology choices with rationale and alternatives considered
- `quickstart.md` - Key validation scenarios to test before full implementation

**Key Content in plan.md:**

The implementation plan contains:
- **Overview** - High-level summary and architecture diagram
- **Agent Definitions** - Instructions, tools, responsibilities for each agent
- **Tool Contracts** - Precise function signatures and data contracts
- **Workflow Definition** - Orchestration pattern, flow, transitions, escalation paths
- **Foundry Deployment** - Configuration, environment setup, scaling strategy
- **Implementation Phases** - Sequenced phases (Foundation, Agents, Workflows, Testing, Deployment)
- **Technology Decisions** - Why specific technologies were chosen (with rationale)

**Example outputs for Customer Service Agent:**

```
plan.md contains:
- 3 agent definitions: Triage, Orders, Billing
- Handoff workflow with routing logic
- 8 tool contracts (search_orders, initiate_return, get_invoice, etc.)
- Data model for Customer, Order, Return, Conversation
- 5 implementation phases with clear sequencing
- Foundry deployment configuration

data-model.md contains:
- Customer: id, name, email, status, tier
- Order: id, customer_id, items, status, dates
- Return: id, order_id, reason, status
- Conversation: id, customer_id, messages, agent_history

contracts/tools.md contains:
- search_orders(customer_id, order_id?, status?) → List[Order]
- initiate_return(order_id, reason) → Return
- get_invoice(invoice_id) → Invoice
- process_refund(order_id, amount, reason) → Refund
- With parameters, returns, errors, and validation rules
```

### 3.3 Creating a Plan: Best Practices

**DO:**
- ✅ **Mention the framework** - "Using Microsoft Agent Framework with Foundry deployment"
- ✅ **Specify agent roles** - "3 agents: Triage, Orders, Billing"
- ✅ **Define orchestration pattern** - "Handoff workflow for dynamic routing"
- ✅ **List tools explicitly** - "Tools: search_orders, initiate_return, get_invoice"
- ✅ **Include observability** - "OpenTelemetry for tool call tracing"
- ✅ **Mention data persistence** - "PostgreSQL for state, conversation history"
- ✅ **Specify deployment target** - "Full Foundry deployment to managed runtime"
- ✅ **Include testing strategy** - "Unit tests for tools, integration tests for workflows"

**AVOID:**
- ❌ Vague descriptions - "Build a good agent system"
- ❌ Technology ambiguity - "Use any database"
- ❌ Over-specification - "Use 10 microservices"
- ❌ Missing Foundry context - Makes it deployment-unfriendly
- ❌ No observability - Can't debug in production
- ❌ Missing escalation - Agent can't handle complex cases

### 3.4 The `/speckit.tasks` Command

**Purpose:** Analyze the implementation plan and generate an executable task list with dependencies and parallelization markers.

**Inputs:**
- `plan.md` (required)
- `data-model.md` (optional but recommended)
- `contracts/` directory (optional but recommended)
- `research.md` (optional)

**What it does:**

1. **Plan Analysis** - Reads the implementation plan and supporting documents
2. **Task Derivation** - Converts architecture, contracts, and entities into specific, actionable tasks
3. **Dependency Mapping** - Identifies which tasks depend on which others
4. **Parallelization** - Marks independent tasks `[P]` and outlines safe parallel groups
5. **Sequencing** - Orders tasks to optimize for execution with maximum parallelism
6. **Output Generation** - Writes `tasks.md` ready for team execution

**Outputs:**
- `tasks.md` - Complete task list with:
  - Task descriptions and acceptance criteria
  - Dependency information
  - Parallelization markers `[P]`
  - Execution groups showing which tasks can run together
  - Estimated timeline and critical path

**Example task structure:**

```
# Tasks: Customer Service Agent

## Summary
- Total Tasks: 35
- Parallel Groups: 8
- Critical Path: Tasks 1→2→4→7→12 (15 working days)
- Estimated Timeline: 4 weeks with 2-3 person team

## Execution Groups

### Group A (Days 1-2): Foundation [Sequential]
- Task 1: Define data models
- Task 2: Create database schema
- Task 3: Set up FastAPI project

### Group B (Days 3-4): Core Agents [Parallel - [P]]
- Task 4: [P] Implement Triage Agent
- Task 5: [P] Implement Orders Agent
- Task 6: [P] Implement Billing Agent
- Task 7: [P] Create tool contracts

### Group C (Days 5-6): Tools [Parallel - [P]]
- Task 8: [P] Implement search_orders tool
- Task 9: [P] Implement initiate_return tool
- Task 10: [P] Implement get_invoice tool

### Group D (Day 7): Workflow
- Task 12: Build HandoffBuilder workflow
- Task 13: Implement FastAPI /chat endpoint

### Group E (Days 8-9): Testing [Parallel - [P]]
- Task 14: [P] Unit tests for tools
- Task 15: [P] Integration tests for agents
- Task 16: [P] E2E tests for workflows

### Group F (Day 10): Deployment
- Task 17: Configure Foundry deployment
- Task 18: Deploy to Foundry
```

### 3.5 Task Execution & Team Coordination

**For Team Leads:**
1. Review task dependencies and critical path
2. Identify parallel groups that teams can work on simultaneously
3. Assign tasks to team members based on expertise
4. Track progress against timeline

**For Developers:**
1. Pick a task from your assigned group
2. Review dependencies (what must complete first)
3. Implement according to the plan
4. Update task status as you progress
5. Move to next task in the group

**For QA:**
1. Review testing tasks and test scenarios from `quickstart.md`
2. Prepare test environments as agents complete
3. Run unit/integration/E2E tests as agents and tools are implemented
4. Track test results and flag issues

### 3.6 Why Plan & Tasks Matter for Agent Development

For agentic AI systems, structured planning is particularly powerful:

| Aspect | Without Planning | With /speckit.plan & /speckit.tasks |
|--------|-----------------|-------------------------------------|
| **Agent Boundaries** | Discovered during coding | Explicit in specification and plan |
| **Tool Contracts** | Undefined until implementation | Precisely defined in contracts/ |
| **Workflow Patterns** | Emergent and undocumented | Documented with flow diagrams |
| **Team Coordination** | Unclear dependencies | Clear parallel groups |
| **Tool Testing** | Happens after implementation | Part of upfront task design |
| **Escalation Logic** | Ad hoc decisions | Specified upfront in plan |
| **Implementation Timeline** | Unpredictable | Estimated with critical path |
| **Replication** | Difficult to reproduce | Reproducible from task list |

---

## 🔧 Hands-On - Creating Plan & Tasks for Customer Service Agent

### Scenario: Multi-Agent Customer Service System

**Goal:** Build a customer service agent system with three specialized agents orchestrated in a handoff workflow.

**Agents:**
1. **Triage Agent** - Classifies customer issues and routes to specialists
2. **Orders Agent** - Handles order tracking and returns
3. **Billing Agent** - Handles refunds and payment issues

**Workflow Pattern:** Handoff (triage routes to specialists)

### Step 1: Generate Plan with `/speckit.plan`

In VS Code, open GitHub Copilot Chat (`Ctrl+Shift+I` on Windows, `Cmd+Shift+I` on Mac).  
Next, enter one the following prompts. For this lab, choose one of the three options based on your desired complexity:

#### Option 1: Comprehensive Multi-Agent Plan (Recommended)

```
/speckit.plan Build a production-ready multi-agent customer service system 
using Microsoft Agent Framework deployed to Microsoft Foundry.

System Components:
- 3 agents: Triage (classify issues), Orders (handle returns/tracking), 
  Billing (handle refunds/payments)
- Orchestration: Handoff workflow - Triage routes to specialists
- Tools: search_orders, initiate_return, get_invoice, process_refund, 
  create_support_ticket
- Backend: FastAPI with async support for concurrent conversations
- Database: PostgreSQL for customer/order data and conversation history
- Frontend: Vite + React + TypeScript for chat UI
- LLM: Azure OpenAI (GPT-4.1-mini) configurable via Foundry
- Observability: OpenTelemetry for tracing all tool calls and agent decisions
- Deployment: Full Foundry deployment with auto-scaling

Key Features:
- Agents maintain full conversation context across turns
- Seamless handoff between agents preserves history
- Tool calls are traceable for debugging and analytics
- Escalation to human support via create_support_ticket
- All agent instructions documented in plan
- Tool contracts documented in contracts/tools.md
- Data models for Customer, Order, Return, Conversation documented
- Error handling and retry logic specified
```

#### Option 2: MVP Plan (Fast Iteration)

```
/speckit.plan Minimal viable multi-agent system. 3 agents (Triage, Orders, 
Billing) in handoff workflow. Core tools: search_orders, initiate_return, 
get_invoice, process_refund. FastAPI + PostgreSQL. React UI. Azure OpenAI. 
Focus on core user stories only (order lookup, return initiation, refund status). 
No advanced features. Rapid implementation.
```

#### Option 3: Enterprise-Grade Plan

```
/speckit.plan Enterprise-grade multi-agent customer service with high 
availability. 3 primary agents (Triage, Orders, Billing) plus escalation 
path to Human Agent. Handoff + Magentic patterns for complex cases. 

Tools (7 total): search_orders, get_order_details, check_return_policy, 
initiate_return, get_refund_status, create_support_ticket, send_notification

Infrastructure:
- FastAPI with circuit breakers for resilience
- PostgreSQL with read replicas + Cosmos DB backup
- Redis for caching and rate limiting
- React + TypeScript with offline support
- Foundry deployment with multi-region failover

Observability:
- OpenTelemetry with structured logging
- Application Insights integration
- Full audit trail of customer interactions
- PII encryption in logs

Testing:
- Unit tests for each tool
- Integration tests for agent-tool interaction
- End-to-end tests for complete workflows
- Load testing for 1000+ concurrent conversations

Security:
- Microsoft Entra authentication
- RBAC for agent access
- Request validation and sanitization
- Rate limiting per customer
- Graceful degradation on service failures
```

### Best Practices for Plan Prompts

**✅ DO:**
- **Mention the framework:** "Using Microsoft Agent Framework with Foundry deployment"
- **Specify agent count and roles:** "3 agents: Triage, Orders, Billing"
- **Define orchestration pattern:** "Handoff workflow for dynamic routing"
- **List tools explicitly:** "Tools: search_orders, initiate_return, get_invoice"
- **Include observability:** "OpenTelemetry for tool call tracing"
- **Mention data persistence:** "PostgreSQL for state, conversation history"
- **Specify deployment target:** "Full Foundry deployment to managed runtime"
- **Include testing strategy:** "Unit tests for tools, integration tests for workflows"

**❌ AVOID:**
- Vague descriptions: "Build a good agent system" (too broad)
- Technology ambiguity: "Use any database" (no clear decisions)
- Over-specification: "Use 10 microservices" (too detailed)
- Missing Foundry context: (Plan won't be deployment-ready)
- No observability: (Can't debug in production)
- Missing escalation: (Agent can't handle complex cases)
- Future speculation: "Add ML later" (not in specification)

**What this generates:**
- `specs/001-customer-service-agent/plan.md` - Complete technical architecture and phases
- `specs/001-customer-service-agent/data-model.md` - Customer, Order, Return, Conversation data models
- `specs/001-customer-service-agent/contracts/tools.md` - Tool function signatures and contracts
- `specs/001-customer-service-agent/contracts/endpoints.md` - FastAPI endpoint contracts
- `specs/001-customer-service-agent/research.md` - Technology choices researched
- `specs/001-customer-service-agent/quickstart.md` - Key validation scenarios

**Verification:**
Check that plan.md was created successfully and review its structure.


If time permits, review the generated `plan.md` to understand the architecture and implementation approach.
Also, we've added some bonus material on creating comprehensive plan prompts and an analysis of plan outputs in the [module appendix below](#appendix-comprehensive-plan-prompts-and-analysis-of-output).

### Step 2: Generate Tasks with `/speckit.tasks`

After `/speckit.plan` completes, run in GitHub Copilot Chat:

```
/speckit.tasks
```

This command:
1. Reads your `plan.md` file
2. Analyzes the architecture, phases, and components
3. Derives executable tasks from:
   - Data model definitions → Database schema tasks
   - Tool contracts → Tool implementation tasks
   - Workflow patterns → Orchestration tasks
   - Testing requirements → Test task
4. Marks parallelizable tasks as `[P]`
5. Generates `tasks.md` with clear dependencies

**Example tasks generated:**

```markdown
# Tasks: Customer Service Agent

## Phase 1: Foundation

### Task 1: Define Data Models
- [ ] Create Customer data model
- [ ] Create Order data model
- [ ] Create Return data model
- [ ] Create Conversation data model
- [ ] Document schemas in data-model.md
**Depends on:** Nothing
**Blocks:** Tasks 2, 3

### Task 2: [P] Implement Database Schema
- [ ] Create PostgreSQL tables (Customer, Order, Return, Conversation)
- [ ] Add indexes for common queries
- [ ] Create migration script
**Depends on:** Task 1
**Parallelizable with:** Task 3

### Task 3: [P] Create Tool Contracts
- [ ] Define search_orders contract
- [ ] Define initiate_return contract
- [ ] Define get_invoice contract
- [ ] Define process_refund contract
- [ ] Document in contracts/tools.md
**Depends on:** Task 1
**Parallelizable with:** Task 2

## Phase 2: Agent Implementation

### Task 4: [P] Implement Triage Agent
- [ ] Create ChatAgent with system prompt
- [ ] Add tool definitions
- [ ] Write routing logic to specialists
**Depends on:** Tasks 2, 3
**Parallelizable with:** Tasks 5, 6

### Task 5: [P] Implement Orders Agent
- [ ] Create ChatAgent specialized for orders
- [ ] Add search_orders tool
- [ ] Add initiate_return tool
**Depends on:** Tasks 2, 3
**Parallelizable with:** Tasks 4, 6

### Task 6: [P] Implement Billing Agent
- [ ] Create ChatAgent specialized for billing
- [ ] Add get_invoice tool
- [ ] Add process_refund tool
**Depends on:** Tasks 2, 3
**Parallelizable with:** Tasks 4, 5

## Phase 3: Workflow Orchestration

### Task 7: Build Handoff Workflow
- [ ] Create HandoffBuilder with Triage agent
- [ ] Connect Triage → Orders agent
- [ ] Connect Triage → Billing agent
- [ ] Add escalation paths
**Depends on:** Tasks 4, 5, 6
**Blocks:** Task 8

### Task 8: Implement FastAPI Endpoints
- [ ] Create /chat endpoint for user input
- [ ] Implement conversation history retrieval
- [ ] Add error handling and validation
**Depends on:** Task 7
**Blocks:** Task 9

## Phase 4: Testing

### Task 9: [P] Write Tool Tests
- [ ] Unit tests for each tool
- [ ] Mock external services
- [ ] Test error conditions
**Depends on:** Tasks 4, 5, 6
**Parallelizable with:** Task 10

### Task 10: [P] Write Integration Tests
- [ ] Test agent + tool interactions
- [ ] Test handoff between agents
- [ ] Test conversation context preservation
**Depends on:** Task 7
**Parallelizable with:** Task 9

### Task 11: Write End-to-End Tests
- [ ] Test complete user scenarios
- [ ] Test each specialist workflow
- [ ] Test escalation paths
**Depends on:** Tasks 9, 10

## Phase 5: Deployment

### Task 12: Deploy to Foundry
- [ ] Create Foundry project configuration
- [ ] Configure agents in Foundry
- [ ] Set up monitoring and logging
- [ ] Deploy to managed runtime
**Depends on:** Task 11
```

---

## ✅ Hands-On Checklist

After completing the hands-on exercise, you should have:

- [ ] Completed `/speckit.plan` command for your customer service agent
- [ ] Generated `plan.md` with agent and tool definitions
- [ ] Generated `data-model.md` with all required data structures
- [ ] Generated `contracts/tools.md` with tool specifications
- [ ] Completed `/speckit.tasks` command
- [ ] Generated `tasks.md` with executable work items
- [ ] Identified parallel task groups for your team
- [ ] Understood handoff workflow pattern
- [ ] Mapped all 3 agents (Triage, Orders, Billing) to tools

---

## 🎓 Module 3 Quiz

Answer these questions to validate your understanding of planning, task generation, Microsoft Agent Framework, and the customer service agent application.

### Question 1: Agent Framework Tool Orchestration

**Scenario**: In the customer service agent, a customer asks: "I want to return my defective item from order #12345."

The agent needs to determine the order is eligible for return before initiating the return request.

**Question**: 
1. Describe the sequence of tools the agent should call (in order)
2. At what point does the agent make a **decision** vs. just calling a tool?
3. How does Agent Framework help the agent decide which tool to call next?

**Hint**: Review the agent lifecycle and tool orchestration section.

---

### Question 2: Tool Design for Agent Reasoning

**Scenario**: A team member proposes combining multiple operations into one tool:

```python
def handle_customer_issue(customer_id, action, data):
    if action == "lookup":
        return lookup_customer_data(customer_id)
    elif action == "return":
        return initiate_return(customer_id, data)
    elif action == "escalate":
        return create_ticket(customer_id, data)
```

**Question**:
1. Why is this poor tool design for Microsoft Agent Framework?
2. How would you restructure this into separate tools?
3. What benefit does this provide to the agent's reasoning process?

**Hint**: Review the "Tool Design Principles" section.

---

### Question 3: Agent State Management and Multi-Turn Conversations

**Scenario**: In your technical plan, you need to document how the agent handles multi-turn conversations:

Customer Message 1: "I can't use my order"
Customer Message 2: "How long do I have to return it?"
Customer Message 3: "Can I get my money back?"

**Question**:
1. How should the agent maintain context across these three messages?
2. What does Agent Framework need (database, state management) to remember order context?
3. Where does this conversation history get stored (PostgreSQL? Agent Framework? Both?)?

**Hint**: Review the Agent Framework planning checklist.

---

### Question 4: Observable Agent Behavior

**Scenario**: Your customer service agent is deployed to Foundry, and a customer is frustrated because the agent keeps calling the same tool repeatedly.

**Question**:
1. How would OpenTelemetry observability help debug this issue?
2. What specific agent behavior should you trace (tool calls, parameters, results)?
3. Why is observability crucial for agent applications (vs. traditional APIs)?

**Hint**: Review "Planning Best Practices" section on observability.

---

## ✅ Module 3 Quiz: Worked Solutions

### Solution 1: Agent Framework Tool Orchestration

**Tool sequence:**

1. **First**, call `lookup_customer(customer_id="12345")` to verify customer identity
2. **Second**, call `search_orders(customer_id)` to find order #12345
3. **Third**, call `get_return_policy()` to check if this order is eligible (age, condition)
4. **Agent Decision Point**: Read results: "Order is 5 days old, policy allows 90 days → ELIGIBLE"
5. **Fourth**, call `initiate_return(order_id="12345", reason="defective")`
6. **Agent generates response**: "Your return has been initiated. Return ID: RET456..."

**Where is the decision?**

After step 3, the agent doesn't just blindly call tool 4. It **reads the return policy results** and **decides**: "All conditions are met. I have enough information to initiate the return." This decision-making is what makes it an **agent**, not just a script executing tool calls in sequence.

**How does Agent Framework help?**

- Tool descriptions guide the agent: "initiate_return() is used when customer wants to return an eligible order"
- The LLM reads tool results and reasons about next steps
- Tool parameters are explicit, so agent knows what data to provide
- The agent can decide to escalate instead if order is ineligible

**Key Insight**: Agents don't follow a fixed flowchart. They reason about results and decide next actions dynamically.

---

### Solution 2: Tool Design for Agent Reasoning

**Why the monolithic tool is bad:**

1. **Agent can't reason about it**: "What does `handle_customer_issue()` do?" - too vague
2. **Parameter is ambiguous**: `action` as a string forces agent to guess which value to use
3. **Difficult to test**: One change breaks all functionality
4. **Tool description problem**: "Handles issues" doesn't help agent decide when to call it
5. **Violates Single Responsibility**: One tool tries to do three different things

**Better structure:**

```python
# Focused tools - agent can reason about each
tool 1: lookup_customer(customer_id: str) → CustomerInfo
tool 2: initiate_return(order_id: str, reason: str) → ReturnConfirmation  
tool 3: create_support_ticket(conversation_context: str, reason: str) → TicketInfo
```

**Why this is better:**

- ✅ Clear descriptions help agent decide when to use each tool
- ✅ Parameters are explicit (agent knows exactly what to provide)
- ✅ Each tool has one responsibility
- ✅ Easy to unit test individually
- ✅ Tool discovery is clearer: "What tools are available?" - agent can list them

**Agent Framework benefit:**

When tools are focused, Agent Framework's LLM can better match customer intent to the right tool:
- Customer asks "Where's my order?" → Clear: use `lookup_customer()` + `search_orders()`
- Customer asks "I want to return this" → Clear: use `get_return_policy()` + `initiate_return()`

---

### Solution 3: Agent State Management and Multi-Turn Conversations

**How agent maintains context:**

1. **Message 1**: "I can't use my order"
   - Agent reads message, searches orders → finds order context
   - Stores in conversation history (database)
   
2. **Message 2**: "How long do I have to return it?"
   - Agent reads **all previous messages** (from database)
   - Context: Order context is already known
   - Agent calls `get_return_policy()` and applies to that order

3. **Message 3**: "Can I get my money back?"
   - Agent reads all previous messages
   - Context: Already knows customer, order, return eligibility
   - Agent responds based on full context

**What Agent Framework needs:**

```
STORAGE (Database - PostgreSQL):
├── Conversations table
│   ├── conversation_id
│   ├── customer_id
│   └── created_at
└── Messages table
    ├── message_id
    ├── conversation_id
    ├── role (user/assistant)
    ├── content
    ├── tool_calls (JSON)
    └── timestamp

AGENT FRAMEWORK (Memory):
├── Current conversation thread (in-memory)
├── Tool results cache (recent calls)
└── User context (extracted intent, order reference, etc.)
```

**Where does conversation history live?**

```
PostgreSQL:
- Full conversation history (persistent)
- All tool calls and results
- For retrieval, auditing, multi-session context

Agent Framework (Memory):
- Current conversation thread
- Active context (what order are we discussing?)
- Tool results from recent calls (for efficiency)
- Between requests, conversation is read from PostgreSQL
```

**Key Insight**: Persistent storage (PostgreSQL) + in-memory context (Agent Framework) work together for multi-turn conversations.

---

### Solution 4: Observable Agent Behavior

**How OpenTelemetry helps debug:**

When the agent calls the same tool repeatedly, observability reveals:

```
OpenTelemetry tracing captures:
├── Tool call 1: lookup_customer(CUST123) → returns customer data
├── Tool call 2: lookup_customer(CUST123) → returns SAME customer data
├── Tool call 3: lookup_customer(CUST123) → returns SAME customer data
│
→ Root cause: Agent isn't progressing (stuck in loop)
```

**Without observability**, you'd see:
- Customer: "Why is the agent not helping?"
- Log output: "(generic chat response)"
- **No visibility** into what tools agent is calling

**Specific behaviors to trace:**

```
TRACE THESE:
├── Tool calls
│   ├── Tool name (e.g., "lookup_customer")
│   ├── Parameters (e.g., customer_id="12345")
│   ├── Execution time (e.g., 234ms)
│   └── Result (success/error)
│
├── Agent decisions
│   ├── "Agent determined escalation needed"
│   ├── "Agent recognized intent: return request"
│   └── "Agent selected tool: initiate_return"
│
└── Conversation context
    ├── Message tokens (input/output)
    ├── LLM response (agent's reasoning)
    └── Final response to customer
```

**Why observability is crucial for agents (vs. traditional APIs):**

| API Observability | Agent Observability |
|------|------|
| Request → Response (linear) | Complex multi-turn reasoning |
| Clear input/output | Internal decision-making is invisible |
| Easy to debug: what went wrong? | **Hard to debug**: why did agent do X? |
| Tools are synchronous | Tools may fail; agent must handle gracefully |
| Simple execution flow | Agent may call tools in unexpected order |

For agents, you need visibility into:
- **Why** the agent called this tool
- **What** the agent thought the customer meant
- **How** the agent progressed through the conversation
- **Where** it failed or took unexpected paths

This is why observability is mentioned in **every planning best practice**.

---

## 📌 What's Next

In **Module 4: Implementation**, you will:
- Implement the three agents from your plan
- Create tool functions for agent use
- Build the HandoffBuilder workflow
- Create FastAPI endpoints
- Implement conversation persistence

In **Module 5: Deployment**, you will:
- Deploy agents to Microsoft Foundry
- Set up observability and monitoring
- Test multi-agent scenarios
- Optimize for production scale
- **How do tools** work in the Microsoft Agent Framework?
- **What data models** do we need?
- **How is the agent deployed** to Microsoft Foundry?
- **What are the testing strategies**?
- **What are the performance constraints**?
- **What observability and monitoring** do we need?

---

## 📚 Resources

- **Spec-Kit `/speckit.plan` Documentation**: https://github.com/github/spec-kit/blob/main/spec-driven.md#the-speckit-plan-command
- **Spec-Kit `/speckit.tasks` Documentation**: https://github.com/github/spec-kit/blob/main/spec-driven.md#the-speckit-tasks-command
- **Microsoft Agent Framework**: https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview
- **Microsoft Foundry**: https://azure.microsoft.com/en-us/products/ai-foundry

---

**Module 3 Status**: ✅ COMPLETE


||||
|-|-|-|
| [Module 2: Specification](./MODULE_2_SPECIFICATION.md) ←  | 📍 Module 3: Planning |  → [Module 4: Implementation](./MODULE_4_IMPLEMENTATION.md) |

---


## Appendix: Comprehensive plan prompts and analysis of output 

<details>
<summary>Expand to view</summary>

### A.1. Why Plans Matter for Agentic Systems

Traditional plans focus on code structure. **Agentic AI plans** focus on:

| Traditional Plan | Agentic Plan |
|-----------------|-------------|
| Database schema | Agent state and conversation history |
| API endpoints | Agent tool signatures and orchestration |
| Code modules | Agent lifecycle and decision logic |
| Deployment | Foundry-native deployment patterns |
| Observability | Tool call tracing and agent reasoning visibility |

**Example**: In a traditional plan, you design a return endpoint. In an **agentic plan**, you design a `initiate_return()` tool that the agent **calls autonomously** based on user intent, with clear contracts for what it accepts and returns.

### Understanding Agent Framework in Technical Plans

Plans must document how the **Microsoft Agent Framework** works for your specific agent:

```
AGENT FRAMEWORK PLANNING CHECKLIST
=====================================

[ ] Tool Definitions
    - Each tool has clear name, description, parameters
    - Parameters are JSON Schema compliant
    - Return types are well-defined
    - Error handling is documented

[ ] Agent Instructions
    - System prompts guide agent reasoning
    - Tool descriptions help agent decide when to use each tool
    - Escalation logic defined (when to create support ticket)

[ ] State Management
    - Conversation history stored in database
    - User context preserved across turns
    - Tool call results cached appropriately

[ ] Orchestration Patterns
    - Sequential: Tool1 → Tool2 → Tool3 (return policy → initiate return → confirm)
    - Conditional: IF condition THEN use Tool1 ELSE Tool2
    - Parallel: Independent queries can run simultaneously

[ ] Foundry Integration
    - Agent fits within Foundry's managed runtime
    - No custom dependencies Foundry doesn't support
    - Observability hooks in place (OpenTelemetry)
    - Deployment model specified (containerized, serverless, etc.)
```

### A.2. Planning Best Practices for Agentic Systems

**1. Explicitly Mention Agent Framework**
```
✅ DO: "Using Microsoft Agent Framework with async tool calling"
❌ DON'T: "Building a conversational system"
```

**2. Document Tool Contracts Clearly**
```
✅ DO: "Tool lookup_customer(customer_id: str) returns {name, email, status}"
❌ DON'T: "Tools for customer data"
```

**3. Include Foundry Deployment from Day 1**
```
✅ DO: "Deploying to Microsoft Foundry managed runtime with auto-scaling"
❌ DON'T: "We'll figure out deployment later"
```

**4. Address Agent Orchestration Patterns**
```
✅ DO: "Agent uses sequential tool calling: policy check → return initiation → confirmation"
❌ DON'T: "Agent uses various tools"
```

**5. Plan for Observability and Debugging**
```
✅ DO: "OpenTelemetry for tool call tracing; structured logging for agent reasoning"
❌ DON'T: "Standard logging"
```

**6. Include Escalation Strategy**
```
✅ DO: "Agent escalates to human support when unable to resolve or customer requests human"
❌ DON'T: "No escalation logic"
```

**7. Reference Test Strategy**
```
✅ DO: "Unit tests per tool; integration tests for agent orchestration; e2e tests for conversations"
❌ DON'T: "Tests later"
```


### A.3. Creating a Comprehensive Plan Prompt

Here's a **template prompt** you can customize for your scenario:

```
/speckit.plan Build a [SCALE: production-ready | MVP] multi-agent 
customer service system using Microsoft Agent Framework deployed to 
Microsoft Foundry.

PRIMARY AGENTS:
- [Agent1 Name]: [Role and responsibilities]
  Tools: [tool1, tool2, ...]
  
- [Agent2 Name]: [Role and responsibilities]
  Tools: [tool1, tool2, ...]
  
- [Agent3 Name]: [Role and responsibilities]
  Tools: [tool1, tool2, ...]

ORCHESTRATION:
- Pattern: [Sequential | Handoff | Concurrent | Magentic]
- Workflow flow: [Describe the flow]
- Escalation: [How complex issues are handled]

BACKEND:
- API Framework: [FastAPI, Django, etc.]
- Database: [PostgreSQL, Azure SQL, etc.]
- Caching: [Redis, Azure Cache, etc.]

FRONTEND:
- UI Framework: [React, Vue, etc.]
- Language: [TypeScript, JavaScript]
- Key features: [List UI requirements]

LLM & DEPLOYMENT:
- Model: [Azure OpenAI GPT-4o, GPT-4, Llama]
- Platform: [Microsoft Foundry]
- Scaling: [Auto-scaling requirements]

OBSERVABILITY:
- Tracing: [OpenTelemetry, Application Insights]
- Logging: [Structured logging, audit trail]
- Metrics: [Tool usage, agent decisions, performance]

TESTING STRATEGY:
- Unit tests: [Tool testing approach]
- Integration tests: [Agent + workflow testing]
- E2E tests: [User scenario testing]
- Performance: [Concurrent conversation targets]

SECURITY:
- Authentication: [Microsoft Entra, JWT, etc.]
- Authorization: [RBAC, per-user access]
- Data protection: [Encryption, PII handling]
```

---

### A.4. Understanding Generated Plan Content

When you run `/speckit.plan`, it generates several key documents:

#### plan.md Structure

```markdown
# Technical Plan: Customer Service Agent

## Overview
High-level summary of what's being built

## Architecture Overview
- Component diagram
- Technology stack table
- Agent definitions

## Agent Definitions
- Triage Agent
  - Instructions/system prompt
  - Tools
  - Responsibilities
  
- Specialist Agents
  - Instructions
  - Tools
  - Escalation logic

## Tool Contracts
- Tool 1: search_orders
  - Parameters
  - Return values
  - Error handling
  
- Tool 2: initiate_return
  - Parameters
  - Return values
  - Validation rules

## Workflow Definition
- Orchestration pattern (Handoff)
- Flow diagram
- Agent transitions
- Escalation paths

## Foundry Deployment
- Configuration YAML
- Environment setup
- Scaling strategy
- Monitoring setup

## Implementation Phases
### Phase 1: Foundation
- Tasks and deliverables

### Phase 2: Agents
- Agent implementation
- Tool integration

### Phase 3: Workflows
- Workflow orchestration
- API endpoints

### Phase 4: Testing
- Unit tests
- Integration tests
- E2E tests

### Phase 5: Deployment
- Foundry configuration
- Production deployment
```

#### data-model.md Structure

```markdown
# Data Models

## Customer
```
customer_id: UUID
name: string
email: string
account_status: "active" | "suspended" | "premium"
created_at: timestamp
```

## Order
```
order_id: string (ORD-XXXXX)
customer_id: UUID
items: Item[]
total: decimal
status: "pending" | "shipped" | "delivered" | "returned"
created_at: timestamp
```

## Return
```
return_id: string (RET-XXXXX)
order_id: string
customer_id: UUID
reason: string
status: "pending_approval" | "approved" | "shipped_back" | "completed"
created_at: timestamp
```

## Conversation
```
conversation_id: UUID
customer_id: UUID
messages: ChatMessage[]
current_agent: string
created_at: timestamp
```

### 5.3 contracts/tools.md Structure

```markdown
# Tool Contracts

## Tool: search_orders

**Purpose:** Find customer orders

**Function Signature:**
```python
def search_orders(
    customer_id: str,
    order_id: str = None,
    status: str = None
) -> List[Order]
```

**Parameters:**
- `customer_id` (required): Customer UUID
- `order_id` (optional): Specific order ID to search
- `status` (optional): Filter by status (pending, shipped, delivered)

**Returns:** List of Order objects matching criteria

**Errors:**
- `CustomerNotFound`: Invalid customer_id
- `DatabaseError`: Connection failure (retry logic)

## Tool: initiate_return

**Purpose:** Start a return process for an order

**Function Signature:**
```python
def initiate_return(
    order_id: str,
    reason: str,
    items: List[str] = None
) -> Return
```

**Parameters:**
- `order_id` (required): Order to return
- `reason` (required): Why is the customer returning
- `items` (optional): Specific items in order to return

**Returns:** Return object with return_id and status

**Errors:**
- `OrderNotFound`: Invalid order_id
- `ReturnNotAllowed`: Order too old or ineligible
- `ValidationError`: Missing required parameters

## Tool: get_invoice

**Purpose:** Retrieve invoice details

**Function Signature:**
```python
def get_invoice(invoice_id: str) -> Invoice
```

## Tool: process_refund

**Purpose:** Approve and process a refund

**Function Signature:**
```python
def process_refund(
    order_id: str,
    amount: decimal,
    reason: str
) -> Refund
```

**Approval Requirements:**
- Amount > $100: Requires manager approval
- Amount > $1000: Requires VP approval
```

---

### Sample Prompts for Your Implementation

#### Complete Sample: Multi-Agent Customer Service

Use this prompt for a comprehensive, production-ready plan:

```
/speckit.plan Build a production-ready multi-agent customer service system 
using Microsoft Agent Framework with Foundry deployment.

AGENTS (3 total):
- Triage Agent: Classify customer issues (Billing, Orders, Technical)
  Routes to appropriate specialist
  
- Orders Agent: Handle order-related issues
  Tools: search_orders, initiate_return, get_order_details
  
- Billing Agent: Handle payment and refund issues
  Tools: get_invoice, process_refund, check_account_balance

ORCHESTRATION:
Pattern: Handoff (Triage routes to specialists)
Flow: Customer → Triage → Specialist (Orders|Billing) → Resolution
Escalation: Complex cases escalate to human support via create_support_ticket

BACKEND:
- API: FastAPI with async support
- Database: PostgreSQL for customers, orders, returns, conversations
- Caching: Redis for recent conversations and customer lookup
- State: Full conversation history preserved across agent handoffs

FRONTEND:
- Framework: Vite + React
- Language: TypeScript
- UI: Real-time chat with agent typing indicators
- Features: Conversation history, customer info sidebar, escalation notification

LLM & DEPLOYMENT:
- Model: Azure OpenAI GPT-4o (configurable via environment)
- Platform: Microsoft Foundry with auto-scaling
- Regions: Primary + backup region for HA

OBSERVABILITY:
- Tracing: OpenTelemetry with Azure Monitor
- Logging: Structured JSON logs with agent decisions
- Metrics: Tool call latency, agent response time, escalation rate
- Dashboard: Real-time monitoring of agent performance

DATA MODELS:
- Customer: ID, name, email, status (active/premium), tier
- Order: ID, customer, items, status, dates
- Return: ID, order reference, reason, status, timeline
- Conversation: ID, customer, messages, agent history, context

TESTING:
- Unit: Each tool in isolation with mocks
- Integration: Agent + tools + database
- E2E: Complete user scenarios (lookup order, initiate return, check refund)
- Load: 1000+ concurrent conversations

SECURITY:
- Auth: Microsoft Entra with RBAC
- Data: Encrypted storage for sensitive fields (phone, address)
- Validation: Input sanitization, SQL injection prevention
- Audit: Full conversation audit trail for compliance
```

#### Quick Sample: MVP Implementation

For rapid prototyping:

```
/speckit.plan Minimal viable multi-agent customer service. 

Agents: Triage, Orders, Billing (handoff pattern)
Tools: search_orders, initiate_return, get_invoice, process_refund
Backend: FastAPI, PostgreSQL
Frontend: React + TypeScript (basic chat UI)
Deployment: Foundry
Focus: Core user flows only - order lookup, return initiation, refund status check
Testing: Basic integration tests
No advanced features yet
```

#### Enterprise Sample: Complex Workflows

For complex, mission-critical systems:

```
/speckit.plan Enterprise customer service platform with advanced orchestration.

ORCHESTRATION PATTERNS:
- Primary: Handoff (Triage → Specialist)
- Complex cases: Magentic (Agent discussion for multi-faceted issues)
- Escalation: Human agent in loop with approval gates

AGENTS (5 total):
- Triage Agent: Issue classification and routing
- Orders Agent: Full order lifecycle (search, modify, return)
- Billing Agent: Payments, refunds, disputes
- Technical Agent: System issues, bugs, technical help
- Human Agent: Final escalation, complex cases, approval gates

TOOLS (10+ total):
- search_orders, get_order_details, modify_order, cancel_order
- initiate_return, check_return_policy, get_return_status
- get_invoice, process_refund, dispute_charge, check_account_balance
- create_support_ticket, assign_to_human, get_ticket_status

WORKFLOW PATTERNS:
- Sequential: Multi-step resolution with handoff
- Concurrent: Parallel lookups (billing + order details)
- Magentic: Complex issues (shipping + billing + returns)
- Escalation: Human review for high-value issues

DEPLOYMENT:
- Foundry with multi-region failover
- Cosmos DB for state backup
- Auto-scaling 0-10,000 conversations/minute
- Content filtering + prompt injection protection

OBSERVABILITY:
- Full distributed tracing (OpenTelemetry)
- Agent decision reasoning captured
- Tool call audit trail
- Customer satisfaction tracking
- Analytics on agent performance

TESTING:
- Unit: All 10+ tools
- Integration: All agent-tool combinations
- E2E: 20+ complete user scenarios
- Load: 5,000+ concurrent conversations
- Chaos: Failure recovery patterns

SECURITY:
- RBAC with fine-grained access
- Conversation encryption at rest
- PII masking in logs
- Rate limiting per customer
- Fraud detection on refunds > $500
```

</details>