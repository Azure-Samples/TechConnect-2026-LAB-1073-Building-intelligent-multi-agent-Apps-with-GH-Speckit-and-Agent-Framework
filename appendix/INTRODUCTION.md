# LAB 1073 - Building intelligent, multi-agent Apps with Github Spec-Kit and Agent Framework


## 🎓 Learning Objectives
🎯 Learn how to convert specs into working code with Spec Kit and build multi-agent workflows using the Microsoft Agent Framework  
🎯 Discover how to use Azure AI Foundry with built-in observability, tracing, and safety to confidently deploy secure, scalable AI apps and multi-agent workflows  

We will learn together and reach our learning objectives by practicing the following:

✅ **Understand** specification-driven development principles  
✅ **Write** executable specifications in Markdown  
✅ **Create** technical plans from specifications   
✅ **Generate** full-stack applications using GitHub Copilot  
✅ **Build** Microsoft Agent Framework applications with tool orchestration.  
✅ **Configure** Microsoft Foundry agents for production use  

---

## Scenario: Multi-Agent Customer Service Application
Throughout this lab, we will build a multi-agent customer service application using specification-driven development principles. The application will consist of specialized AI agents that handle different aspects of customer service, such as billing inquiries, order tracking, and technical support.

We will use technologies including the Microsoft Agent Framework for creating and orchestrating, Microsoft Foundry for hosting our agents, conversation threads and AI models. We will learn to use the Spec-Kit framework to write executable specifications that drive the development process.

Below is an overview of the architecture and design principles we will follow.

### Business Requirements

Modern customer service demands:
- **24/7 Availability**: Instant response to customer inquiries
- **Specialization**: Different issues require different expertise
- **Escalation Handling**: Complex issues route to human agents
- **Context Awareness**: Understanding customer history and context
- **Validation of actions**: Human-in-the-loop for sensitive operations

### Multi-Agent Architecture Design

A professional customer service system uses **specialized agents**, each focused on one aspect:

```
┌──────────────────────────────────────────────────────────┐
│         Customer Service Multi-Agent System              │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐      ┌──────────────┐    ┌──────────┐   │
│  │   Triage    │      │   Billing    │    │  Orders  │   │
│  │   Agent     │      │   Agent      │    │  Agent   │   │
│  │             │      │              │    │          │   │
│  │ • Classify  │      │ • Payments   │    │ • Track  │   │
│  │ • Route     │      │ • Invoices   │    │ • Modify │   │
│  │ • Context   │      │ • Refunds    │    │ • Cancel │   │
│  └─────────────┘      └──────────────┘    └──────────┘   │
│         ▲                   ▲                   ▲        │
│         │ Routes to         │ Routes to         │        │
│         └─────────────┬─────┴───────────────────┘        │
│                       │                                  │
│                 ┌─────▼──────┐                           │
│                 │   Router   │                           │
│                 │  Service   │                           │
│                 └─────▲──────┘                           │
│                       │                                  │
│              ┌────────┴────────┐                         │
│              │                 │                         │
│         ┌────▼──────┐   ┌──────▼───┐                     │
│         │   Human   │   │ Knowledge│                     │
│         │   Escalate│   │   Base   │                     │
│         └───────────┘   └──────────┘                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Agent Responsibilities

#### 1. **Triage Agent**
- **Purpose**: First point of contact
- **Responsibilities**:
  - Understand customer issue
  - Classify inquiry type
  - Route to appropriate specialist
  - Maintain conversation context
- **Tools**: Classification model, routing rules, conversation history

#### 2. **Billing Agent**
- **Purpose**: Handle payment and billing inquiries
- **Responsibilities**:
  - Check invoice status
  - Process refunds
  - Explain payment terms
  - Update billing information
- **Tools**: Billing database access, payment processing API, refund system

#### 3. **Orders Agent**
- **Purpose**: Manage order-related inquiries
- **Responsibilities**:
  - Track order status
  - Modify order details
  - Process cancellations
  - Handle shipping inquiries
- **Tools**: Order management system, inventory database, shipping API

#### 4. **Technical Support Agent** (optional specialized agent)
- **Purpose**: Handle technical issues
- **Responsibilities**:
  - Troubleshoot problems
  - Provide technical guidance
  - Escalate infrastructure issues
- **Tools**: Knowledge base, diagnostic tools, escalation system

---

## 📖 Lab Curriculum (5 Modules)

| # | Module | File | Duration | Focus |
|---|--------|------|----------|-------|
| 1 | **Constitution & Foundations** | [MODULE_1_FOUNDATIONS.md](lab/modules/MODULE_1_FOUNDATIONS.md) | 10 minutes | Philosophy & Principles |
| 2 | **Specification & Features** | [MODULE_2_SPECIFICATION.md](lab/modules/MODULE_2_SPECIFICATION.md) | 20 minutes | Writing Executable Specs |
| 3 | **Technical Planning** | [MODULE_3_TECHNICAL-PLANNING.md](lab/modules/MODULE_3_TECHNICAL-PLANNING.md) | 20 minutes | Architecture & Design |
| 4 | **Implementation** | [MODULE_4_IMPLEMENTATION.md](lab/modules/MODULE_4_IMPLEMENTATION.md) | 20 minutes | Backend + Frontend Code |
| 5 | **Deployment to Azure** | [MODULE_5_DEPLOYMENT.md](lab/modules/MODULE_5_DEPLOYMENT.md) | 10 minutes | Execution |

**Total Learning Time**: 1.5 hours (90 minutes)

---

## 🎯 Learning Objectives Summary

### Module 1: Constitution
- Understand specification-driven development philosophy
- Set up GitHub Copilot as development tool
- Learn the constitutional principles

### Module 2: Specification
- Write executable specifications
- Define features, APIs, and data models
- Create tool contracts and test requirements

### Module 3: Planning
- Convert specs to technical designs
- Plan system architecture
- Design infrastructure and deployment

### Module 4: Implementation
- Generate code using `/speckit.implement`
- Build Agent Framework backend
- Create React chat frontend
- Test full-stack application

### Module 5: Deployment
- Write Bicep infrastructure templates
- Deploy Foundry agents
- Setup CI/CD with GitHub Actions
- Configure monitoring with Application Insights

---

## What's Next?

In **Module 1: Foundations**, we will:
- Establish the principles of specification-driven development
- Set up our development environment with GitHub Copilot
- Define the constitutional articles that will guide our lab journey
- Prepare for writing executable specifications in the next module
- Get ready to embark on building our multi-agent customer service application!

---

**Let's get started building our multi-agent customer service application!**

||
|-|
| ➡ [Module 1: Foundations](./modules/MODULE_1_FOUNDATIONS.md)|