<!-- 
================================================================================
  SYNC IMPACT REPORT - Constitution v1.0.0
================================================================================

  Version Change: [TEMPLATE] → 1.0.0 (Initial Creation - MAJOR)
  
  Principles Defined (5 total):
    ✅ I. Spec-Driven Development Foundation (new)
    ✅ II. Intent-First Architecture for Agentic AI (new)
    ✅ III. Microsoft Foundry-Native Deployment (new)
    ✅ IV. Clear, Simple Learning Path (new)
    ✅ V. Quiz-Driven Competency Validation (new)

  Sections Added:
    ✅ Overview - Lab purpose and scope
    ✅ Lab Structure: Five Progressive Modules - Detailed module breakdown
    ✅ Lab Delivery Standards - Quality assurance requirements
    ✅ Technology Stack & Prerequisites - Tools and services required
    ✅ Governance - Amendment, compliance, and review procedures

  Template Consistency Status:
    ✅ spec-template.md - Aligned (user stories already support learning objectives)
    ✅ plan-template.md - Aligned (technical context fits agent architecture planning)
    ✅ tasks-template.md - Aligned (task organization supports module-based delivery)
    ✅ checklist-template.md - Verified compatible
    ⚠️  agent-file-template.md - Note: Module content will reference this for agent patterns

  Outstanding Items (for implementation):
    [ ] Module 1: Agentic AI Fundamentals & Lab Constitution (full lesson plan)
    [ ] Module 2: Intent Specification & User Story Definition (full lesson plan)
    [ ] Module 3: Technical Architecture & Foundry Deployment Planning (full lesson plan)
    [ ] Module 4: Agent Implementation & Iterative Development (full lesson plan)
    [ ] Module 5: Deployment, Monitoring & Advanced Patterns (full lesson plan)
    [ ] Quiz questions and solutions (25 total - 5 per module)
    [ ] Code examples and hands-on exercises (5 per module)

  No Breaking Changes: All template conventions preserved. No existing content overwritten.
  
================================================================================
-->

# Microsoft Agent Framework Hands-On Training Lab Constitution

## Overview

This hands-on training lab guides developers through building a complete agentic AI application using the Microsoft Agent Framework and Microsoft Foundry, following the Spec-Driven Development methodology with the Spec-Kit framework. The lab consists of 5 progressive modules that build competency in specification-driven development, with quiz questions and comprehensive solutions included.

## Core Principles

### I. Spec-Driven Development Foundation
Specifications are executable blueprints, not documentation artifacts. Every feature begins with a clear, measurable specification that defines **what** to build before addressing **how** to build it. Specifications must precede implementation in all cases. The Spec-Kit framework governs this process: Constitution → Specification → Technical Plan → Task Breakdown → Implementation. This non-negotiable sequence ensures clarity, reduces rework, and produces predictable outcomes.

### II. Intent-First Architecture for Agentic AI
Agentic applications require explicit intent definition before tool selection or orchestration design. Every agent capability MUST be grounded in a clear user intent and measurable success criteria. Agents must be composed of reusable, independently testable components. Microsoft Agent Framework patterns (tool definition, orchestration, state management) MUST be applied consistently across all agent implementations.

### III. Microsoft Foundry-Native Deployment
All developed artifacts MUST be deployable to Microsoft Foundry. Agents, models, and supporting infrastructure MUST use Foundry-compatible patterns and configurations. Development occurs in Foundry-aligned environments to eliminate deployment surprises. Tested artifacts MUST verify Foundry deployment paths before claiming completion.

### IV. Clear, Simple Learning Path
Each module builds directly on prior module output. No module requires external domain knowledge. Step-by-step instructions MUST be accompanied by expected outcomes and verification checkpoints. Jargon MUST be explained on first use. Each module MUST take 60–90 minutes for a developer new to agentic AI but experienced in general software development.

### V. Quiz-Driven Competency Validation
Knowledge must be validated through practical quizzes after each module. Quizzes MUST test understanding of module concepts, not memorization. Each quiz MUST include complete worked solutions showing the reasoning process. Quizzes guide learners to self-diagnose gaps without instructor intervention.

## Lab Structure: Five Progressive Modules

### Module 1: Agentic AI Fundamentals & Lab Constitution
**Objective**: Understand agentic AI concepts and establish project governance.
- Introduction to agents, tools, and orchestration
- Lab constitution review and ratification
- Setup: Spec-Kit initialization, agent environment
- **Deliverable**: Initialized project with governance established
- **Quiz**: 5 questions on agent concepts, constitution principles

