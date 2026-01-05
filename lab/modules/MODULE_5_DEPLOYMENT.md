# Module 5: Deployment to Azure - Infrastructure as Code & Foundry Agents

**Estimated Duration**: 90-120 minutes  
**Prerequisites**: Complete Modules 1-4, have full-stack implementation (backend + frontend) ready  
**Deliverables**: 
- Complete Bicep infrastructure templates for Azure deployment
- Foundry agent configuration and deployment
- CI/CD pipeline for automated testing and deployment
- Monitoring and observability setup (Application Insights)
- Running customer service agent on Azure using Microsoft Foundry
- Production-ready infrastructure following security best practices

---

## 🎯 Learning Objectives

By the end of this module, you will:

1. Understand **Bicep best practices** for deploying agent-based applications to Azure
2. Learn to deploy **Foundry agents** with Microsoft Agent Framework
3. Set up **CI/CD pipelines** for automated testing and deployment
4. Configure **observability** with Application Insights for agent monitoring
5. Use `/speckit.implement` for **infrastructure generation only** (app code already complete)
6. Deploy a **production-ready customer service agent** on Azure

---

## 📚 Section 1: Azure Deployment Architecture for Agent-Based Apps

### Full-Stack Architecture on Azure

```
┌─────────────────────────────────────────────────────────────┐
│                        INTERNET                             │
└────────┬────────────────────────────────────────────────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────────┐
│            AZURE FRONT DOOR (Global Load Balancing)         │
│                   HTTPS Termination                         │
└────────┬────────────────────────────────────────────────────┘
         │
         ├─────────────────────────────────────────┬───────────────────┐
         ↓                                         ↓                   ↓
┌──────────────────────┐      ┌──────────────────────┐    ┌──────────────────┐
│   STATIC WEB APP     │      │  APP SERVICE (FastAPI│    │  FOUNDRY AGENTS   │
│   (React Frontend)   │      │  + Agent Framework)  │    │  (Model Runtime)  │
│  - index.html        │      │  - Tool implementations     │  - Agent         │
│  - Chat.tsx          │      │  - API endpoints      │    │  - Orchestration │
│  - CSS/Assets        │      │  - Python runtime     │    │  - Tool calls    │
└──────────────────────┘      └──────────┬───────────┘    └────────┬─────────┘
                                         │                         │
                                         └─────────────┬───────────┘
                                                       │
                    ┌──────────────────────────────────┴─────────────────┐
                    │                                                    │
                    ↓                                                    ↓
        ┌───────────────────────┐                       ┌──────────────────────┐
        │  AZURE KEYVAULT       │                       │  APPLICATION INSIGHTS│
        │  - Secrets            │                       │  - Agent traces      │
        │  - Credentials        │                       │  - Performance       │
        │  - Connection strings │                       │  - Errors            │
        └───────────────────────┘                       └──────────────────────┘
                    │                                    
                    ├─────────────────────┬──────────────┤
                    ↓                     ↓              ↓
        ┌──────────────────┐  ┌─────────────────┐  ┌──────────────┐
        │   POSTGRESQL     │  │  AZURE OPENAI   │  │  AZURE AI    │
        │   (Conversations)│  │  (LLM inference)│  │  (Embeddings)│
        │   - Messages     │  │  - Chat models  │  │              │
        │   - History      │  │  - Completions  │  └──────────────┘
        │   - State        │  │                 │
        └──────────────────┘  └─────────────────┘
```

### Components

**Frontend Layer**:
- Azure Static Web App (React app, Chat.tsx)
- Global CDN for static assets
- Auto-deployed from GitHub (CI/CD)

**Backend Layer**:
- Azure App Service (Python FastAPI runtime)
- Auto-scaling based on CPU/memory
- Health checks every 30s
- Graceful shutdown on updates

**Agent Layer**:
- Azure AI Foundry Agents
- Manages agent state and orchestration
- Calls tools (FastAPI endpoints)
- Handles streaming responses

**Data Layer**:
- PostgreSQL (flexible server)
- Stores conversation history
- Automatic backups, read replicas
- VNet integration for security

**LLM Layer**:
- Azure OpenAI Service
- GPT-4o models for agent reasoning
- Quota management and rate limiting
- Regional failover support

**Observability**:
- Application Insights
- Traces agent tool calls, decisions
- Logs all API requests/responses
- Alerts on errors and latency

---

## 📚 Section 2: Bicep Infrastructure Templates

