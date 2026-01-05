# Module 4: Implementation with `/speckit.implement` - Backend & Frontend

**Estimated Duration**: 90-120 minutes  
**Prerequisites**: Complete Modules 1-3, have specification, plan, and tasks from previous modules  
**Deliverables**: 
- Full-stack implementation (backend + frontend) from `/speckit.implement`
- Functional agent with tools, FastAPI backend, React chat interface
- Agent state management with PostgreSQL and OpenTelemetry observability
- Comprehensive test suite (unit, integration, e2e)
- Ready for Foundry deployment

---

## 🎯 Learning Objectives

By the end of this module, you will:

1. Understand how `/speckit.implement` generates **complete full-stack code** (backend + frontend) from specifications
2. Learn **Microsoft Agent Framework implementation patterns** for tool definition and orchestration
3. Understand **FastAPI async patterns** for concurrent conversations
4. Learn to build **React chat interfaces** that interact with Agent Framework backends
5. Implement **test-driven development** across backend and frontend
6. Deploy **full-stack applications** to Microsoft Foundry

---

## 📚 Section 1: The `/speckit.implement` Command - Full-Stack Code Generation

### What `/speckit.implement` Generates

The `/speckit.implement` command analyzes your specification, plan, and tasks to generate **production-ready code**:

**Backend** (Python/FastAPI):
- Tool implementations with `@ai_function` decorator
- FastAPI server with Agent Framework integration
- PostgreSQL database schema and models
- Test suite (contract, integration, e2e tests)
- OpenTelemetry observability setup
- Docker container and Foundry deployment config

**Frontend** (React/TypeScript):
- Chat interface component with message display
- Input field for customer queries
- Real-time message streaming
- Agent response handling
- Conversation history display
- Error handling and loading states

**Infrastructure**:
- Dockerfile for containerization
- CI/CD pipeline (GitHub Actions)
- Foundry deployment manifests
- Database migrations

---

## 📚 Section 2: Backend Implementation - Agent Framework Patterns

### Tool Definition (3 Essential Patterns)

```python
# Pattern 1: Lookup Tool (Query only)
@ai_function
async def lookup_customer(customer_id: str) -> dict | None:
    """Find customer by email or ID."""
    result = await db.query(Customer).filter(...).first()
    return result if result else None

# Pattern 2: Decision Tool (Returns decision data)
@ai_function
async def get_return_policy(order_age: int) -> dict:
    """Check return eligibility."""
    if order_age > 90:
        return {"eligible": False, "reason": "Order too old"}
    return {"eligible": True, "refund_amount": 99.99}

# Pattern 3: Action Tool (Creates side effects)
@ai_function
async def initiate_return(order_id: str, reason: str) -> dict:
    """Start return process."""
    return_id = await db.create_return(order_id, reason)
    return {"status": "initiated", "return_id": return_id}
```

**Key Pattern**: Tools are **independent functions** the agent orchestrates. Agent reads results and **decides** next steps.

### FastAPI Backend Structure