### Module 2: Intent Specification & User Story Definition
**Objective**: Define clear intents and translate to executable specifications.
- Understanding user intents in agentic systems
- Writing specifications that guide agent design
- Use case: Multi-step AI assistant for [specific domain]
- **Deliverable**: Completed specification document in Spec-Kit format
- **Quiz**: 5 questions on specification clarity and completeness

### Module 3: Technical Architecture & Foundry Deployment Planning
**Objective**: Plan technical implementation using Microsoft Agent Framework and Foundry.
- Microsoft Agent Framework architecture patterns
- Defining agent tools and tool contracts
- Foundry deployment topology and configuration
- **Deliverable**: Technical plan with tool definitions and Foundry config
- **Quiz**: 5 questions on architecture patterns and Foundry concepts

### Module 4: Agent Implementation & Iterative Development
**Objective**: Build working agent using Microsoft Agent Framework.
- Implementing agents with Microsoft Agent Framework
- Tool integration and state management
- Local testing and validation loops
- **Deliverable**: Working agent code, unit tests, local validation
- **Quiz**: 5 questions on implementation patterns and testing strategy

### Module 5: Deployment, Monitoring & Advanced Patterns
**Objective**: Deploy to Foundry, monitor, and explore advanced agent patterns.
- Deploying agents to Microsoft Foundry
- Monitoring, observability, and logging
- Advanced: Multi-agent orchestration, fine-tuning, optimization
- **Deliverable**: Live agent in Foundry with monitoring enabled
- **Quiz**: 5 questions on deployment, monitoring, and advanced patterns

## Lab Delivery Standards

### Clarity & Accessibility
- Each module includes step-by-step instructions with expected outputs
- Screenshots or terminal examples MUST show expected state at each checkpoint
- Links to Microsoft documentation MUST be current and verified
- Code examples MUST be copy-pasteable and runnable without modification

### Hands-On Reinforcement
- Each module MUST include at least one "hands-on" exercise requiring learner input
- Exercises build on prior module outputs to reinforce Spec-Driven Development continuity
- No "magic" commands—every step MUST explain what it does and why

### Quiz & Solution Format
- Each module concludes with 5 practical quiz questions
- Quiz questions test application of concepts, not recall
- Complete worked solutions MUST accompany quiz answers
- Solutions MUST explain reasoning and reference applicable framework concepts

## Technology Stack & Prerequisites

### Required Tools
- Python 3.11+ (Spec-Kit requirement)
- Spec-Kit CLI (installed via `uv tool install specify-cli`)
- Microsoft Agent Framework SDK
- Git for version control
- Supported AI coding agent (Claude, GitHub Copilot, Cursor, etc.)

### Microsoft Services
- Microsoft Foundry account (trial or production)
- Microsoft Agent Framework (public preview or stable)
- Optional: Azure OpenAI or GitHub Models for LLM access

### Development Environment
- macOS, Linux, or Windows (Spec-Kit compatible)
- IDE with AI agent support recommended
- Terminal/shell (bash, zsh, or PowerShell)

## Governance

### Amendment Process
This constitution MUST be reviewed and updated after each full cohort completion. Amendments require:
1. Documented feedback from learners (Module completion surveys)
2. Identified gaps or pain points in the learning path
3. Proposed changes with rationale and impact assessment
4. Approval by lab maintainers before implementation

### Compliance & Versioning
- All quiz solutions and code samples MUST reflect current Microsoft Agent Framework APIs
- Module content MUST be validated against current Foundry deployment documentation monthly
- Version MUST follow MAJOR.MINOR.PATCH:
  - MAJOR: New module added or existing module completely redesigned
  - MINOR: Significant content updates, new quiz questions, or framework version upgrades
  - PATCH: Clarifications, link updates, typo fixes, code example corrections

### Review & Validation Checklist
- [ ] All code examples tested in clean environment
- [ ] Quiz solutions verified for accuracy
- [ ] Microsoft documentation links checked for validity
- [ ] Microsoft Agent Framework version clearly stated per module
- [ ] Estimated time-to-complete validated by new learner
- [ ] Foundry deployment path verified end-to-end
- [ ] Accessibility review (clarity, terminology, code readability)

### Lab Maintenance Responsibility
A designated lab maintainer MUST conduct quarterly reviews against:
- Latest Microsoft Agent Framework releases and breaking changes
- Foundry UI/API updates that affect deployment workflows
- Learner feedback and completion metrics
- Module difficulty calibration (target: 90%+ completion rate)

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