### Bicep Best Practices for Agent Apps

**1. Use Symbolic References (Not resourceId)**
```bicep
// ✅ GOOD: Symbolic references
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: 'B2'
    capacity: 1
  }
}

resource appService 'Microsoft.Web/sites@2023-12-01' = {
  name: appServiceName
  location: location
  properties: {
    serverFarmId: appServicePlan.id  // Direct reference
  }
}

// ❌ BAD: Using resourceId function
resource appService 'Microsoft.Web/sites@2023-12-01' = {
  name: appServiceName
  location: location
  properties: {
    serverFarmId: resourceId('Microsoft.Web/serverfarms', appServicePlanName)
  }
}
```

**2. Use User-Defined Types for Configuration**
```bicep
@export()
type ConfigSettings = {
  @description('Environment name (dev, staging, prod)')
  environment: 'dev' | 'staging' | 'prod'
  
  @description('App Service SKU')
  appServiceSku: 'B2' | 'B3' | 'P1V2'
  
  @description('PostgreSQL admin password')
  @secure()
  dbPassword: string
  
  @description('Azure OpenAI API key')
  @secure()
  openaiApiKey: string
}

param config ConfigSettings
```

**3. Use Parameter Files (.bicepparam)**
```bicep
// deployment.bicepparam
using './main.bicep'

param config = {
  environment: 'prod'
  appServiceSku: 'B3'
  dbPassword: readEnvironmentVariable('DB_PASSWORD')
  openaiApiKey: readEnvironmentVariable('OPENAI_API_KEY')
}

param location = 'eastus'
param resourceGroupName = 'rg-customer-service-agent'
```

**4. Handle Child Resources with parent Property**
```bicep
// ✅ GOOD: Using parent property
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: appServicePlanName
  location: location
}

// Child resource uses parent, not name with /
resource appServiceAppSettings 'Microsoft.Web/sites/config@2023-12-01' = {
  parent: appService
  name: 'appsettings'
  properties: {
    'WEBSITES_ENABLE_APP_SERVICE_STORAGE': 'false'
    'PYTHON_VERSION': '3.11'
  }
}

// ❌ BAD: Using / in name
resource appServiceAppSettings 'Microsoft.Web/sites/config@2023-12-01' = {
  name: '${appServiceName}/appsettings'
  properties: { }
}
```

**5. Use Safe-Dereference Operator**
```bicep
// ✅ GOOD: Safe dereference with ?? operator
resource postgres 'Microsoft.DBforPostgreSQL/flexibleServers@2023-12-01' = existing = {
  name: postgresServerName
}

output dbFqdn string = postgres.properties.?fullyQualifiedDomainName ?? 'postgres.database.azure.com'

// ❌ BAD: Might fail if property missing
output dbFqdn string = postgres.properties.fullyQualifiedDomainName
```

**6. Use @export() for Reusable Types**
```bicep
// common-types.bicep
@export()
type AgentAppConfig = {
  @description('Foundry agent name')
  agentName: string
  
  @description('Tool definitions from specification')
  tools: {
    name: string
    description: string
  }[]
  
  @description('System instructions for agent')
  instructions: string
}

// Then reuse in main.bicep
param agentConfig AgentAppConfig
```

---

## 📚 Section 3: Foundry Agents Deployment

### Agent Deployment Template Structure

```bicep
// agents.bicep - Separate module for agent setup
param agentName string
param resourceGroupName string
param location string
param appServiceUrl string
param openaiEndpoint string
param foundryEndpoint string

// Create agent in Foundry
resource agent 'Microsoft.AI/foundryAgents/agents@2024-01-01' = {
  name: agentName
  location: location
  properties: {
    instructions: loadTextContent('./agent-instructions.txt')
    tools: [
      {
        name: 'lookup_customer'
        description: 'Find customer by email or ID'
        inputSchema: {
          type: 'object'
          properties: {
            customer_id: {
              type: 'string'
              description: 'Customer email or ID'
            }
          }
          required: ['customer_id']
        }
      }
      {
        name: 'get_return_policy'
        description: 'Check order return eligibility'
        inputSchema: {
          type: 'object'
          properties: {
            order_id: { type: 'string' }
          }
          required: ['order_id']
        }
      }
      {
        name: 'initiate_return'
        description: 'Start return process for order'
        inputSchema: {
          type: 'object'
          properties: {
            order_id: { type: 'string' }
            reason: { type: 'string' }
          }
          required: ['order_id', 'reason']
        }
      }
    ]
    model: {
      deployment: 'gpt-4o'
      endpoint: openaiEndpoint
    }
  }
}

// Configure tool endpoints (point to FastAPI)
resource agentToolEndpoints 'Microsoft.AI/foundryAgents/agents/toolEndpoints@2024-01-01' = {
  parent: agent
  name: 'fastapi-tools'
  properties: {
    baseUrl: '${appServiceUrl}/tools'
    authentication: {
      type: 'managedIdentity'
    }
  }
}

output agentId string = agent.id
output agentEndpoint string = agent.properties.endpoint
```