```python
from fastapi import FastAPI
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint

app = FastAPI(title="Customer Service Agent")

# Tools (from implementation)
from agents.tools import (
    lookup_customer, search_orders, get_return_policy,
    initiate_return, create_support_ticket
)

# Create agent
agent = ChatAgent(
    name="CustomerServiceAgent",
    instructions="Help customers with orders and returns. Escalate complex issues.",
    chat_client=AzureOpenAIChatClient(...),
    tools=[lookup_customer, search_orders, get_return_policy, 
           initiate_return, create_support_ticket],
)

# Expose agent
add_agent_framework_fastapi_endpoint(app, agent, "/agent")

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Important**: All tools must be **async** for FastAPI concurrency (100+ simultaneous conversations).

### Agent State Management

**Two-Layer Architecture**:

1. **Agent Framework Memory** (in-memory, fast)
   - Recent conversation messages
   - Tool results cache
   - Current context

2. **PostgreSQL** (persistent, safe)
   ```sql
   CREATE TABLE conversations (
       id UUID PRIMARY KEY,
       customer_id VARCHAR(255) NOT NULL,
       created_at TIMESTAMP,
       status VARCHAR(50) DEFAULT 'active'
   );
   
   CREATE TABLE conversation_messages (
       id UUID PRIMARY KEY,
       conversation_id UUID NOT NULL,
       role VARCHAR(50), -- 'user', 'assistant', 'tool'
       content TEXT,
       tool_name VARCHAR(255),
       tool_parameters JSONB,
       tool_result JSONB,
       timestamp TIMESTAMP
   );
   ```

Agents load conversation history from PostgreSQL, maintain recent context in memory, and save all interactions for audit trails.

---

## 🎨 Section 3: Frontend Implementation - Chat Interface

### React Chat Component Structure

```typescript
// src/components/Chat.tsx
import { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string>('');

  // Initialize conversation
  useEffect(() => {
    setConversationId(crypto.randomUUID());
  }, []);

  // Send message to backend
  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: text,
        }),
      });

      const reader = response.body.getReader();
      let assistantContent = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        assistantContent += new TextDecoder().decode(value);

        setMessages(prev => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg?.role === 'assistant') {
            return [...prev.slice(0, -1), 
              { ...lastMsg, content: assistantContent }];
          }
          return [...prev, {
            id: crypto.randomUUID(),
            role: 'assistant',
            content: assistantContent,
            timestamp: new Date(),
          }];
        });
      }
    } catch (error) {
      setMessages(prev => [...prev, {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: `Error: ${error.message}`,
        timestamp: new Date(),
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} />
      <MessageInput 
        value={input}
        onChange={setInput}
        onSend={handleSendMessage}
        disabled={loading}
      />
    </div>
  );
}

// MessageList component
function MessageList({ messages }: { messages: Message[] }) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="messages">
      {messages.map(msg => (
        <div key={msg.id} className={`message message-${msg.role}`}>
          <p>{msg.content}</p>
          <small>{msg.timestamp.toLocaleTimeString()}</small>
        </div>
      ))}
      <div ref={scrollRef} />
    </div>
  );
}

// MessageInput component
function MessageInput({ value, onChange, onSend, disabled }: {
  value: string;
  onChange: (v: string) => void;
  onSend: (text: string) => void;
  disabled: boolean;
}) {
  return (
    <div className="input-area">
      <input
        type="text"
        value={value}
        onChange={e => onChange(e.target.value)}
        onKeyPress={e => e.key === 'Enter' && onSend(value)}
        placeholder="Ask about your order..."
        disabled={disabled}
      />
      <button onClick={() => onSend(value)} disabled={disabled || !value.trim()}>
        {disabled ? 'Sending...' : 'Send'}
      </button>
    </div>
  );
}
```

### Frontend ↔ Backend Flow

1. **User types message** → `handleSendMessage()` POSTs to `/agent/chat`
2. **Backend loads** conversation history from PostgreSQL
3. **Agent Framework** orchestrates tool calls (lookup_customer → get_return_policy → initiate_return)
4. **Backend streams** response chunks back to frontend  
5. **Frontend displays** agent response + tool details in real-time

**Error handling**:
```typescript
if (response.status === 400) {
  const error = await response.json();
  showError(`Invalid: ${error.detail}`);
} else if (response.status === 503) {
  showError('Service unavailable');
}
```

### Tool Results in Frontend

When agent calls tools, frontend can display tool details:

```typescript
interface Message {
  id: string;
  role: 'user' | 'assistant' | 'tool';
  content: string;
  toolName?: string;      // e.g., "initiate_return"
  toolResult?: object;    // e.g., { "return_id": "RET-123", "label_url": "..." }
  timestamp: Date;
}