### Agent Instructions Template

```text
# Customer Service Agent

You are a helpful customer service agent for an e-commerce platform.

## Responsibilities
1. Help customers track orders
2. Process returns and refunds
3. Answer questions about policies
4. Escalate complex issues to human support

## Available Tools
- lookup_customer: Find customer account
- search_orders: List customer orders
- get_return_policy: Check return eligibility
- initiate_return: Start return process
- get_refund_status: Track refund progress
- create_support_ticket: Escalate to support

## Behavior Guidelines
1. Always start by looking up the customer
2. Verify order eligibility before processing returns
3. Be empathetic and clear about policies
4. Escalate immediately if customer is frustrated
5. Never promise refunds without verification

## Error Handling
- If order not found: Ask customer to verify order ID
- If policy check fails: Explain reason and offer escalation
- If return initiation fails: Suggest contacting support
```

### Foundry Agent Streaming Response

```python
# How agent responses stream to frontend
from azure.ai.foundry import FoundryAgentClient

client = FoundryAgentClient(
    endpoint=FOUNDRY_ENDPOINT,
    credential=DefaultAzureCredential()
)

# Stream responses from agent
async def stream_agent_response(conversation_id: str, user_message: str):
    """Stream agent response to frontend."""
    
    # Send message to Foundry agent
    with client.agent_chat(
        agent_id=AGENT_ID,
        conversation_id=conversation_id,
        message=user_message,
        stream=True  # Enable streaming
    ) as response:
        # Yield response chunks as they arrive
        for chunk in response:
            # chunk.delta contains incremental response text
            # chunk.tool_calls contains tool calls made
            # chunk.tool_results contains tool execution results
            yield chunk.delta.content if chunk.delta else ""
            
            # Save tool calls to conversation history
            if chunk.tool_calls:
                for tool_call in chunk.tool_calls:
                    await save_tool_call(
                        conversation_id=conversation_id,
                        tool_name=tool_call.function.name,
                        parameters=tool_call.function.arguments,
                        result=tool_call.result
                    )
```

---

## 📚 Section 4: CI/CD Pipeline for Automated Deployment

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/agent

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
      
      - name: Run backend tests
        run: |
          pytest backend/tests/ -v --cov=backend/agents
      
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Build frontend
        run: |
          cd frontend && npm ci && npm run build

  deploy-infrastructure:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy Bicep templates
        uses: azure/arm-deploy@v1
        with:
          subscriptionId: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          resourceGroupName: rg-customer-service-agent
          template: ./infrastructure/main.bicep
          parameters: ./infrastructure/deployment.bicepparam
      
  deploy-backend:
    needs: deploy-infrastructure
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build and push Docker image
        run: |
          docker build -t ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} ./backend
          docker push ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
      
      - name: Deploy to App Service
        uses: azure/webapps-deploy@v2
        with:
          app-name: app-customer-service-agent
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
  
  deploy-frontend:
    needs: deploy-infrastructure
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build frontend
        run: |
          cd frontend && npm ci && npm run build
      
      - name: Deploy to Static Web App
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_TOKEN }}
          action: "upload"
          app_location: "frontend/dist"
          api_location: ""
          output_location: ""
```

### Deployment Steps

```bash
# 1. Authenticate to Azure
az login
az account set --subscription <subscription-id>

# 2. Create resource group
az group create \
  --name rg-customer-service-agent \
  --location eastus

# 3. Deploy Bicep templates
az deployment group create \
  --resource-group rg-customer-service-agent \
  --template-file infrastructure/main.bicep \
  --parameters infrastructure/deployment.bicepparam

# 4. Deploy application (CI/CD handles this, but manual option)
az functionapp deployment source config-zip \
  --name app-customer-service-agent \
  --resource-group rg-customer-service-agent \
  --src ./backend/dist.zip
```

---

## 📚 Section 5: Monitoring & Observability with Application Insights

### Application Insights Setup in Bicep

```bicep
// monitoring.bicep
param appInsightsName string
param location string
param logAnalyticsWorkspaceName string

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: logAnalyticsWorkspaceName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
    RetentionInDays: 30
  }
}

// Alert for high error rate
resource errorRateAlert 'Microsoft.Insights/metricAlerts@2018-03-01' = {
  name: 'high-error-rate-alert'
  location: 'global'
  properties: {
    description: 'Alert when error rate > 5%'
    severity: 2
    enabled: true
    scopes: [appInsights.id]
    evaluationFrequency: 'PT5M'
    windowSize: 'PT15M'
    criteria: {
      'odata.type': 'Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria'
      allOf: [
        {
          name: 'Error Rate'
          metricName: 'failedRequests'
          operator: 'GreaterThan'
          threshold: 5
          timeAggregation: 'Average'
        }
      ]
    }
    actions: []
  }
}

output appInsightsKey string = appInsights.properties.InstrumentationKey
output logAnalyticsWorkspaceId string = logAnalyticsWorkspace.id
```

### Agent Monitoring in Python

```python
# monitoring.py
from opentelemetry import trace, metrics
from azure.monitor.opentelemetry import configure_azure_monitor

# Configure Azure Monitor
configure_azure_monitor(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)

tracer = trace.get_tracer(__name__)

def monitor_agent_execution(conversation_id: str, user_message: str):
    """Trace agent execution with full observability."""
    
    with tracer.start_as_current_span("agent_execution") as span:
        span.set_attribute("conversation_id", conversation_id)
        span.set_attribute("message_length", len(user_message))
        span.set_attribute("timestamp", datetime.utcnow().isoformat())
        
        # Trace agent tool calls
        for tool_call in agent.get_tool_calls():
            with tracer.start_as_current_span("tool_call") as tool_span:
                tool_span.set_attribute("tool_name", tool_call.name)
                tool_span.set_attribute("tool_params", str(tool_call.parameters))
                
                # Execute tool and trace result
                result = execute_tool(tool_call)
                tool_span.set_attribute("tool_result", str(result))
                tool_span.set_attribute("tool_duration_ms", tool_call.duration_ms)
        
        # Trace agent decision
        span.set_attribute("agent_decision", agent.last_decision)
        span.set_attribute("response_length", len(agent.response))
        
        return agent.response

# View traces in Azure Portal → Application Insights → Performance
```

---

## 📚 Section 6: Hands-On - Generate Deployment Artifacts with `/speckit.implement`

### Step 1: Create Deployment Specification

Before running `/speckit.implement`, clarify deployment requirements:

```
/speckit.specify Customer Service Agent Deployment to Azure

Requirements:
- Deploy to Azure using Bicep Infrastructure as Code
- Use Azure App Service for FastAPI backend
- Use Azure Static Web App for React frontend
- Use Azure PostgreSQL for data persistence
- Integrate with Azure OpenAI for LLM inference
- Deploy Foundry agents for agent orchestration
- Setup CI/CD pipeline with GitHub Actions
- Configure Application Insights for monitoring
- Implement security: KeyVault, managed identities, VNet integration
```

### Step 2: Generate Deployment Plan

In GitHub Copilot Chat:

```
/speckit.plan for Azure infrastructure deployment

Focus on:
- Bicep templates following Microsoft best practices
- Separate modules for compute, database, monitoring
- Parameter files for different environments (dev, staging, prod)
- User-defined types for type safety
- Managed identities for secure service-to-service auth
- CI/CD workflow with GitHub Actions
- Observability with Application Insights
```

### Step 3: Generate Deployment Artifacts

**IMPORTANT**: This step generates **infrastructure only**, not application code.

In GitHub Copilot Chat:

```
/speckit.implement for deployment artifacts only

Generate:
✅ Infrastructure (Bicep templates, parameter files)
✅ CI/CD pipeline (GitHub Actions workflows)
✅ Deployment scripts (bash/PowerShell)
✅ Configuration files (app settings, environment variables)