// In MessageList, show tool results:
{msg.role === 'tool' && msg.toolResult && (
  <div className="tool-result">
    <strong>{msg.toolName}</strong>
    <pre>{JSON.stringify(msg.toolResult, null, 2)}</pre>
  </div>
)}
```

---

## Section 4: Backend Infrastructure - FastAPI & Persistence

### FastAPI with Agent Framework Integration

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient

app = FastAPI(title="Customer Service Agent")

# Enable frontend access
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

# Initialize agent
agent = ChatAgent(
    name="CustomerServiceAgent",
    instructions="Help customers with orders and returns.",
    chat_client=AzureOpenAIChatClient(...),
    tools=[lookup_customer, search_orders, get_return_policy, initiate_return, ...],
)

# Register agent endpoint
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/agent")

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Key**: Tools are async-ready for concurrent conversations (`await db.query()`).

### Conversation Persistence

```sql
-- Store conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP,
    metadata JSONB
);

-- Store messages and tool calls
CREATE TABLE conversation_messages (
    id UUID PRIMARY KEY,
    conversation_id UUID NOT NULL,
    role VARCHAR(50), -- 'user', 'assistant', 'tool'
    content TEXT,
    tool_name VARCHAR(255),
    tool_parameters JSONB,
    tool_result JSONB,
    timestamp TIMESTAMP
);

CREATE INDEX idx_messages_conversation ON conversation_messages(conversation_id);
```

### Loading Conversation Context

```python
async def load_context(conversation_id: str) -> list[dict]:
    """Load conversation history for agent."""
    messages = await db.execute(
        select(ConversationMessage)
        .where(ConversationMessage.conversation_id == conversation_id)
        .order_by(ConversationMessage.timestamp)
    )
    
    return [
        {"role": msg.role, "content": msg.content, "tool": msg.tool_name}
        for msg in messages.scalars()
    ]
```

### OpenTelemetry for Agent Visibility

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@ai_function
async def lookup_customer(customer_id: str) -> dict | None:
    """Look up customer with tracing."""
    with tracer.start_as_current_span("lookup_customer") as span:
        span.set_attribute("customer_id", customer_id)
        
        result = await db.get_customer(customer_id)
        
        span.set_attribute("status", "found" if result else "not_found")
        return result
```

**Why**: Debug agent decisions (which tool called, what result returned, did agent reason correctly).

---

## 📚 Section 5: Testing Full-Stack Implementation

### Test Types

**Unit Tests** (Tool Functions):
```python
@pytest.mark.asyncio
async def test_lookup_customer_found():
    result = await lookup_customer("test@example.com")
    assert result["customer_id"] == "12345"
    assert result["status"] in ["active", "inactive"]

@pytest.mark.asyncio
async def test_lookup_customer_not_found():
    result = await lookup_customer("nonexistent@example.com")
    assert result is None
```

**Integration Tests** (Agent + Tools):
```python
@pytest.mark.asyncio
async def test_agent_return_workflow():
    """Agent orchestrates: lookup → policy check → initiate return."""
    customer = await db.create(Customer)
    order = await db.create(Order, customer_id=customer.id, age_days=5)
    
    response = await agent.run(
        f"I want to return order #{order.id}",
        context={"customer_id": customer.id}
    )
    
    assert "return" in response.lower()
    assert "initiated" in response.lower()
```

**E2E Tests** (Frontend + Backend):
```typescript
// tests/chat.e2e.ts (Playwright/Cypress)
test('customer returns item via chat', async ({ page }) => {
  await page.goto('http://localhost:3000');
  
  // Send message
  await page.fill('input[placeholder="Ask about your order"]', 'I want to return my order');
  await page.click('button:has-text("Send")');
  
  // Verify agent response appears
  await page.waitForSelector('text=initiated');
  expect(page.locator('text=Return ID')).toBeDefined();
});
```

### Running Tests

```bash
# Backend tests
pytest backend/tests/ -v

# Frontend tests
npm run test --prefix frontend

# E2E tests
npx playwright test
```

---

## 📚 Section 6: Hands-On - Generate & Test Full-Stack Implementation

### Run `/speckit.implement`

In GitHub Copilot Chat:
```
/speckit.implement
```