DO NOT generate:
❌ Application code (already completed in Module 4)
❌ Tool implementations (already completed)
❌ Database schema (already completed)
```

**What Gets Generated**:

```
infrastructure/
├── main.bicep              # Root template
├── modules/
│   ├── networking.bicep    # VNet, subnets, NSGs
│   ├── compute.bicep       # App Service, Static Web App
│   ├── database.bicep      # PostgreSQL flexible server
│   ├── monitoring.bicep    # Application Insights, Log Analytics
│   ├── security.bicep      # KeyVault, managed identities
│   └── foundry.bicep       # Foundry agents configuration
├── deployment.bicepparam   # Production parameters
├── deployment.dev.bicepparam
├── deployment.staging.bicepparam
├── common-types.bicep      # User-defined types
└── agent-instructions.txt  # Agent system prompt

scripts/
├── deploy.sh               # Main deployment script
├── setup-roles.sh          # Configure RBAC
├── configure-secrets.sh    # Populate KeyVault
└── cleanup.sh              # Remove resources

.github/workflows/
├── deploy.yml              # Deployment pipeline
├── test.yml                # Testing pipeline
└── rollback.yml            # Rollback procedure

docs/
├── DEPLOYMENT.md           # Deployment guide
├── TROUBLESHOOTING.md      # Common issues
└── ARCHITECTURE.md         # Architecture decisions
```

### Step 4: Review Generated Infrastructure

```bash
# Validate Bicep templates
az bicep build-params infrastructure/deployment.bicepparam

# Check syntax
az bicep lint infrastructure/main.bicep

# Preview changes (what will be deployed)
az deployment group what-if \
  --resource-group rg-customer-service-agent \
  --template-file infrastructure/main.bicep \
  --parameters infrastructure/deployment.bicepparam
```

### Step 5: Deploy to Azure

```bash
# Deploy to development environment
./scripts/deploy.sh --environment dev

# Deploy to production (requires approval)
./scripts/deploy.sh --environment prod

# Monitor deployment
az deployment group show \
  --resource-group rg-customer-service-agent \
  --name CustomerServiceAgentDeployment
```

### Step 6: Verify Deployment

```bash
# Check deployed resources
az resource list --resource-group rg-customer-service-agent

# Test FastAPI endpoint
curl https://app-customer-service-agent.azurewebsites.net/health

# Access frontend
open https://app-customer-service-agent.azurestaticapps.net

# View agent traces
az monitor app-insights metrics show \
  --resource-group rg-customer-service-agent \
  --app insights-agent
```

---

## 📚 Section 7: Key Deployment Concepts

### Infrastructure as Code with Bicep

**Why Bicep for Agent Apps**:
- Type-safe parameter definitions
- Reusable modules (networking, compute, monitoring)
- Symbolic references instead of resourceId() strings
- Parameter files for environment management
- Works with Azure Policy for compliance
- Version controlled for repeatability

### Foundry Agent Deployment Model

**Stateless Design**:
- Agent logic runs in Foundry service
- Tool calls routed to FastAPI backend
- Conversation state in PostgreSQL
- Enabling horizontal scaling

**Tool Integration**:
- Tools defined in Bicep (inputSchema, description)
- Tools execute on FastAPI backend
- Results returned to agent
- Agent decides next steps

### Zero-Trust Security

**Principles**:
1. **Never trust, always verify**: Managed identities, not connection strings
2. **Least privilege**: RBAC roles scoped to specific resources
3. **Encryption in transit**: HTTPS, mTLS between services
4. **Secrets in KeyVault**: Never in environment variables
5. **Network isolation**: VNet integration, private endpoints

**Implementation**:
```bicep
// Use managed identity instead of secrets
resource appService 'Microsoft.Web/sites@2023-12-01' = {
  identity: {
    type: 'SystemAssigned'
  }
}

// Grant identity access to KeyVault
resource keyVaultAccessPolicy 'Microsoft.KeyVault/vaults/accessPolicies@2023-07-01' = {
  parent: keyVault
  name: 'add'
  properties: {
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: appService.identity.principalId
        permissions: {
          secrets: ['get', 'list']
        }
      }
    ]
  }
}
```

### Environment Management

**Three Environments**:

| Environment | Purpose | Scale | Approvals |
|-----------|---------|-------|-----------|
| Development | Rapid iteration, testing | Small (B2 App Service) | None |
| Staging | Pre-production validation | Medium (B3 App Service) | One approver |
| Production | Live agent | Large (P1V2 App Service) | Two approvers |

**Parameter Inheritance**:
```bicep
// deployment.bicepparam
param config = environment() == 'prod' ? prodConfig : devConfig

var prodConfig = {
  appServiceSku: 'P1V2'
  dbBackupRetention: 35
  enableAutoScale: true
  alertingSeverity: 1
}