**What generates**:
- Backend: `agents/`, `main.py`, `models.py`, `schema.sql`, `tests/`
- Frontend: `src/Chat.tsx`, `components/`
- Infrastructure: `Dockerfile`, `.github/workflows/`

### Test Locally (Backend)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt

# Run tests
pytest backend/tests/ -v

# Start server
python -m uvicorn backend.main:app --reload
```

### Test Locally (Frontend)

```bash
cd frontend && npm install && npm run dev
# Visit http://localhost:5173

# In another terminal, start backend
# Backend receives POST /agent/chat with customer messages
```

### Test E2E (Full Conversation)

```bash
# Terminal 1: Backend running on http://localhost:8000
# Terminal 2: Frontend running on http://localhost:5173

# In browser, type: "What orders do I have?"
# See agent response with order details

# Follow up: "I want to return order #123"
# See agent initiate return with return ID and label URL
```

---

## 📚 Section 7: Key Implementation Concepts

### Tool Independence

Each tool works standalone; agent orchestrates:
```python
# Good: Tools don't depend on each other
result = await lookup_customer("email@example.com")  # Works alone
result = await search_orders(customer_id)            # Works alone
```

### Error Handling for Agents

Return error objects, not exceptions:
```python
# Good
return {"status": "error", "message": "Order not found"}

# Bad  
raise ValueError("Order not found")  # Agent crashes
```

### State Across Turns

PostgreSQL preserves conversation history:
```python
# Message 1: "What orders do I have?"
# Message 2: "Return the first one"  ← Agent remembers Message 1
# Message 3: "When will I get my refund?"  ← Context includes both previous messages
```

---

## 📚 Section 8: Best Practices

1. **Test tools independently** - Contract tests ensure all tools work before agent runs
2. **Log all tool calls** - OpenTelemetry traces answer "why did agent do X?"
3. **Handle errors gracefully** - Return status fields, never raise exceptions
4. **Version tools** - As tools evolve, old conversations shouldn't break
5. **Observe frontend** - Log API calls so you see customer experience

---

```python
@ai_function
async def initiate_return(order_id: str, reason: str) -> dict:
    with tracer.start_as_current_span("initiate_return") as span:
        span.set_attribute("order_id", order_id)
        span.set_attribute("reason", reason)
        
        # Implementation
        result = await db.create_return(order_id, reason)
        
        span.set_attribute("return_id", result["return_id"])
        return result
```

---

## 🎓 Module 4 Quiz

Answer these questions to validate your understanding of Agent Framework implementation, tool design, and Foundry deployment.

### Question 1: Tool Orchestration and Agent Decision-Making

**Scenario**: A customer asks "I'm having issues with my order" (ambiguous request).

Your agent has these tools:
- `lookup_customer(email)` → customer_id
- `search_orders(customer_id)` → list of orders
- `get_order_details(order_id)` → detailed info
- `create_support_ticket(...)` → escalate

**Question**:
1. In what sequence should the agent call these tools?
2. Where does the agent make a **decision** vs. just executing a tool?
3. How would you implement error handling if lookup_customer returns None?

**Hint**: Think about how agent reasoning works—it's not a fixed flowchart.

---

### Question 2: Tool Design for Agent Reasoning

**Scenario**: Your team proposes combining return operations:

```python
def handle_return(order_id, action):
    if action == "check_policy":
        return check_policy(order_id)
    elif action == "initiate":
        return initiate_return(order_id)
    elif action == "status":
        return get_status(order_id)
```

**Question**:
1. Why is this poor tool design for Agent Framework?
2. How should these be restructured?
3. What benefit does proper separation provide to the agent's reasoning?

**Hint**: Review the tool design principles section.

---

### Question 3: Async Implementation for Concurrent Conversations

**Scenario**: Your backend needs to handle 100+ concurrent customer conversations.

**Question**:
1. Why must tools be async-ready (async/await)?
2. What happens if a tool blocks (synchronous database query)?
3. How does FastAPI with async support improve throughput?

**Hint**: Think about how concurrent conversations interact with tool execution.

---

### Question 4: State Management and Conversation History

**Scenario**: In a 5-message conversation:
- Message 1: "Where's my order?"
- Message 2: "It's order #12345"
- Message 3: "How long for refund?"
- Message 4: "I don't see it"
- Message 5: "When will it arrive?" (This is ambiguous—which refund?)

**Question**:
1. How does the agent maintain context across 5 messages?
2. Where is state stored (PostgreSQL, Agent Framework memory, or both)?
3. In message 5, how does agent know which refund the customer refers to?

**Hint**: Review the state management architecture section.

---

### Question 5: Observability for Debugging Agent Behavior

**Scenario**: An agent is stuck in a loop—it keeps calling the same tool repeatedly.

---

## ✅ Module 4 Quiz

**Question 1**: Customer says "I want to return my order" in the chat. Trace this through the full stack:
- What REST endpoint is called on the backend?
- Which Agent Framework tools are invoked in sequence?
- What HTTP response streams back to the frontend?
- How does the frontend display the return initiation response?

**Question 2**: You discover the agent is calling `get_order_status()` 15 times in a row with the same parameters. How would you diagnose this using OpenTelemetry traces? What are the possible root causes?

**Question 3**: Why must all tools be `async def` instead of `def` for FastAPI? Explain the difference between blocking and non-blocking database queries with 100 concurrent customers.

**Question 4**: A customer says "When will my refund arrive?" in Message 5 of a conversation. The agent correctly infers this refers to a refund initiated in Message 2. Explain:
- Where the context comes from (Agent Framework memory vs. PostgreSQL)
- How the agent resolves the ambiguity
- Why both layers (memory + database) are needed

**Question 5**: You're deploying the chat agent. List 5 changes you'd make comparing the local development setup to production, including CORS, logging, database, secrets, and rate limiting.

---

### 📚 Quick Reference: Full-Stack Data Flow

```
USER: "I want to return order #123"
  ↓
FRONTEND: fetch('/agent/chat', {message, conversation_id})
  ↓
BACKEND: POST /agent/chat receives request
  ↓
LOAD CONTEXT: load_conversation_context(conversation_id) from PostgreSQL
  ↓
AGENT FRAMEWORK: Analyzes message + context
  → Decision: "Need to check return policy"
  → Tool 1: get_return_policy(order_id=123)
  → Result: {"eligible": True, "refund_amount": 99.99}
  ↓
AGENT DECISION: "Eligible! Now initiate return"
  → Tool 2: initiate_return(order_id=123, reason="customer_request")
  → Result: {"status": "initiated", "return_id": "RET-456", "label_url": "..."}
  ↓
AGENT RESPONSE: "Return initiated. ID: RET-456. Label: https://..."
  ↓
BACKEND: Saves to PostgreSQL conversation_messages
  → role: "assistant"
  → tool_calls: [get_return_policy, initiate_return]
  → content: agent response
  ↓
FRONTEND: Receives streamed response
  → Displays: "Return initiated. ID: RET-456..."
  → Shows: Return label URL as clickable link
  ↓
USER: Sees confirmation in chat and can click label URL
```

---

## Resources

- [Agent Framework Tool Definitions](https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/tool-definitions)
- [FastAPI Async Databases](https://fastapi.tiangolo.com/async-sql-databases/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Spec-Driven Development (Spec-Kit)](https://github.com/github/spec-kit/blob/main/spec-driven.md)

---

## Next Steps

After completing Module 4:

1. **Run `/speckit.implement`** to generate full-stack code
2. **Run tests locally** (`pytest backend/tests/ -v`)
3. **Test agent in chat** locally via frontend
4. **Deploy to Foundry** with CI/CD pipeline (Module 5)

**You've completed the full spec-driven development workflow!**  
From Constitution → Specification → Planning → Implementation  
Your production-ready agent is ready for deployment. 🚀