var devConfig = {
  appServiceSku: 'B2'
  dbBackupRetention: 7
  enableAutoScale: false
  alertingSeverity: 3
}
```

---

## 📚 Section 8: Best Practices Checklist

**Pre-Deployment**:
- [ ] All tests pass (backend + frontend)
- [ ] Bicep templates validated with `az bicep lint`
- [ ] Infrastructure changes reviewed in `what-if`
- [ ] All secrets stored in KeyVault (never in code)
- [ ] RBAC roles follow least privilege principle
- [ ] Application Insights configured for monitoring
- [ ] Disaster recovery plan documented

**Deployment**:
- [ ] Deploy infrastructure first (Bicep), then application
- [ ] Use deployment slots for zero-downtime updates
- [ ] Verify health checks pass on new instances
- [ ] Monitor error rates during rollout
- [ ] Keep previous version available for rollback

**Post-Deployment**:
- [ ] Smoke tests pass against live endpoint
- [ ] Agent responds correctly to test queries
- [ ] Tool calls execute successfully
- [ ] Conversation history persists in PostgreSQL
- [ ] Metrics flowing to Application Insights
- [ ] Load test validates scaling policies
- [ ] Security scan completes without issues

---

## ✅ Module 5 Quiz

**Question 1**: You're deploying the agent app to Azure. Your Bicep template references a PostgreSQL server with `resourceId()` instead of symbolic references. What's the problem?
- A) It won't work; resourceId() is deprecated
- B) It's less maintainable; if you rename resources, references break
- C) It bypasses type checking; you lose Bicep validation
- D) All of the above

**Question 2**: The Foundry agent needs to call a tool implemented on FastAPI. In your Bicep template, how should you connect them?
- A) Pass the FastAPI URL as an environment variable
- B) Use managed identity to authenticate, configure tool endpoint
- C) Both A and B
- D) Create a direct Azure Service Bus connection

**Question 3**: Your CI/CD pipeline tests pass, but you're worried about deploying to production. What safety mechanisms should you use?
- A) Deployment slots for zero-downtime updates
- B) Approval gates before production push
- C) Health checks to verify agent is responding correctly
- D) All of the above

**Question 4**: How should you store database passwords and API keys in Azure?
- A) In environment variables on App Service
- B) In KeyVault with managed identity access
- C) In a configuration file in the repository
- D) Hardcoded in Bicep templates

**Question 5**: You need to monitor whether the agent is making correct tool calls. Where do you configure this?
- A) Application Insights with OpenTelemetry tracing
- B) GitHub Actions workflow logs
- C) Azure Monitor alerts only
- D) Frontend console logging

---

### 📚 Quick Reference: Bicep Best Practices

| Practice | Good | Avoid |
|----------|------|-------|
| Resource References | `appService.id` | `resourceId(...)` |
| Child Resources | `parent: parentResource` | `name: 'parent/child'` |
| Parameters | User-defined types | Individual `param` for each value |
| Secrets | `@secure()` decorator | Plaintext strings |
| Safe Access | `resource.?property ?? default` | `resource.property` without null checks |

---

## Resources

- [Bicep Documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep)
- [Bicep Best Practices](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/best-practices)
- [Azure AI Foundry Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents)
- [Agent Framework Deployment](https://learn.microsoft.com/en-us/agent-framework/deployment)
- [Azure App Service](https://learn.microsoft.com/en-us/azure/app-service)
- [PostgreSQL on Azure](https://learn.microsoft.com/en-us/azure/postgresql)
- [Application Insights](https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)

---

## Next Steps

**You've completed the full spec-driven development lab!**

From Constitution → Specification → Planning → Implementation → **Deployment**

Your customer service agent is now:
- ✅ Fully specified in Modules 1-3
- ✅ Implemented with Agent Framework in Module 4
- ✅ **Deployed to Azure with infrastructure as code in Module 5**

**Your agent is running live on Azure!**

### Post-Deployment Workflow

1. **Monitor** agent performance in Application Insights
2. **Iterate** by updating specification in Module 2, then regenerate
3. **Scale** by adjusting Bicep parameters for different environments
4. **Maintain** specification as source of truth, code as generated output
5. **Evolve** agent by creating new feature specifications

This is the power of **Specification-Driven Development**: Change requirements in spec, regenerate implementation and infrastructure, deploy automatically. No manual rewrites, no drift between intent and code.

**Welcome to the future of software development.** 🚀

